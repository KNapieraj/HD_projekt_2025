function Remove-ResourceGroup {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName
    )

    # Sprawdzenie, czy grupa zasobów istnieje
    $resourceGroup = Get-AzResourceGroup -Name $resourceGroupName -ErrorAction SilentlyContinue

    if ($null -eq $resourceGroup) {
        Write-Host "WARN -- Grupa zasobów '$resourceGroupName' nie istnieje."
    }
    else {
        Write-Host "INFO -- Usuwanie grupy zasobów '$resourceGroupName'..."
        Remove-AzResourceGroup -Name $resourceGroupName -Force -AsJob
    }
}

function Remove-ServerName {
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $resourceGroupName,

        [Parameter(Mandatory = $true)]
        [string]
        $serverName
    )

    # Sprawdzenie, czy serwer SQL istnieje
    $sqlServer = Get-AzSqlServer -ResourceGroupName $resourceGroupName -ServerName $serverName -ErrorAction SilentlyContinue

    if ($null -eq $sqlServer) {
        Write-Host "WARN -- Serwer SQL '$serverName' nie istnieje w grupie zasobów '$resourceGroupName'."
    }
    else {
        Write-Host "INFO -- Usuwanie SQL Server '$serverName'..."
        Remove-AzSqlServer -ResourceGroupName $resourceGroupName -ServerName $serverName -Force
    }
}

function Remove-SqlDBName {
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

    # Sprawdzenie, czy baza danych istnieje
    $sqlDatabase = Get-AzSqlDatabase -ResourceGroupName $resourceGroupName -ServerName $serverName -DatabaseName $sqlDBName -ErrorAction SilentlyContinue

    if ($null -eq $sqlDatabase) {
        Write-Host "WARN -- Baza danych '$sqlDBName' nie istnieje na serwerze '$serverName' w grupie zasobów '$resourceGroupName'."
    }
    else {
        Write-Host "INFO -- Usuwanie SQL Database '$sqlDBName'..."
        Remove-AzSqlDatabase -ResourceGroupName $resourceGroupName -ServerName $serverName -DatabaseName $sqlDBName -Force
    }
}
