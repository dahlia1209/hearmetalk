function replaceAksClientId {
    # 置換する値を設定
    $IDENTITY_CLIENT_ID=$(az aks show -g nakamura-rg-aks -n nakamura-aks --query addonProfiles.azureKeyvaultSecretsProvider.identity.clientId -o tsv)
    
    # ファイルパス
    $filePath = "C:\src\hearmetalk\kubernetes\SecretProviderClass.yaml"
    
    # ファイル内容を読み込む
    $fileContent = Get-Content $filePath
    
    # 文字列を置換
    $replacedContent = $fileContent -replace 'userAssignedIdentityID: .+', "userAssignedIdentityID: $IDENTITY_CLIENT_ID"
    
    # 結果をファイルに上書き保存
    $replacedContent | Set-Content $filePath
}

function replaceIngressWhitelistIp{
    # ファイルパス
    $filePathList = ("C:\src\hearmetalk\kubernetes\neural-text-to-speech-en-ingress.yaml","C:\src\hearmetalk\kubernetes\neural-text-to-speech-ingress.yaml","C:\src\hearmetalk\kubernetes\openaicompletions-ingress.yaml","C:\src\hearmetalk\kubernetes\speech-to-text-ingress.yaml")
    $myGlobalIp=(ConvertFrom-Json (Invoke-WebRequest httpbin.org/ip).content).origin
    $ubuntuIp=Get-UbuntuIP

    # ファイル内容を読み込んで置換処理
    foreach ($filePath in $filePathList) {
        $fileContent = Get-Content $filePath

        $replacedContent = $fileContent -replace 'nginx\.ingress\.kubernetes\.io/whitelist-source-range: .+', "nginx.ingress.kubernetes.io/whitelist-source-range: $myGlobalIp/32,$ubuntuIp/32"
        $replacedContent | Set-Content $filePath
    }
}

function replaceServiceWhitelistIp{
    # ファイルパス
    $filePathList = ("C:\src\hearmetalk\kubernetes\ubuntu-service.yaml")
    $myGlobalIp=(ConvertFrom-Json (Invoke-WebRequest httpbin.org/ip).content).origin
    
    # ファイル内容を読み込んで置換処理
    foreach ($filePath in $filePathList) {
        $fileContent = Get-Content $filePath
        $replacedContent = $fileContent -replace '- .+ #myGlobalIp', "- $myGlobalIp/32 #myGlobalIp"
        $replacedContent | Set-Content $filePath
    }
}

function replaceServiceWhitelistIp{
    # ファイルパス
    $filePathList = ("C:\src\hearmetalk\kubernetes\ubuntu-service.yaml")
    
    # ファイル内容を読み込んで置換処理
    foreach ($filePath in $filePathList) {
        $fileContent = Get-Content $filePath
        $myGlobalIp=(ConvertFrom-Json (Invoke-WebRequest httpbin.org/ip).content).origin
        $replacedContent = $fileContent -replace '- .+ #myGlobalIp', "- $myGlobalIp/32 #myGlobalIp"
        $replacedContent | Set-Content $filePath
    }
}

function Get-UbuntuIP  {
    param (
        [string]$appName="ubuntu-xfce-desktop",
        [int]$maxRetries = 5,
        [int]$retryInterval = 10
    )

    $tryCount = 0
    $command = { kubectl get pods -l app=$appName -o jsonpath='{.items[0].status.podIP}' }

    do {
        try {
            $output = & $command
            if (-not [string]::IsNullOrWhiteSpace($output)) {
                return $output
            } else {
                # Write-Output "External IP has not been assigned yet. Retrying..."
                throw "IP not assigned yet"
            }
        } catch {
            # Write-Output "Attempt #$($tryCount + 1) failed: $_"
            if ($tryCount -lt $maxRetries - 1) {
                Start-Sleep -Seconds $retryInterval
            }
        }
        $tryCount++
    } while ($tryCount -lt $maxRetries)

    Write-Error "Command execution reached the maximum number of retries ($maxRetries). The operation failed."
}

