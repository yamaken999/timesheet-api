---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

name: Bug Report 🐛
description: 不具合の詳細を報告します
title: "[BUG] "
labels: ["bug"]
body:
  - type: input
    id: environment
    attributes:
      label: 使用環境
      placeholder: 例）Chrome 125 / Windows 11
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: 再現手順
      placeholder: |
        1. ○○を開く
        2. ○○を実行する
        3. エラー発生
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: 期待する挙動
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: 実際の挙動
    validations:
      required: true
