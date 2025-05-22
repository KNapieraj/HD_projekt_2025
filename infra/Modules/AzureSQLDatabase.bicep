@description('Pełna nazwa zasobu serwera SQL, np. format: my-sql-server')
param sqlServerName string

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
}
