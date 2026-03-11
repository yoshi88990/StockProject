$path = "$env:APPDATA\Code\User\settings.json"
$json = Get-Content $path -Raw | ConvertFrom-Json
$json.'workbench.colorTheme' = 'Default Light Modern'
$json | ConvertTo-Json | Set-Content $path -Force
