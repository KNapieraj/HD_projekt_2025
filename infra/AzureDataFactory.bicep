@description('Nazwa dla Azure Data Factory')
param dataFactoryName string

@description('Tagi dla zasobu')
param resourceProductOwner string

@description('Nazwa grupy zasobów')
param resourceGroupConventionName string

// @description('Nazwa dla resource locka')
// param resourceLockName string = '${dataFactoryName}-lock'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' existing = {
  name: resourceGroupConventionName
}

resource dataFactory 'Microsoft.DataFactory/factories@2022-09-01' = {
  name: dataFactoryName
  location: resourceGroup.location
  tags: {
    Product_Owner: resourceProductOwner
  }
}

// resource lock 'Microsoft.Authorization/locks@2022-09-01' = {
//   name: resourceLockName
//   scope: dataFactory
//   properties: {
//     level: 'CanNotDelete'
//   }
// }

// output dataFactoryId string = dataFactory.id
