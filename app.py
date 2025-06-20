from flask import Flask, request, send_file, render_template
from flask_cors import CORS
from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime, date, timedelta
import pandas as pd
import tempfile
import os
import io

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

@app.route("/upload", methods=["POST"])
def generate_timesheet():
    files = request.files.getlist("files")
    name = request.form.get("name")
    eid = request.form.get("eid")
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))
    task = request.form.get("task")
    president_mode = request.form.get("president") == "on"

    # ファイル分類
    csv_files = [f for f in files if f.filename.lower().endswith(".csv")]
    excel_files = [f for f in files if f.filename.lower().endswith(".xlsx")]
    if len(csv_files) != 2 or len(excel_files) != 1:
        return "ファイル数が不正です（CSV2個・Excel1個）", 400

    # テンプレートファイル名を抽出
    template_filename = os.path.splitext(excel_files[0].filename)[0]

    # CSV読み込み＆結合
    df_all = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    df_all["Work start"] = pd.to_datetime(df_all["Work start"], errors="coerce")
    df_all["Work end"] = pd.to_datetime(df_all["Work end"], errors="coerce")
    df_all["Break start"] = pd.to_datetime(df_all["Break start"], errors="coerce")
    df_all["Break end"] = pd.to_datetime(df_all["Break end"], errors="coerce")
    df_all["Date"] = df_all["Work start"].dt.date
    df_all.sort_values("Work start", inplace=True)

    # Excelテンプレート読み込み
    wb = load_workbook(filename=io.BytesIO(excel_files[0].read()))
    ws = wb.worksheets[0]
    ws.title = f"{month}月"

    d9_date = date(year, month, 1)
    ws["D6"] = "部署名（必要に応じて固定で書く）"
    ws["D8"] = name
    ws["D9"] = d9_date

    days_in_month = pd.Timestamp(year=year, month=month, day=1).days_in_month
    limit_timedelta = timedelta(hours=4, minutes=48)

    # 祝日辞書の読み込み
    holiday_dict = {}
    try:
        with open("holidays.csv", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split(",")
                if len(parts) >= 2:
                    holiday_dict[parts[0]] = parts[1]
    except:
        pass

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        row = 12 + day
        date_str = current_date.strftime("%Y-%m-%d")
        day_data = df_all[df_all["Date"] == current_date]
        holiday_name = holiday_dict.get(date_str)

        # C列（業務内容・祝日名など）の記入
        if holiday_name:
            ws[f"C{row}"] = holiday_name
        elif current_date.weekday() < 5:
            ws[f"C{row}"] = task
        else:
            ws[f"C{row}"] = ""

        # 勤務時間の処理
        if not day_data.empty:
            start_time = day_data["Work start"].min()
            end_time = day_data["Work end"].max()
            ws[f"H{row}"] = start_time.time()
            ws[f"I{row}"] = end_time.time()

            valid_breaks = day_data.dropna(subset=["Break start", "Break end"])
            total_break_duration = (valid_breaks["Break end"] - valid_breaks["Break start"]).sum()
            total_work_duration = (end_time - start_time) - total_break_duration

            if president_mode and total_work_duration > limit_timedelta:
                ws[f"K{row}"] = limit_timedelta.total_seconds() / 86400
                excess = total_work_duration - limit_timedelta
                ws[f"G{row}"] = excess.total_seconds() / 86400
                ws[f"G{row}"].font = Font(size=12)
            else:
                ws[f"K{row}"] = total_work_duration.total_seconds() / 86400
                ws[f"G{row}"] = None

            break_minutes = int(total_break_duration.total_seconds() // 60)
            ws[f"J{row}"] = break_minutes / 1440

            for col in ["H", "I", "J", "K", "G"]:
                if ws[f"{col}{row}"].value is not None:
                    ws[f"{col}{row}"].number_format = "h:mm"

        # 休暇の記入条件（勤務なし・平日・祝日でない）
        elif current_date.weekday() < 5 and not holiday_name:
            ws[f"C{row}"] = "休暇"

    # サマリ部分
    def find_cell_by_value(ws, value, column=None):
        for row in ws.iter_rows():
            for cell in row:
                if cell.value == value and (column is None or cell.column == column):
                    return cell
        return None

    end_row = 12 + days_in_month

    # 「就業時間」の下の列（F列）に合計式
    work_time_cell = find_cell_by_value(ws, "就業時間", column=5)
    if work_time_cell:
        target = ws.cell(row=work_time_cell.row, column=6)
        target.value = f"=SUM(K13:K{end_row})/TIME(1,,)"
        target.number_format = "0.0"

    # 「実働日」行のC列に COUNTA(H13:H*)
    actual_day_cell = find_cell_by_value(ws, "実働日")
    if actual_day_cell:
        target = ws.cell(row=actual_day_cell.row, column=3)
        target.value = f"=COUNTA(H13:H{end_row})"

    # ファイル名構築
    safe_eid = eid.replace(" ", "_").replace("　", "_")
    output_filename = f"{template_filename}_{safe_eid}.xlsx"
    output_stream = io.BytesIO()
    wb.save(output_stream)
    output_stream.seek(0)
    return send_file(output_stream, as_attachment=True, download_name=output_filename)

@app.route("/holidays-ui")
def holidays_ui():
    return render_template("holidays.html")

@app.route("/holidays/download")
def download_holidays():
    try:
        return send_file("holidays.csv", as_attachment=True)
    except:
        return "holidays.csv が見つかりません", 404

@app.route("/holidays/upload", methods=["POST"])
def upload_holidays():
    file = request.files.get("file")
    if file and file.filename.endswith(".csv"):
        file.save("holidays.csv")
        return "アップロード完了", 200
    return "CSVファイルのみアップロード可能です", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
