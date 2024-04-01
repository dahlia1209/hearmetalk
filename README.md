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
az group create --name nakamura-rg-99 --location "Japan East" 
cd C:\src\hearmetalk\backend
az webapp up -g nakamura-rg-99 -n nakamura-app-01 -p appserviceplan-nakamura-app-01 --runtime PYTHON:3.11 --sku B1
cd C:\src\hearmetalk\resources
az deployment group create --resource-group "nakamura-rg-99" --template-file ".\backend.bicep"

#### リソース削除
az group delete -n nakamura-rg-99 -y

#### 再デプロイ
az webapp up -g nakamura-rg-99 -n nakamura-app-01 -p appserviceplan-nakamura-app-01 --runtime PYTHON:3.11 --sku B1
az webapp restart -g nakamura-rg-99 -n nakamura-app-01

#### docker 起動
・speech to text
docker run --rm -it -p 5000:5000 --memory 8g --cpus 4 `
mcr.microsoft.com/azure-cognitive-services/speechservices/speech-to-text:4.5.0-amd64-ja-jp `
Eula=accept `
Billing=https://eastus.api.cognitive.microsoft.com/ `
ApiKey={apikey}

・text to speech
docker run --rm -it -p 5001:5000 --memory 12g --cpus 6 `
mcr.microsoft.com/azure-cognitive-services/speechservices/neural-text-to-speech:3.1.0-amd64-ja-jp-nanamineural `
Eula=accept `
Billing=https://eastus.api.cognitive.microsoft.com/ `
ApiKey={API_KEY}

#### speechToText app service作成
az group create --name nakamura-rg-99 --location "eastus" 
cd C:\src\hearmetalk\resources\speechToText
az deployment group create --resource-group "nakamura-rg-99" --template-file ".\app.bicep"

#### OpenAIContainer作成
cd C:\src\hearmetalk\backend-fastapi\  
az acr build --resource-group nakamura-rg --registry nakamuraacr --image openaicompletions:latest .

#### AKS作成
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name chat --yes
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name speech-to-text  --yes
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name chat --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name speech-to-text  --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech --yes
az group create --name nakamura-rg-aks --location "japaneast" 
az aks create --resource-group nakamura-rg-aks --name nakamura-aks  --generate-ssh-keys --attach-acr nakamuraacr  --node-vm-size Standard_B8s_v2 --enable-cluster-autoscaler --min-count 1 --max-count 20 --enable-addons monitoring --enable-app-routing  --node-count 1 --enable-aad --aad-admin-group-object-ids 167cbd1d-f736-4590-9154-6c899fb2311d
az aks get-credentials --resource-group nakamura-rg-aks --name nakamura-aks --overwrite-existing
$ZONEID=$(az network dns zone show -g nakamura-rg -n hearmetalk.net --query "id" --output tsv)
az aks approuting zone add -g nakamura-rg-aks -n nakamura-aks --ids=$ZONEID --attach-zones
$KEYVAULTID=$(az keyvault show --name nakamura-kv --query "id" --output tsv)
az aks approuting update  --resource-group nakamura-rg-aks --name nakamura-aks --enable-kv --attach-kv $KEYVAULTID
$IDENTITY_OBJECT_ID=$(az aks show -g nakamura-rg-aks -n nakamura-aks --query addonProfiles.azureKeyvaultSecretsProvider.identity.objectId -o tsv)
$KEYVAULT_SCOPE=$(az keyvault show --name nakamura-kv --query id -o tsv)
az role assignment create --role "Key Vault Administrator" --assignee $IDENTITY_OBJECT_ID --scope $KEYVAULT_SCOPE

cd C:\src\hearmetalk\kubernetes

Import-Module C:\src\hearmetalk\kubernetes\helper.psm1
replaceAksClientId
replaceIngressWhitelistIp
replaceServiceWhitelistIp
kubectl apply -f .\SecretProviderClass.yaml 
kubectl apply -f .\ubuntu-deployment.yaml
kubectl apply -f .\ubuntu-service.yaml
kubectl apply -f .\neural-text-to-speech-deployment.yaml
kubectl apply -f .\neural-text-to-speech-service.yaml
kubectl apply -f .\neural-text-to-speech-ingress.yaml
kubectl apply -f .\neural-text-to-speech-en-deployment.yaml
kubectl apply -f .\neural-text-to-speech-en-service.yaml
kubectl apply -f .\neural-text-to-speech-en-ingress.yaml
kubectl apply -f .\openaicompletions-deployment.yaml
kubectl apply -f .\openaicompletions-service.yaml
kubectl apply -f .\openaicompletions-ingress.yaml
#kubectl apply -f .\mssql-deployment.yaml
#kubectl apply -f .\mssql-service.yaml
#kubectl apply -f .\speech-to-text-deployment.yaml
#kubectl apply -f .\speech-to-text-service.yaml
#kubectl apply -f .\speech-to-text-ingress.yaml
az aks update -g nakamura-rg-aks -n nakamura-aks --enable-aad --aad-admin-group-object-ids 167cbd1d-f736-4590-9154-6c899fb2311d
 
kubectl get deployment
kubectl get service
kubectl get ingress

■Ubuntuのコマンド
sudo apt-get -y update
sudo apt install -y obs-studio ffmpeg v4l2loopback-dkms language-pack-ja fonts-ipafont fonts-ipaexfont wget
fc-cache -fv 
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install /config/google-chrome-stable_current_amd64.deb -y

■削除
az group delete -n nakamura-rg-aks -y


### Tips
#### 証明書
https://www.ipentec.com/document/windows-iis-ssl-wild-card-domain-certificate-using-win-acme

cd C:\src\hearmetalk\backend-oauth2
venv\Scripts\activate    
uvicorn main:app --reload