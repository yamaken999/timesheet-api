from flask import Flask, request, send_file
import pandas as pd
import tempfile

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    df = pd.read_csv(file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        df.to_excel(tmp.name, index=False)
        return send_file(tmp.name, as_attachment=True, download_name="timesheet.xlsx")

@app.route("/", methods=["GET"])
def index():
    return "Render connection OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
