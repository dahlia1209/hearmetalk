# hearmetalk

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


### GitHub
https://github.com/dahlia1209/hearmetalk.git

### tamaranbai

### Web Site
https://ashy-mushroom-062ed5b10.4.azurestaticapps.net/


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
