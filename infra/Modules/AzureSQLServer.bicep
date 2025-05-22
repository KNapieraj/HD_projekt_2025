@description('Nazwa serwera SQL.')
param serverName string

@description('Login administratora serwera SQL.')
param administratorLogin string

@description('Hasło administratora serwera SQL.')
@secure()
param administratorLoginPassword string

resource sqlServer 'Microsoft.Sql/servers@2022-05-01-preview' = {
  name: serverName
  location: resourceGroup().location
  properties: {
    administratorLogin: administratorLogin
    administratorLoginPassword: administratorLoginPassword
  }
}

resource firewallRule 'Microsoft.Sql/servers/firewallRules@2022-05-01-preview' = {
  name: 'AllowClientIP'
  parent: sqlServer
  properties: {
    startIpAddress: '80.253.213.1'
    endIpAddress: '80.253.213.254'
  }
}

resource firewallRule 'Microsoft.Sql/servers/firewallRules@2022-05-01-preview' = {
  name: 'AllowClientIP'
  parent: sqlServer
  properties: {
    startIpAddress: '147.161.251.1'
    endIpAddress: '147.161.251.254'
  }
}
