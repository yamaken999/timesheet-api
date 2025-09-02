#!/bin/bash
# Azure App Service用の起動スクリプト
gunicorn --bind 0.0.0.0:8000 --workers 1 app:app
