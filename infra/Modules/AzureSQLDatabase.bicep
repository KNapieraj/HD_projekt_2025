@description('Tags for resource')
param resourceProductOwner string

// @description('Resource lock name')
// param resourceLockName string = '${sqlDBName}-lock'

@description('Nazwa bazy danych SQL.')
param sqlDBName string

@description('SKU - nazwa warstwy cenowej, np. Basic, Standard, Premium.')
param skuTier string

@description('SKU - nazwa SKU')
@allowed([
  'Basic'
  'S0'
  'S1'
])
param skuName string

resource sqlDB 'Microsoft.Sql/servers/databases@2022-05-01-preview' = {
  name: '${sqlServerName}/${sqlDBName}'
  location: resourceGroup().location
  sku: {
    name: skuName
    tier: skuTier
  }
  tags:{
    Product_Owner: resourceProductOwner
  }
}

// resource lock 'Microsoft.Authorization/locks@2022-09-01' = {
//   name: resourceLockName
//   scope: sqlDB
//   properties: {
//     level: 'CanNotDelete'
//   }
// }
