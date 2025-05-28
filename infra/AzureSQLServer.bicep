@description('Login administratora serwera SQL.')
param administratorLogin string

@description('Hasło administratora serwera SQL.')
@secure()
param administratorLoginPassword string

@description('Resource group full name')
param resourceGroupConventionName string

@description('Resource lock name')
param resourceLockName = '${serverName}-lock'

@description('Tags for resource')
param resourceProductOwner string

@description('Nazwa serwera SQL.')
param serverName string

resource sqlServer 'Microsoft.Sql/servers@2022-05-01-preview' = {
  name: serverName
  scope: resourceGroup(resourceGroupConventionName)
  location: resourceGroup(resourceGroupConventionName).location
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

resource lock 'Microsoft.Authorization/locks@2022-09-01' = {
  name: resourceLockName
  scope: sqlServer
  properties: {
    level: 'CanNotDelete'
  }
}
