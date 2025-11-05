# Entra / Azure CLI with Microsoft Graph (Dry‑Run Style)

> The dedicated `entra` CLI is evolving; these examples use `az rest` to hit Microsoft Graph directly.
> Replace placeholders, then remove the `# DRY‑RUN` comments to execute.

## 0) Login (run separately)
```bash
az login
az account show
```

## 1) HIRE (create user)
```bash
# DRY-RUN: review payload
cat > user_create.json <<'JSON'
{
  "accountEnabled": true,
  "displayName": "Julia Santos",
  "userPrincipalName": "julia.santos@example.onmicrosoft.com",
  "mailNickname": "jsantos",
  "passwordProfile": { "forceChangePasswordNextSignIn": true, "password": "P@ssw0rd!ChangeMe" },
  "department": "IT",
  "jobTitle": "Help Desk Tech"
}
JSON

# Execute (remove echo to run)
echo az rest --method POST --uri https://graph.microsoft.com/v1.0/users --body @user_create.json
```

## 2) CHANGE (update title/department)
```bash
UPN="kate.morgan@example.onmicrosoft.com"

cat > user_update.json <<'JSON'
{ "jobTitle": "Sales Engineer", "department": "Sales" }
JSON

# Execute
echo az rest --method PATCH --uri https://graph.microsoft.com/v1.0/users/$UPN --body @user_update.json
```

## 3) Group membership (add/remove)
```bash
UPN="kate.morgan@example.onmicrosoft.com"
ADD_GROUP="Sales-Engineers"
REMOVE_GROUP="Sales-Staff"

# Resolve IDs
USER_ID=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/users/$UPN" --query id -o tsv)
ADD_ID=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '$ADD_GROUP'" --query "value[0].id" -o tsv)
REM_ID=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '$REMOVE_GROUP'" --query "value[0].id" -o tsv)

# Add member
echo az rest --method POST --uri "https://graph.microsoft.com/v1.0/groups/$ADD_ID/members/\$ref" --body "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/$USER_ID\"}"

# Remove member
echo az rest --method DELETE --uri "https://graph.microsoft.com/v1.0/groups/$REM_ID/members/$USER_ID/\$ref"
```

## 4) TERMINATE (disable, strip groups, add to Leavers)
```bash
UPN="david.mills@example.onmicrosoft.com"
LEAVERS="Leavers"

# Disable
echo az rest --method PATCH --uri https://graph.microsoft.com/v1.0/users/$UPN --body '{ "accountEnabled": false }'

# Add to Leavers
LID=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '$LEAVERS'" --query "value[0].id" -o tsv)
UID=$(az rest --method GET --uri "https://graph.microsoft.com/v1.0/users/$UPN" --query id -o tsv)
echo az rest --method POST --uri "https://graph.microsoft.com/v1.0/groups/$LID/members/\$ref" --body "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/$UID\"}"
```

> Remove the leading `echo` commands to execute for real.
