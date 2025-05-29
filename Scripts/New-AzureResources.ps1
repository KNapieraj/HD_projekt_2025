function New-ResourceGroup {
    param (
        # location
        [Parameter(Mandatory = $false)]
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
        $resourceGroupName
    )

    New-AzDeployment `
        -Location $location `
        -TemplateFile "./infra/ResourceGroup.bicep" `
        -TemplateParameterObject @{
            location = $location
            resourceGroupName = $resourceGroupName
            resourceGroupProductOwner = $ProductOwner
        }
}

function New-AzureServerSQL {
    param (
        # administratorLogin
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $administratorLogin,

        # administratorLoginPassword
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $administratorLoginPassword,

        # Set TAG - owner name
        [Parameter(Mandatory = $true)]
        [string]
        $ProductOwner,

        # RG name
        [Parameter(Mandatory = $true)]
        [ValidatePattern('^$|^[-\w\.\(\)-]{1,90}$')]
        [string]
        $resourceGroupConvetionName,

        # SQL server name
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $sqlServerName
    )

    New-AzDeployment `
        -Location $location `
        -TemplateFile "./infra/AzureSQLServer.bicep" `
        -TemplateParameterObject @{
            administratorLogin = $administratorLogin
            administratorLoginPassword = $administratorLoginPassword
            resourceGroupConvetionName = $resourceGroupConvetionName
            resourceGroupProductOwner = $ProductOwner
            sqlServerName = $sqlServerName
        }

}

function New-AzureDatabaseSQL {
    param (
        # Set TAG - owner name
        [Parameter(Mandatory = $true)]
        [string]
        $ProductOwner,

        # RG name
        [Parameter(Mandatory = $true)]
        [ValidatePattern('^$|^[-\w\.\(\)-]{1,90}$')]
        [string]
        $resourceGroupConvetionName,

        # SKUname
        [Parameter(Mandatory = $true)]
        [ValidateSet('Basic', 'S0', 'S1')]
        [string]
        $SkuName,

        # SKUtier
        [Parameter(Mandatory = $true)]
        [ValidateSet('Basic', 'Standard')]
        [string]
        $SkuTier,

        # sqlDBName
        [Parameter(Mandatory = $false)]
        [ValidateNotNullOrEmpty()]
        [string]
        $sqlDBName,

        # SQL server name
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $sqlServerName
    )

    New-AzDeployment `
        -Location $location `
        -TemplateFile "./infra/main.bicep" `
        -TemplateParameterObject @{
            resourceGroupConventionName = $resourceGroupConvetionName
            resourceProductOwner = $ProductOwner
            skuTier = $skuTier
            skuName = $skuName
            sqlDBName = $sqlDBName
            sqlServerName = $serverName
        }
    }

function New-AzureDataFactory {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $dataFactoryName,

        # Set TAG - owner name
        [Parameter(Mandatory = $true)]
        [string]
        $ProductOwner,

        # RG name
        [Parameter(Mandatory = $true)]
        [ValidatePattern('^$|^[-\w\.\(\)-]{1,90}$')]
        [string]
        $resourceGroupName
    )

    New-AzDeployment `
        -Location $location `
        -TemplateFile "./infra/ResourceGroup.bicep" `
        -TemplateParameterObject @{
            dataFactoryName = $dataFactoryName
            resourceGroupConventionName = $resourceGroupName
            resourceProductOwner = $ProductOwner
        }
}