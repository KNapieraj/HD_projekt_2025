function New-AzureResources {
    param (
        # administratorLogin
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $administratorLogin,

        # administratorLoginPassword
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [securestring]
        $administratorLoginPassword,

        # location
        [Parameter(Mandatory = $true)]
        [string]
        $location = "westeurope",

        # Set TAG - owner name
        [Parameter(Mandatory = $true)]
        [string]
        $ProductOwner,

        # RG name
        [Parameter(Mandatory = $true)]
        [ValidatePattern('^$|^[-\w\.\(\)]{1,90}$')]
        [string]
        $resourceGroupName,

        # SQL server name
        [Parameter(Mandatory = $false)]
        [ValidateNotNullOrEmpty()]
        [string]
        $serverName,

        # SKU tier
        [Parameter(Mandatory = $false)]
        [ValidateSet('Basic', 'Standard')]
        [string]
        $SkuTier = 'Basic',

        # SKU name
        [Parameter(Mandatory = $false)]
        [ValidateSet('Basic', 'S0', 'S1')]
        [string]
        $SkuName = 'Basic',

        # sqlDBName
        [Parameter(Mandatory = $false)]
        [ValidateNotNullOrEmpty()]
        [string]
        $sqlDBName
    )

    New-AzDeployment `
        -Location $location `
        -TemplateFile "./main.bicep" `
        -TemplateParameterObject @{
            administratorLogin = $administratorLogin
            administratorLoginPassword = $administratorLoginPassword
            location = $location
            resourceGroupName = $resourceGroupName
            resourceGroupProductOwner = $ProductOwner
            serverName = $serverName
            skuTier = $skuTier
            skuName = $skuName
            sqlDBName = $sqlDBName

  }
}