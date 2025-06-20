# 🕒 タイムシート作成くん（Webアプリ & API）

## ✅ 概要

MyTIMから出力した勤怠CSV（前半・後半）とタイムシートExcelテンプレートを使って、  
勤務時間や休憩時間、就業時間などを自動入力したタイムシートを作成できるWebアプリです。

---

## 🌐 システム構成

| 種類 | URL |
|------|-----|
| 🎨 フロントエンド（UI） | [https://yamaken999.github.io/timesheet-frontend/](https://yamaken999.github.io/timesheet-frontend/) |
| 🛠 API（Flask） | [https://timesheet-api-un72.onrender.com](https://timesheet-api-un72.onrender.com) |
| 🎌 祝日メンテナンスUI | [https://timesheet-api-un72.onrender.com/holidays-ui](https://timesheet-api-un72.onrender.com/holidays-ui) |

---

## 📁 ディレクトリ構成（このAPIリポジトリ）

```
timesheet-api/
├── app.py               # Flask API本体
├── holidays.csv         # 祝日データ（UTF-8 CSV）
├── requirements.txt     # 依存パッケージ
├── .render.yaml         # Renderデプロイ設定
├── static/
│   ├── holidays.js
│   ├── holidays.css
│   └── favicon.ico
├── templates/
│   └── holidays.html    # 祝日編集画面テンプレート
├── README.md            # 本ドキュメント
```

---

## 🛠 利用方法（Web UI）

### 準備するもの：

| ファイル | 内容 |
|--------|------|
| 勤怠CSV（前半） | MyTIMから出力（1日〜15日） |
| 勤怠CSV（後半） | MyTIMから出力（16日〜末日） |
| Excelテンプレート | 支給されたタイムシートテンプレート（.xlsx） |

### 操作手順：

1. Web UI で氏名・EID・対象年月などを入力
2. CSV2枚＋Excel1枚をアップロード
3. 「タイムシート作成」ボタンを押下
4. 自動入力されたExcelファイルがダウンロードされます

---

## 📌 特徴・仕様

- **就業時間・休憩時間・残業**などを自動で計算
- **土日祝を除く平日で空欄の場合、休暇**と記入
- **祝日は祝日名が自動入力される**
- **社長モードONで勤務時間に制限（4時間48分）を適用**
- ファイル名は「テンプレート名 + _EID.xlsx」で保存されます
- アップロードしたファイルはメモリ上に展開されるため、オンライン上には保存されません
- 祝日はCSVで管理されており、だれでもメンテナンスできるようにしています

---

## 🎌 祝日管理機能

- `holidays.csv` のデータをWeb UIで編集可能
- [祝日編集画面](https://timesheet-api-un72.onrender.com/holidays-ui) から操作
- CSV形式（例）：
  ```csv
  date,name
  2025-01-01,元日
  2025-01-13,成人の日
  ```

---

## 🧑‍💻 ローカル実行方法（開発者向け）

```bash
pip install -r requirements.txt
python app.py
```

- `http://localhost:10000/upload` でAPIが起動します
- CORS設定済のため、GitHub Pages上のフロントエンドから接続可能

---

## 🐍 使用ライブラリ

| ライブラリ | 用途 |
|-----------|------|
| flask     | 軽量Webアプリフレームワーク |
| flask_cors | フロントエンドからのリクエスト許可 |
| pandas    | CSV集計・日付変換など |
| openpyxl  | Excelテンプレート読み書き |
| datetime  | 日付操作 |
| io        | メモリ内ファイル処理 |

---

## 🔐 注意点

- CSVはMyTIMの出力形式のままでOK（Work start等の列名あり）
- Excelテンプレートは最初のシートが対象になります
- holidays.csvはRender上で毎回読み込まれ、更新が即反映されます

---

## ✨ フロントエンド（GitHub Pages）

フロントエンドは以下のリポジトリで管理しています：

🔗 [https://github.com/yamaken999/timesheet-frontend](https://github.com/yamaken999/timesheet-frontend)

- HTML / JS / CSSにより構成
- GitHub Pagesにホストされており、バックエンドAPIに接続します

---

本アプリは業務効率化を目的に作成されています。  
改善点や要望があればPull Request / Issueでお知らせください！

---

## 📝 コントリビューションと Issue 提出方法

### 🚨 不具合の報告（Bug Report）
1. このリポジトリの `Issues` タブにアクセス
2. `Bug Report` テンプレートを選択して、必要事項を記入・送信してください
3. HTML（frontend）側の`Issues`は 🔗 [frontend側のIssue](https://github.com/yamaken999/timesheet-frontend/issues) に挙げてくれると管理しやすくて助かります

### 💡 機能改善・提案（Feature Request）
1. 同様に `Issues` タブから `Feature Request` テンプレートを使用してください
2. 提案の背景やユースケースを具体的に記述すると採用されやすくなります

### 🤝 コントリビューション（開発への参加）
- `fork` → `feature ブランチで修正` → `Pull Request` をお送りください
- コードの変更点には簡単な説明コメントを付けていただけると助かります

---

### 備考
- APIの実行にrenderの無料プランを使用しています。（月750時間の実行制限あり24h*31d=744h）
- 1APIなら常時起動でいいけれど、2APIになると費用面を考えなければならぬ。
- 15分以上アクセスがないとスリープモードに入ってリクエストのレスポンスが悪くなるので、uptimerobotというサービスを利用して5分に1度リクエストを送るようにしています。
