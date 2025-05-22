function resourceGroupName {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName
    )

    Write-Host "INFO -- Usuwanie bazy danych '$sqlDBName' z serwera '$serverName'..."
    Remove-AzSqlDatabase -ResourceGroupName $resourceGroupName -ServerName $serverName -DatabaseName $sqlDBName -Force
}

function Remove-serverName {
    param (
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
        $sqlDBName
    )

    Write-Host "INFO -- Usuwanie grupy zasobów '$resourceGroupName'..."
    Remove-AzResourceGroup -Name $resourceGroupName -Force -AsJob
}