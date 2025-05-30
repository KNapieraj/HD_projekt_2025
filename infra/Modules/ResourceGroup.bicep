targetScope = 'subscription'

@description('Nazwa grupy zasobów.')
param resourceGroupName string

@description('Resource Naming convention')
param resourceGroupConventionName string = '${resourceGroupName}-rg'

@description('Allowed locations')
@allowed([
  'westeurope'
  'polandcentral'
])
param location string = 'westeurope'

@description('Tags for resource')
param resourceGroupProductOwner string

@description('Resource lock name')
param resourceLockName string = '${resourceGroupConventionName}-lock'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupConventionName
  location: location
  tags:{
    Product_Owner: resourceGroupProductOwner
  }
}
