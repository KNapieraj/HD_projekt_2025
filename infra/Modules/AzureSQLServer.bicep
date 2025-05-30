@description('Login administratora serwera SQL.')
param administratorLogin string

@description('Hasło administratora serwera SQL.')
@secure()
param administratorLoginPassword string

@description('Resource group full name')
param resourceGroupConventionName string

// @description('Resource lock name')
// param resourceLockName string = '${sqlServerName}-lock'

@description('Tags for resource')
param resourceProductOwner string

@description('Allowed locations')
@allowed([
  'westeurope'
  'polandcentral'
])
param location string = 'westeurope'

@description('Nazwa serwera SQL.')
param sqlServerName string

resource sqlServer 'Microsoft.Sql/servers@2022-05-01-preview' = {
  name: serverName
  location: resourceGroup().location
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
  }
  tags:{
    Product_Owner: resourceProductOwner
  }
}

resource firewallRule 'Microsoft.Sql/servers/firewallRules@2022-05-01-preview' = {
  name: 'Laptop'
  parent: sqlServer
  properties: {
    startIpAddress: '80.253.213.1'
    endIpAddress: '80.253.213.254'
  }
}

// resource lock 'Microsoft.Authorization/locks@2022-09-01' = {
//   name: resourceLockName
//   scope: sqlServer
//   properties: {
//     level: 'CanNotDelete'
//   }
// }
