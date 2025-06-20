---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: ''
assignees: ''

---

name: Feature Request ✨
description: 新しい機能や改善提案を投稿します
title: "[Feature] "
labels: ["enhancement"]
body:
  - type: input
    id: summary
    attributes:
      label: 機能概要
      placeholder: 例）テンプレートを複数保存できるようにする
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: 必要と感じた理由
    validations:
      required: true

  - type: textarea
    id: suggestion
    attributes:
      label: 実装案（任意）
    validations:
      required: false
