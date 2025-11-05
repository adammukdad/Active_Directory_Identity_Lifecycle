# Microsoft Graph — Raw HTTP Examples (curl)

## 0) Token (run separately)
```bash
# Acquire a token via Azure CLI
TOKEN=$(az account get-access-token --resource https://graph.microsoft.com --query accessToken -o tsv)
```

## 1) HIRE (create user)
```bash
curl -s -X POST https://graph.microsoft.com/v1.0/users  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  -d '{
   "accountEnabled": true,
   "displayName": "Julia Santos",
   "userPrincipalName": "julia.santos@example.onmicrosoft.com",
   "mailNickname": "jsantos",
   "passwordProfile": {"forceChangePasswordNextSignIn": true, "password": "P@ssw0rd!ChangeMe"},
   "department": "IT",
   "jobTitle": "Help Desk Tech"
 }' | jq
```

## 2) CHANGE (update title/department)
```bash
UPN="kate.morgan@example.onmicrosoft.com"
curl -s -X PATCH "https://graph.microsoft.com/v1.0/users/$UPN"  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  -d '{ "jobTitle": "Sales Engineer", "department": "Sales" }' | jq
```

## 3) Group membership (add/remove)
```bash
UPN="kate.morgan@example.onmicrosoft.com"
ADD_GROUP="Sales-Engineers"
REMOVE_GROUP="Sales-Staff"

USER_ID=$(curl -s -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/users/$UPN" | jq -r .id)
ADD_ID=$(curl -s -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/groups?\$filter=displayName eq '$ADD_GROUP'" | jq -r '.value[0].id')
REM_ID=$(curl -s -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/groups?\$filter=displayName eq '$REMOVE_GROUP'" | jq -r '.value[0].id')

# Add member
curl -s -X POST "https://graph.microsoft.com/v1.0/groups/$ADD_ID/members/\$ref"  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  -d "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/$USER_ID\"}" | jq

# Remove member
curl -s -X DELETE "https://graph.microsoft.com/v1.0/groups/$REM_ID/members/$USER_ID/\$ref"  -H "Authorization: Bearer $TOKEN"
```

## 4) TERMINATE (disable, add to Leavers)
```bash
UPN="david.mills@example.onmicrosoft.com"
LEAVERS="Leavers"
LID=$(curl -s -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/groups?\$filter=displayName eq '$LEAVERS'" | jq -r '.value[0].id')

# Disable
curl -s -X PATCH "https://graph.microsoft.com/v1.0/users/$UPN"  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  -d '{ "accountEnabled": false }' | jq

# Add to Leavers
UID=$(curl -s -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/users/$UPN" | jq -r .id)
curl -s -X POST "https://graph.microsoft.com/v1.0/groups/$LID/members/\$ref"  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"  -d "{\"@odata.id\": \"https://graph.microsoft.com/v1.0/directoryObjects/$UID\"}" | jq
```

> These calls execute live. Test in a dev tenant only.
