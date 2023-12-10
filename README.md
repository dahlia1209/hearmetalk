# hearmetalk

## Frontend Project setup
### モジュールのインストール
```
cd ./frontend
npm install
```

### Compiles and hot-reloads for development
```
npm run dev
```

### Compiles and minifies for production
```
npm run build
npm run serve
```

### Lints and fixes files
```
npm run lint
```
## Backend Project setup

## Resources

### GitHub
https://github.com/dahlia1209/hearmetalk.git

### tamaranbai

### Web Site
https://ashy-mushroom-062ed5b10.4.azurestaticapps.net/

### API endpoint
https://nakamura-app-01.azurewebsites.net/


### リソース構築メモ
#### リソース作成・デプロイ
(az login)
az group create --name nakamura-rg-99 --location "eastus" 
cd C:\src\hearmetalk\backend
az webapp up -g nakamura-rg-99 -n nakamura-app-01 -p appserviceplan-nakamura-app-01 --runtime PYTHON:3.11 --sku B1
cd C:\src\hearmetalk\resources
az deployment group create --resource-group "nakamura-rg-99" --template-file ".\backend.bicep"

#### リソース削除
az group delete -n nakamura-rg-99 -y

#### 再デプロイ
az webapp up -g nakamura-rg-99 -n nakamura-app-01 -p appserviceplan-nakamura-app-01 --runtime PYTHON:3.11 --sku B1
az webapp restart -g nakamura-rg-99 -n nakamura-app-01
