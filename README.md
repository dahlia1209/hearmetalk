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
### OpenAIContainer作成
cd C:\src\hearmetalk\backend-fastapi\  
az acr build --resource-group nakamura-rg --registry nakamuraacr --image openaicompletions:latest .

### ローカルサーバ起動コマンド
cd C:\src\hearmetalk\backend-fastapi
venv\Scripts\activate    
uvicorn main:app --reload

## Resources
### AKS作成
```
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name chat --yes
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name speech-to-text  --yes
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech --yes
az network dns record-set a delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech-en --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name chat --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name speech-to-text  --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech --yes
az network dns record-set txt delete --resource-group nakamura-rg --zone-name hearmetalk.net --name text-to-speech-en --yes
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
replaceServiceWhitelistIp
kubectl apply -f .\SecretProviderClass.yaml 
kubectl apply -f .\ubuntu-deployment.yaml
kubectl apply -f .\ubuntu-service.yaml
replaceIngressWhitelistIp
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
```
■Ubuntuのコマンド
```
sudo apt-get -y update
sudo apt install -y obs-studio ffmpeg v4l2loopback-dkms language-pack-ja fonts-ipafont fonts-ipaexfont wget
fc-cache -fv 
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install /config/google-chrome-stable_current_amd64.deb -y
```
■削除
```
az group delete -n nakamura-rg-aks -y
```

## プッシュ前にやること
・シークレットのスキャン
```
docker pull zricethezav/gitleaks:latest
docker run -v  C:\src\hearmetalk:/path zricethezav/gitleaks:latest detect  --source="/path" 
```
## Tips
### 証明書
https://www.ipentec.com/document/windows-iis-ssl-wild-card-domain-certificate-using-win-acme

### GitHub
https://github.com/dahlia1209/hearmetalk.git

### mov→WebMファイル変換
```
cd C:\src\hearmetalk\frontend\src\assets
ffmpeg -i speaking.mov -c:v libvpx-vp9 -b:v 0 -crf 30 -pix_fmt yuva420p speaking.webm 
```

### tamaranbai

## 素材提供者
クレジット表記：
みんちりえ（ https://min-chi.material.jp/ ）
素材：
C:\src\hearmetalk\frontend\src\assets\School_music_room_night_lights_ON.jpg
C:\src\hearmetalk\frontend\src\assets\School_bench_daytime.jpg

クレジット表記：
「本作品のキャラクターには株式会社Live2Dの著作物であるサンプルデータが株式会社Live2Dの定める規約に従って用いられています。本作品は制作者の完全な自己の裁量で制作されています。」
素材：
C:\src\hearmetalk\frontend\src\assets\hiyori_m05.webm
C:\src\hearmetalk\frontend\src\assets\hiyori_m08.webm
C:\src\hearmetalk\frontend\src\assets\hiyori_m09.webm
C:\src\hearmetalk\frontend\src\assets\hiyori_m10.webm
