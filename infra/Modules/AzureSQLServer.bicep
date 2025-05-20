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
