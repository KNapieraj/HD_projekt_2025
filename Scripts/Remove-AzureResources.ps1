function Remove-resourceGroup {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName
    )

    Write-Host "INFO -- Usuwanie grupy zasobów '$resourceGroupName'..."
    Remove-AzResourceGroup -Name $resourceGroupName -Force -AsJob
}

function Remove-serverName {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]
        $serverName
    )

    Write-Host "INFO -- Usuwanie serwera SQL '$serverName'..."
    Remove-AzSqlServer -ResourceGroupName $resourceGroupName -ServerName $serverName -Force
}

function Remove-sqlDBName {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]
        $sqlDBName,

        [Parameter(Mandatory = $true)]
        [string]
        $serverName
    )

    Write-Host "INFO -- grupy '$serverName'..."
    Remove-AzSqlDatabase -ResourceGroupName $resourceGroupName -ServerName $serverName -DatabaseName $sqlDBName -Force
}