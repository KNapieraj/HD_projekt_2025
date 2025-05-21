function Remove-AzureResources {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]
        $serverName,

        [Parameter(Mandatory = $true)]
        [string]
        $sqlDBName
    )

    Write-Host "INFO -- Usuwanie bazy danych '$sqlDBName' z serwera '$serverName'..."
    Remove-AzSqlDatabase -ResourceGroupName $resourceGroupName -ServerName $serverName -DatabaseName $sqlDBName -Force

    Write-Host "INFO -- Usuwanie serwera SQL '$serverName'..."
    Remove-AzSqlServer -ResourceGroupName $resourceGroupName -ServerName $serverName -Force

    Write-Host "INFO -- Usuwanie grupy zasobów '$resourceGroupName'..."
    Remove-AzResourceGroup -Name $resourceGroupName -Force -AsJob
}
