# Azure App Service リソース作成スクリプト
# 事前に az login でログインしてください

# 変数設定
$resourceGroup = "timesheet-rg"
$location = "Japan East"
$appServicePlan = "timesheet-plan"
$apiAppName = "timesheet-api-prod"
$frontendAppName = "timesheet-frontend-prod"
$stagingApiAppName = "timesheet-api-staging"
$stagingFrontendAppName = "timesheet-frontend-staging"

# リソースグループ作成
Write-Host "Creating resource group..."
az group create --name $resourceGroup --location $location

# App Service Plan 作成（無料プラン F1）
Write-Host "Creating App Service Plan..."
az appservice plan create --name $appServicePlan --resource-group $resourceGroup --sku F1 --is-linux

# 本番環境 - API App Service 作成
Write-Host "Creating API App Service (Production)..."
az webapp create --resource-group $resourceGroup --plan $appServicePlan --name $apiAppName --runtime "PYTHON|3.11"

# 本番環境 - Frontend App Service 作成
Write-Host "Creating Frontend App Service (Production)..."
az webapp create --resource-group $resourceGroup --plan $appServicePlan --name $frontendAppName --runtime "NODE|18-lts"

# 検証環境 - API App Service 作成
Write-Host "Creating API App Service (Staging)..."
az webapp create --resource-group $resourceGroup --plan $appServicePlan --name $stagingApiAppName --runtime "PYTHON|3.11"

# 検証環境 - Frontend App Service 作成
Write-Host "Creating Frontend App Service (Staging)..."
az webapp create --resource-group $resourceGroup --plan $appServicePlan --name $stagingFrontendAppName --runtime "NODE|18-lts"

# App Settings 設定
Write-Host "Setting app configurations..."
az webapp config appsettings set --resource-group $resourceGroup --name $apiAppName --settings WEBSITES_PORT=8000
az webapp config appsettings set --resource-group $resourceGroup --name $stagingApiAppName --settings WEBSITES_PORT=8000

Write-Host "Azure resources created successfully!"
Write-Host "API Production URL: https://$apiAppName.azurewebsites.net"
Write-Host "Frontend Production URL: https://$frontendAppName.azurewebsites.net"
Write-Host "API Staging URL: https://$stagingApiAppName.azurewebsites.net"
Write-Host "Frontend Staging URL: https://$stagingFrontendAppName.azurewebsites.net"

Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Set up GitHub Actions secrets in your repository:"
Write-Host "   - AZURE_WEBAPP_API_PUBLISH_PROFILE"
Write-Host "   - AZURE_WEBAPP_FRONTEND_PUBLISH_PROFILE"
Write-Host "2. Get publish profiles from Azure Portal"
Write-Host "3. Push code to trigger deployment"
