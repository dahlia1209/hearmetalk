param webAppName string = 'nakamura-app-03' // Generate unique String for web app name
param sku string = 'B2' // The SKU of App Service Plan
param location string = resourceGroup().location // Location for all resources
var appServicePlanName = toLower('appserviceplan-nakamura-app-01')
var webSiteName = toLower(webAppName)
var appSettingsJson = loadJsonContent('secret.json')
var linuxFxVersion='DOCKER|mcr.microsoft.com/azure-cognitive-services/speechservices/speech-to-text:4.5.0-amd64-ja-jp'

resource appServicePlan 'Microsoft.Web/serverfarms@2020-06-01' = {
  name: appServicePlanName
  location: location
  properties: {
    reserved: true
  }
  sku: {
    name: sku
  }
  kind: 'linux'
}

resource appService 'Microsoft.Web/sites@2020-06-01' = {
  name: webSiteName
  location: location
  kind: 'app,linux,container'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: appSettingsJson
    }
  }
}

