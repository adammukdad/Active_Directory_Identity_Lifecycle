<# Entra ID PowerShell Examples (Dry-Run)
Use with README.md in the same folder. Remove -WhatIf to apply changes.
#>

# Connect (run once per session)
# Connect-MgGraph -Scopes "User.ReadWrite.All, Group.ReadWrite.All"
# Select-MgProfile -Name "beta"

# --- HIRE ------------------------------------------------------
# Example:
# New-MgUser -DisplayName "Julia Santos" -UserPrincipalName "julia.santos@example.onmicrosoft.com" `
#   -MailNickname "jsantos" -PasswordProfile @{ Password="P@ssw0rd!ChangeMe" } -AccountEnabled:$true `
#   -Department "IT" -JobTitle "Help Desk Tech" -WhatIf

# --- CHANGE ----------------------------------------------------
# $UPN = "kate.morgan@example.onmicrosoft.com"
# Update-MgUser -UserId $UPN -JobTitle "Sales Engineer" -Department "Sales" -WhatIf
# $Add = @("Sales-Engineers"); $Remove=@("Sales-Staff")
# $user = Get-MgUser -UserId $UPN
# foreach ($g in $Add)   { $grp=Get-MgGroup -Filter "displayName eq '$g'"; if($grp){ New-MgGroupMember -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf } }
# foreach ($g in $Remove){ $grp=Get-MgGroup -Filter "displayName eq '$g'"; if($grp){ Remove-MgGroupMemberByRef -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf } }

# --- TERMINATE -------------------------------------------------
# $UPN = "david.mills@example.onmicrosoft.com"
# Update-MgUser -UserId $UPN -AccountEnabled:$false -WhatIf
# $Leavers="Leavers"
# $user = Get-MgUser -UserId $UPN
# $grp = Get-MgGroup -Filter "displayName eq '$Leavers'" | Select-Object -First 1
# if ($grp) { New-MgGroupMember -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf }
