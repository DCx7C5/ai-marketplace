# Daily Key Rotation - Required Secrets Setup Guide

## Overview

This guide details all secrets required to configure the daily key rotation workflow.

## Required Secrets by Category

### 1. GitHub App Credentials (Required)

These credentials enable the workflow to create temporary tokens for managing secrets.

#### `GITHUB_APP_ID`
```yaml
Type: Number (string representation)
Scope: Environment (production)
Purpose: GitHub App application ID
Source: GitHub Settings → Developer settings → GitHub Apps → Your App → App ID
Example: "123456"
Sensitivity: PUBLIC (displayed in app settings)
```

**How to obtain:**
1. Go to GitHub → Settings → Developer settings → GitHub Apps
2. Create new GitHub App or use existing
3. Copy the App ID (numeric value at top of app page)
4. Set as secret: `gh secret set GITHUB_APP_ID --env production --body "123456"`

#### `GITHUB_APP_PRIVATE_KEY`
```yaml
Type: PEM-formatted private key
Scope: Environment (production)
Purpose: Authenticates GitHub App for secret management
Source: GitHub Settings → Developer settings → GitHub Apps → Your App → Generate private key
Example: |
  -----BEGIN RSA PRIVATE KEY-----
  MIIEpAIBAAKCAQEA1234567890...
  -----END RSA PRIVATE KEY-----
Sensitivity: HIGHLY SENSITIVE (keep secure)
```

**How to obtain:**
1. Go to GitHub App settings
2. Scroll to "Private keys" section
3. Click "Generate a private key"
4. GitHub creates and downloads a `.pem` file
5. Set as secret: `gh secret set GITHUB_APP_PRIVATE_KEY --env production < /path/to/private-key.pem`

**Required App Permissions:**
- Actions: `read`, `write`
- Secrets: `read`, `write`
- Environments: `read`, `write`
- Organization secrets: `read`, `write` (if managing org-level secrets)

### 2. Key Suffix Secrets (Initial + Managed)

#### `KEY_SUFFIX_DAILY`
```yaml
Type: String (8 alphanumeric uppercase characters)
Scope: Environment (production)
Purpose: Current key identifier suffix
Source: Generated initially, auto-rotated daily
Example: "ABC12345"
Sensitivity: MEDIUM (non-secret identifier)
Auto-updated: YES (daily)
```

**Initial setup:**
```bash
# Generate initial suffix
SUFFIX=$(openssl rand -base64 128 | tr "[:lower:]" "[:upper:]" | tr -d '/+=' | head -c 8)
echo "Initial suffix: $SUFFIX"

# Set initial secret
gh secret set KEY_SUFFIX_DAILY --env production --body "$SUFFIX"
```

#### `KEY_SUFFIX_DAILY_OLD`
```yaml
Type: String (8 alphanumeric uppercase characters)
Scope: Environment (production)
Purpose: Previous day's key suffix (for cleanup)
Source: Auto-managed by rotation workflow
Example: "INITKEY0"
Sensitivity: MEDIUM (non-secret identifier)
Auto-updated: YES (daily)
Initial-value: "XXXXXXXX" (placeholder)
```

**Initial setup:**
```bash
gh secret set KEY_SUFFIX_DAILY_OLD --env production --body "XXXXXXXX"
```

### 3. API Key Secrets (Rotated Daily)

#### `API_KEY_DAILY_[SUFFIX]`
```yaml
Type: String (64 hexadecimal characters = 32 bytes)
Scope: Environment (production)
Purpose: Primary API key for current day
Source: Generated daily by rotation workflow
Example: "a1b2c3d4e5f6a7b8c9d0a1b2c3d4e5f6a7b8c9d0a1b2c3d4e5f6a7b8c9d0"
Naming: API_KEY_DAILY_ABC12345 (where ABC12345 is current KEY_SUFFIX_DAILY)
Sensitivity: HIGHLY SENSITIVE (secret credential)
Auto-updated: YES (daily)
```

**Initial setup (before first rotation):**
```bash
# Generate initial API key
API_KEY=$(openssl rand -hex 32)
SUFFIX=$(gh secret view KEY_SUFFIX_DAILY --env production)

# Set secret with current suffix
gh secret set "API_KEY_DAILY_${SUFFIX}" --env production --body "$API_KEY"
```

#### `API_KEY_SECONDARY_[SUFFIX]`
```yaml
Type: String (64 hexadecimal characters = 32 bytes)
Scope: Environment (production)
Purpose: Secondary/backup API key for current day
Source: Generated daily by rotation workflow
Example: "f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9"
Naming: API_KEY_SECONDARY_ABC12345 (where ABC12345 is current KEY_SUFFIX_DAILY)
Sensitivity: HIGHLY SENSITIVE (secret credential)
Auto-updated: YES (daily)
```

**Initial setup:**
```bash
# Generate initial secondary API key
API_KEY_SECONDARY=$(openssl rand -hex 32)
SUFFIX=$(gh secret view KEY_SUFFIX_DAILY --env production)

# Set secret with current suffix
gh secret set "API_KEY_SECONDARY_${SUFFIX}" --env production --body "$API_KEY_SECONDARY"
```

### 4. Signature Key Secrets (Rotated Daily)

#### `SIGN_KEY_DAILY_[SUFFIX]`
```yaml
Type: String (base64-encoded 32 bytes)
Scope: Environment (production)
Purpose: Primary EdDSA/Ed25519 signature key for current day
Source: Generated daily by rotation workflow
Example: "TzDsRmK9LxWqP2hJvN8aB3sC5dE7fG9hI0jK2lM4n6O8p/"
Naming: SIGN_KEY_DAILY_ABC12345 (where ABC12345 is current KEY_SUFFIX_DAILY)
Sensitivity: HIGHLY SENSITIVE (cryptographic key)
Auto-updated: YES (daily)
```

**Initial setup:**
```bash
# Generate initial signature key
SIGN_KEY=$(openssl rand -base64 32)
SUFFIX=$(gh secret view KEY_SUFFIX_DAILY --env production)

# Set secret with current suffix
gh secret set "SIGN_KEY_DAILY_${SUFFIX}" --env production --body "$SIGN_KEY"
```

#### `SIGN_KEY_DAILY_[SUFFIX]_SECONDARY`
```yaml
Type: String (base64-encoded 32 bytes)
Scope: Environment (production)
Purpose: Secondary EdDSA/Ed25519 signature key for current day
Source: Generated daily by rotation workflow
Example: "pQ9oR1sT3uV5wX7yZ9aB1cD3eF5gH7iJ9kL1mN3oP5qR7sT9u/"
Naming: SIGN_KEY_DAILY_ABC12345_SECONDARY (where ABC12345 is current KEY_SUFFIX_DAILY)
Sensitivity: HIGHLY SENSITIVE (cryptographic key)
Auto-updated: YES (daily)
```

**Initial setup:**
```bash
# Generate initial secondary signature key
SIGN_KEY_SECONDARY=$(openssl rand -base64 32)
SUFFIX=$(gh secret view KEY_SUFFIX_DAILY --env production)

# Set secret with current suffix
gh secret set "SIGN_KEY_DAILY_${SUFFIX}_SECONDARY" --env production --body "$SIGN_KEY_SECONDARY"
```

### 5. Backup Secrets (Auto-Managed)

#### `BACKUP_API_KEYS_DAILY`
```yaml
Type: String (CSV or delimited list)
Scope: Environment (production)
Purpose: Backup of API keys before rotation/deletion
Source: Auto-created by rotation workflow
Format: "KEY_NAME,KEY_VALUE\nKEY_NAME2,KEY_VALUE2"
Sensitivity: HIGHLY SENSITIVE (contains old credentials)
Auto-updated: YES (daily before deletion)
Retention: Keep for audit trail (review monthly)
```

#### `BACKUP_KEYS_DAILY`
```yaml
Type: String (delimited list or JSON)
Scope: Environment (production)
Purpose: General backup of all rotated keys
Source: Auto-created by rotation workflow
Sensitivity: HIGHLY SENSITIVE (contains credentials)
Auto-updated: YES (daily)
Retention: Keep for recovery (review quarterly)
```

## Complete Setup Checklist

### Phase 1: Create GitHub App
- [ ] Go to GitHub Settings → Developer settings → GitHub Apps
- [ ] Click "New GitHub App"
- [ ] Fill in app details:
  - **App name:** e.g., "AI Marketplace Key Rotator"
  - **Homepage URL:** Your repository URL
  - **Webhook:** Uncheck (not needed)
  - **Permissions:**
    - Actions: Read, Write
    - Secrets: Read, Write
    - Environments: Read, Write
    - Organization secrets: Read, Write (optional)
- [ ] Save app
- [ ] Copy **App ID** → Use for `GITHUB_APP_ID`
- [ ] Generate **Private Key** → Use for `GITHUB_APP_PRIVATE_KEY`

### Phase 2: Generate Initial Keys

```bash
#!/bin/bash
set -euo pipefail

echo "=== Generating Initial Keys for Daily Rotation ==="
echo ""

# Generate suffix
SUFFIX=$(openssl rand -base64 128 | tr "[:lower:]" "[:upper:]" | tr -d '/+=' | head -c 8)
echo "✓ Generated suffix: $SUFFIX"

# Generate API keys
API_KEY=$(openssl rand -hex 32)
API_KEY_SECONDARY=$(openssl rand -hex 32)
echo "✓ Generated API keys"

# Generate signature keys
SIGN_KEY=$(openssl rand -base64 32)
SIGN_KEY_SECONDARY=$(openssl rand -base64 32)
echo "✓ Generated signature keys"

echo ""
echo "=== Initial Key Values (save for reference) ==="
echo "SUFFIX: $SUFFIX"
echo "API_KEY_DAILY_$SUFFIX: $API_KEY"
echo "API_KEY_SECONDARY_$SUFFIX: $API_KEY_SECONDARY"
echo "SIGN_KEY_DAILY_$SUFFIX: $SIGN_KEY"
echo "SIGN_KEY_DAILY_$SUFFIX_SECONDARY: $SIGN_KEY_SECONDARY"
```

### Phase 3: Set Environment Secrets

```bash
#!/bin/bash
set -euo pipefail

echo "=== Setting Secrets for Production Environment ==="
echo ""

# Get app credentials from files or prompts
read -p "GitHub App ID: " APP_ID
read -p "GitHub App Private Key file path: " PRIVATE_KEY_FILE

# Set GitHub App secrets
gh secret set GITHUB_APP_ID --env production --body "$APP_ID"
echo "✓ Set GITHUB_APP_ID"

gh secret set GITHUB_APP_PRIVATE_KEY --env production < "$PRIVATE_KEY_FILE"
echo "✓ Set GITHUB_APP_PRIVATE_KEY"

# Initial suffix
SUFFIX=$(openssl rand -base64 128 | tr "[:lower:]" "[:upper:]" | tr -d '/+=' | head -c 8)
gh secret set KEY_SUFFIX_DAILY --env production --body "$SUFFIX"
echo "✓ Set KEY_SUFFIX_DAILY: $SUFFIX"

gh secret set KEY_SUFFIX_DAILY_OLD --env production --body "XXXXXXXX"
echo "✓ Set KEY_SUFFIX_DAILY_OLD (placeholder)"

# Initial API keys
API_KEY=$(openssl rand -hex 32)
gh secret set "API_KEY_DAILY_$SUFFIX" --env production --body "$API_KEY"
echo "✓ Set API_KEY_DAILY_$SUFFIX"

API_KEY_SECONDARY=$(openssl rand -hex 32)
gh secret set "API_KEY_SECONDARY_$SUFFIX" --env production --body "$API_KEY_SECONDARY"
echo "✓ Set API_KEY_SECONDARY_$SUFFIX"

# Initial signature keys
SIGN_KEY=$(openssl rand -base64 32)
gh secret set "SIGN_KEY_DAILY_$SUFFIX" --env production --body "$SIGN_KEY"
echo "✓ Set SIGN_KEY_DAILY_$SUFFIX"

SIGN_KEY_SECONDARY=$(openssl rand -base64 32)
gh secret set "SIGN_KEY_DAILY_$SUFFIX_SECONDARY" --env production --body "$SIGN_KEY_SECONDARY"
echo "✓ Set SIGN_KEY_DAILY_$SUFFIX_SECONDARY"

echo ""
echo "=== All secrets configured ==="
gh secret list --env production | grep -E "^(GITHUB_APP|KEY_SUFFIX|API_KEY|SIGN_KEY)"
```

### Phase 4: Verify Setup

```bash
#!/bin/bash
set -euo pipefail

echo "=== Verifying Secret Setup ==="
echo ""

# Required secrets
required=(
  "GITHUB_APP_ID"
  "GITHUB_APP_PRIVATE_KEY"
  "KEY_SUFFIX_DAILY"
  "KEY_SUFFIX_DAILY_OLD"
)

# Check fixed secrets
for secret in "${required[@]}"; do
  if gh secret list --env production | grep -q "^$secret"; then
    echo "✓ $secret"
  else
    echo "✗ MISSING: $secret"
  fi
done

echo ""
echo "=== Dynamic Secrets (should exist with current suffix) ==="

# Get current suffix
SUFFIX=$(gh secret view KEY_SUFFIX_DAILY --env production)
echo "Current suffix: $SUFFIX"

# Check dynamic secrets
dynamic=(
  "API_KEY_DAILY_$SUFFIX"
  "API_KEY_SECONDARY_$SUFFIX"
  "SIGN_KEY_DAILY_$SUFFIX"
  "SIGN_KEY_DAILY_$SUFFIX_SECONDARY"
)

for secret in "${dynamic[@]}"; do
  if gh secret list --env production | grep -q "^$secret"; then
    echo "✓ $secret"
  else
    echo "✗ MISSING: $secret"
  fi
done

echo ""
echo "✓ Setup verification complete"
```

## Naming Convention Reference

| Secret Type | Pattern | Example |
|---|---|---|
| GitHub App ID | Fixed | `GITHUB_APP_ID` |
| GitHub App Private Key | Fixed | `GITHUB_APP_PRIVATE_KEY` |
| Key Suffix (current) | Fixed | `KEY_SUFFIX_DAILY` |
| Key Suffix (old) | Fixed | `KEY_SUFFIX_DAILY_OLD` |
| Primary API Key | Dynamic | `API_KEY_DAILY_ABC12345` |
| Secondary API Key | Dynamic | `API_KEY_SECONDARY_ABC12345` |
| Primary Signature Key | Dynamic | `SIGN_KEY_DAILY_ABC12345` |
| Secondary Signature Key | Dynamic | `SIGN_KEY_DAILY_ABC12345_SECONDARY` |
| API Keys Backup | Fixed | `BACKUP_API_KEYS_DAILY` |
| General Backup | Fixed | `BACKUP_KEYS_DAILY` |

## Troubleshooting Secret Setup

### "Secret not found" Error
**Cause:** Secret set at organization level instead of environment level  
**Solution:** Use `--env production` flag when setting secrets

### "GitHub App not authorized"
**Cause:** App permissions insufficient  
**Solution:** Update app permissions in GitHub settings to include required scopes

### "Private key format invalid"
**Cause:** Key file not in PEM format or corrupted  
**Solution:** Download new private key from GitHub App settings

### "Secret with suffix doesn't exist"
**Cause:** Keys haven't been rotated yet (first run)  
**Solution:** Run workflow manually or wait for scheduled execution

## Security Best Practices

✅ **DO:**
- Store private keys in secure password manager
- Rotate GitHub App credentials annually
- Monitor backup secrets for exposure
- Review access logs monthly
- Use environment-level secrets (not repository-level)

❌ **DON'T:**
- Share private keys via email/chat
- Commit secrets to repository
- Use weak random generation
- Reuse keys across environments
- Store plaintext backups

## Cleanup (Optional)

To remove all rotation secrets:

```bash
# List all rotation-related secrets
gh secret list --env production | grep -E "(KEY_SUFFIX|API_KEY|SIGN_KEY|BACKUP)"

# Delete specific secret
gh secret delete API_KEY_DAILY_OLDKEY --env production

# Delete all (use with caution!)
gh secret list --env production | grep DAILY | cut -d' ' -f1 | while read secret; do
  gh secret delete "$secret" --env production
done
```

## Support

For issues:
1. Verify all secrets exist: `gh secret list --env production`
2. Check workflow logs: `gh run view <run-id> --log`
3. Validate secret naming: Confirm suffix matches `KEY_SUFFIX_DAILY`
