# Azure / Entra ID Add‑On (Dry‑Run Examples)

**Goal:** Mirror the CSV‑based lifecycle (hire → change → terminate) with Entra ID examples.  
**Mode:** Safe **dry‑run**; replace placeholders and remove `-WhatIf` to execute for real.

---

## 0) Prereqs (run separately)
```powershell
# Install modules once (elevated PowerShell)
Install-Module Microsoft.Graph -Scope CurrentUser -Force

# Connect with the right scopes
Connect-MgGraph -Scopes "User.ReadWrite.All, Group.ReadWrite.All"
Select-MgProfile -Name "beta"   # or v1.0 if preferred
```
> If prompted, consent to the scopes in your tenant (needs admin).

---

## 1) HIRE (create user, add groups) — Dry‑Run
```powershell
# Variables (edit)
$DisplayName = "Julia Santos"
$UserPrincipalName = "julia.santos@example.onmicrosoft.com"
$MailNickname = "jsantos"
$Password = "P@ssw0rd!ChangeMe"
$Dept = "IT"
$Title = "Help Desk Tech"
$GroupNamesToAdd = @("IT-Helpdesk","ALL-Employees")  # match your CSV/JSON

# CREATE user (remove -WhatIf to execute)
New-MgUser `
  -DisplayName $DisplayName `
  -UserPrincipalName $UserPrincipalName `
  -MailNickname $MailNickname `
  -PasswordProfile @{ Password=$Password } `
  -AccountEnabled:$true `
  -Department $Dept -JobTitle $Title `
  -WhatIf

# ADD groups by name (remove -WhatIf to execute)
foreach ($g in $GroupNamesToAdd) {
  $group = Get-MgGroup -Filter "displayName eq '$g'" | Select-Object -First 1
  if ($group) {
    $user = Get-MgUser -Filter "userPrincipalName eq '$UserPrincipalName'" | Select-Object -First 1
    New-MgGroupMember -GroupId $group.Id -DirectoryObjectId $user.Id -WhatIf
  }
}
```

---

## 2) CHANGE (update title/department, adjust groups) — Dry‑Run
```powershell
# Variables (edit)
$UPN = "kate.morgan@example.onmicrosoft.com"
$NewTitle = "Sales Engineer"
$NewDept  = "Sales"
$AddGroups    = @("Sales-Engineers")
$RemoveGroups = @("Sales-Staff")

# UPDATE profile
Update-MgUser -UserId $UPN -JobTitle $NewTitle -Department $NewDept -WhatIf

# ADD/REMOVE groups
$user = Get-MgUser -UserId $UPN
foreach ($g in $AddGroups) {
  $grp = Get-MgGroup -Filter "displayName eq '$g'" | Select-Object -First 1
  if ($grp) { New-MgGroupMember -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf }
}
foreach ($g in $RemoveGroups) {
  $grp = Get-MgGroup -Filter "displayName eq '$g'" | Select-Object -First 1
  if ($grp) {
    # Find membership object and remove
    $mem = Get-MgGroupMember -GroupId $grp.Id | Where-Object Id -eq $user.Id
    if ($mem) { Remove-MgGroupMemberByRef -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf }
  }
}
```

---

## 3) TERMINATE (disable sign‑in, strip groups, move to “Leavers”) — Dry‑Run
```powershell
# Variables (edit)
$UPN = "david.mills@example.onmicrosoft.com"
$LeaversGroup = "Leavers"

# DISABLE sign-in
Update-MgUser -UserId $UPN -AccountEnabled:$false -WhatIf

# REMOVE all groups
$user = Get-MgUser -UserId $UPN
Get-MgUserMemberOf -UserId $user.Id | ForEach-Object {
  if ($_.AdditionalProperties.displayName) {
    $gid = $_.Id
    Remove-MgGroupMemberByRef -GroupId $gid -DirectoryObjectId $user.Id -WhatIf
  }
}

# ADD to Leavers
$grp = Get-MgGroup -Filter "displayName eq '$LeaversGroup'" | Select-Object -First 1
if ($grp) { New-MgGroupMember -GroupId $grp.Id -DirectoryObjectId $user.Id -WhatIf }
```

---

## Notes
- Keep **-WhatIf** while testing. Remove it to apply changes for real.
- Map your CSV values to UPNs and group names for a 1:1 mirror of your mock lifecycle.
- Use `Get-MgUser -Filter "displayName eq 'Name'"` if UPNs differ from your CSV emails.
