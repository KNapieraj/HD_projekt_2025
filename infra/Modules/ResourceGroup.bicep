targetScope='subscription'

@description('Resource Naming convention')
param resourceGroupConventionName string

@description('Allowed locations')
@allowed([
  'westeurope'
  'polandcentral'
])
param resourceGroupLocation string = 'westeurope'

@description('Tags for resource')
param resourceGroupProductOwner string

resource newRG 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupConventionName
  location: resourceGroupLocation
  tags:{
    Product_Owner: resourceGroupProductOwner
  }
}
