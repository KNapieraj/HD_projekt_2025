@description('Nazwa dla Azure Data Factory')
param dataFactoryName string

@description('Tagi dla zasobu')
param resourceProductOwner string

resource dataFactory 'Microsoft.DataFactory/factories@2022-09-01' = {
  name: dataFactoryName
  location: resourceGroup().location
  tags: {
    Product_Owner: resourceProductOwner
  }
}
