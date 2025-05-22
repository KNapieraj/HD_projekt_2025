param (
    [Parameter(Mandatory = $true)]
    [string] $ServicePrincipalJson
)

$creds = $ServicePrincipalJson | ConvertFrom-Json

$securePassword = ConvertTo-SecureString $creds.clientSecret -AsPlainText -Force
$psCredential = New-Object System.Management.Automation.PSCredential ($creds.clientId, $securePassword)

Connect-AzAccount `
  -ServicePrincipal `
  -Credential $psCredential `
  -TenantId $creds.tenantId `
  -SubscriptionId $creds.subscriptionId
