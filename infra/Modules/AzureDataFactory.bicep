@description('Nazwa dla Azure Data Factory')
param dataFactoryName string

@description('Tagi dla zasobu')
param resourceProductOwner string

resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: dataFactoryName
  location: resourceGroup().location
  properties: {
    repoConfiguration: {
      type: 'FactoryGitHubConfiguration'
      accountName: 'KNapieraj'
      repositoryName: 'HD_projekt_2025'
      collaborationBranch: 'master'
      rootFolder: '/'
    }
  }

  tags: {
    Product_Owner: resourceProductOwner
  }
}
