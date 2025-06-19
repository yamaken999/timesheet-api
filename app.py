from flask import Flask, request, send_file
from openpyxl import load_workbook
from openpyxl.styles import Font
from datetime import datetime, date, timedelta
import pandas as pd
import tempfile
import os
import io

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def generate_timesheet():
    files = request.files.getlist("files")
    name = request.form.get("name")
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

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        row = 12 + day
        date_str = current_date.strftime("%Y-%m-%d")
        day_data = df_all[df_all["Date"] == current_date]

        if not day_data.empty:
            ws[f"C{row}"] = task
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

    # 出力ファイル名を構築
    safe_name = name.replace(" ", "_").replace("　", "_")
    output_filename = f"{template_filename}_{safe_name}.xlsx"

    output_stream = io.BytesIO()
    wb.save(output_stream)
    output_stream.seek(0)
    return send_file(output_stream, as_attachment=True, download_name=output_filename)