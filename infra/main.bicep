targetScope = 'subscription'

@description('Nazwa dla Azure Data Factory')
param azureDataFactoryName string

@description('Nazwa grupy zasobów.')
param resourceGroupName string

@description('Resource Naming convention')
param resourceGroupConventionName string = '${resourceGroupName}-rg'

@description('Właściciel zasobu')
param ProductOwner string

@description('Nazwa serwera SQL.')
param serverName string

@description('Login administratora SQL.')
param administratorLogin string

@description('Hasło administratora SQL.')
@secure()
param administratorLoginPassword string

@description('Location')
param location string = 'westeurope'

@description('Nazwa bazy danych.')
param sqlDBName string

@description('SKU - warstwa cenowa.')
param skuTier string = 'Basic'

@description('SKU - nazwa SKU.')
param skuName string = 'Basic'

// Moduł: Resource Group (opcjonalnie, jeśli nie tworzysz RG osobno)
module rgModule './Modules/ResourceGroup.bicep' = {
  name: 'deployResourceGroup'
  scope: subscription()
  params: {
    location: location
    resourceGroupConventionName: resourceGroupConventionName
    resourceGroupProductOwner: ProductOwner
  }
}

// Moduł: SQL Server
module sqlServerModule './Modules/AzureSQLServer.bicep' = {
  name: 'deploySqlServer'
  scope: resourceGroup(resourceGroupConventionName)
  params: {
    serverName: serverName
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
    resourceProductOwner:ProductOwner
  }
  dependsOn: [
    rgModule
  ]
}

// Moduł: SQL Database
module sqlDatabaseModule './Modules/AzureSQLDatabase.bicep' = {
  name: 'deploySqlDatabase'
  scope: resourceGroup(resourceGroupConventionName)
  params: {
    resourceProductOwner: ProductOwner
    sqlServerName: serverName
    sqlDBName: sqlDBName
    skuTier: skuTier
    skuName: skuName
  }
  dependsOn: [
    sqlServerModule
  ]
}

// Moduł: Azure Data Factory
module azureDataFactoryModule './Modules/AzureDataFactory.bicep' = {
  name: 'deployAzureDataFactory'
  scope: resourceGroup(resourceGroupConventionName)
  params: {
    dataFactoryName: azureDataFactoryName
    resourceGroupConventionName: ProductOwner
    resourceProductOwner: skuTier
  }
  dependsOn: [
    sqlDatabaseModule
  ]
}
