# タイムシートAPI構築・デプロイ手順書（Flask + Render）

## ⚙️ 環境構築手順

### 必要なサービス

- [Render](https://render.com/)：Flaskアプリを無料でホスト
- [GitHub](https://github.com/)：ソースコード管理と連携

### セットアップ手順

1. Python環境に以下のパッケージをインストール：

   - flask
   - flask-cors
   - pandas
   - openpyxl

2. Flaskアプリのディレクトリ構成例：

```
project_root/
├─ app.py
├─ requirements.txt
├─ .render.yaml
└─ static/ (HTML/JSなど)
```

3. `requirements.txt` に依存ライブラリを記述：

```
flask
flask-cors
pandas
openpyxl
```

4. `.render.yaml` を用意：

```yaml
services:
  - type: web
    name: timesheet-api
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"
    envVars:
      - key: PORT
        value: 10000
```

5. GitHubにPushし、Renderで新規サービスとしてデプロイ

---

## 📦 インポートしているライブラリの説明

| ライブラリ名     | 説明                                       |
| ---------- | ---------------------------------------- |
| flask      | Webアプリを作るためのPythonの軽量フレームワーク             |
| flask-cors | 他のWebサイト（例：GitHub Pages）からアクセスを許可するための拡張 |
| pandas     | CSVデータを読み込んで整形・加工するためのデータ処理ライブラリ         |
| openpyxl   | Excelファイルを読み書きするためのライブラリ                 |
| datetime   | 日付や時間の操作を行う標準ライブラリ                       |
| io         | メモリ上でファイルのように扱えるデータストリーム処理               |
| os         | ファイル名の操作や環境変数の取得など、OSとのやり取りに使う標準モジュール    |
| tempfile   | 一時ファイルの作成・管理用ライブラリ（今回は未使用の可能性あり）         |

---

## 📘 仕様概要

### 入力

- CSVファイル：2つ（勤務開始・終了、休憩情報など）
- Excelテンプレート：1つ
- ユーザー入力フォーム：氏名、EID、対象年月、タスク名、社長モードのON/OFF

### 出力

- テンプレートに勤務情報を反映し、Excel形式で返却
- 出力ファイル名：`テンプレートファイル名_EID.xlsx`

### 主な機能

- 勤務開始・終了時間、休憩時間を元に実働時間を計算
- 社長モードON時：4時間48分を上限とし、超過時間を分離表示
- 「就業時間」セルに `=SUM(...)` の数式挿入
- 「実働日」セルに `=COUNTA(...)` の数式挿入
- D8セルに氏名、D9セルに対象年月の1日を設定
- CORS許可済（外部ドメインからのfetch対応）

---

### 💡 CORSと外部ドメインからのfetchとは？（かんたん説明）

#### 🔒 CORSとは？

「このサーバー、外からデータを取りにきていいですか？」と聞くしくみです。 Webサイトから他のサーバーにデータを送ったりもらったりする時、勝手にアクセスできないようにブロックされます。

#### ✅ このアプリでは？

GitHub Pagesで公開している画面（フロント）から、RenderのAPI（バックエンド）にデータを送る必要があります。 そのため、「このWebサイト（GitHub Pages）からならOKだよ」とFlask側で許可しておく必要があるのです。

#### 📘 例えるなら

学校に遊びに来た友達が「○○くんの部屋に入ってもいい？」と親に聞いて、親が「うん、この子はOK」と言ってくれるようなものです。

---

### 備考

- HTMLフォームでは、ドラッグ＆ドロップとファイル選択ボタン両対応
- 入力ファイルはlocalStorageに保存され、再利用可能
- 不正なファイル数や形式にはサーバー側でバリデーションあり

---

以上の構成により、GitHub PagesとRenderを用いたタイムシート生成Webアプリが構築されます。

