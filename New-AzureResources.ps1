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
        [string]
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
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $serverName,

        # SKU tier
        [Parameter(Mandatory = $true)]
        [ValidateSet('Basic', 'Standard')]
        [string]
        $SkuTier,

        # SKU name
        [Parameter(Mandatory = $true)]
        [ValidateSet('Basic', 'S0', 'S1')]
        [string]
        $SkuName,

        # sqlDBName
        [Parameter(Mandatory = $false)]
        [ValidateNotNullOrEmpty()]
        [string]
        $sqlDBName
    )

    # # PowerShell
    # $securePassword = ConvertTo-SecureString $administratorLoginPassword -AsPlainText -Force
    # New-AzDeployment `
    #     -Location $location `
    #     -TemplateFile "./infra/main.bicep" `
    #     -TemplateParameterObject @{
    #         administratorLogin = $administratorLogin
    #         administratorLoginPassword = $securePassword
    #         location = $location
    #         resourceGroupName = $resourceGroupName
    #         resourceGroupProductOwner = $ProductOwner
    #         serverName = $serverName
    #         skuTier = $skuTier
    #         skuName = $skuName
    #         sqlDBName = $sqlDBName
    #     }

    # CLI
    az deployment sub create \
        --location "$location" \
        --template-file "./infra/main.bicep" \
        --parameters \
            administratorLogin="$administratorLogin" \
            administratorLoginPassword="$administratorLoginPassword" \
            location="$location" \
            resourceGroupName="$resourceGroupName" \
            resourceGroupProductOwner="$ProductOwner" \
            serverName="$serverName" \
            skuTier="$skuTier" \
            skuName="$skuName" \
            sqlDBName="$sqlDBName"


}
