# Daily Key Rotation Workflow

## Overview

The `rotate_keys_daily.yml` workflow automates daily rotation of cryptographic keys and API credentials stored as GitHub secrets. It implements a secure key management strategy by:

- **Daily suffix rotation** — Generates random 8-character suffix daily
- **API key rotation** — Rotates primary and secondary API keys
- **Signature key rotation** — Rotates Ed25519 signature keys for signing
- **Automated backup** — Backs up old keys before deletion
- **Verification** — Validates new keys exist after rotation

## Architecture

### Job Dependency Chain

```
rotate-key-suffix
    ↓
    ├→ rotate-api-keys
    ├→ rotate-signature-keys
    ↓
verify-rotation
```

### Jobs

1. **rotate-key-suffix** (runs-on: ubuntu-latest)
   - Backs up current `KEY_SUFFIX_DAILY` to `KEY_SUFFIX_DAILY_OLD`
   - Generates new random 8-character suffix
   - Sets new `KEY_SUFFIX_DAILY` secret

2. **rotate-api-keys** (needs: rotate-key-suffix)
   - Backs up existing API keys with old suffix
   - Generates new 32-byte hex API keys
   - Sets `API_KEY_DAILY_[SUFFIX]` and `API_KEY_SECONDARY_[SUFFIX]`
   - Deletes old API keys with old suffix

3. **rotate-signature-keys** (needs: rotate-key-suffix)
   - Backs up existing signature keys
   - Generates new base64-encoded 32-byte signature keys
   - Sets `SIGN_KEY_DAILY_[SUFFIX]` and `SIGN_KEY_DAILY_[SUFFIX]_SECONDARY`
   - Deletes old signature keys with old suffix

4. **verify-rotation** (needs: rotate-api-keys, rotate-signature-keys)
   - Verifies all new secrets exist
   - Confirms `KEY_SUFFIX_DAILY` is set
   - Confirms API keys are present
   - Confirms signature keys are present
   - Logs rotation completion timestamp

## Configuration

### Schedule

- **Default:** Daily at 22:02 UTC (cron: `2 22 * * *`)
- **Manual trigger:** Via `workflow_dispatch`

### Environment

- **Environment:** `production`
- **Permissions:** `contents: write`, `actions: write`

## Required Secrets

These secrets must be configured at the **environment level** (`production`):

### GitHub App Credentials
```yaml
GITHUB_APP_ID              # GitHub App ID (numeric)
GITHUB_APP_PRIVATE_KEY     # GitHub App private key (PEM format)
```

### Initial Key Secrets
```yaml
KEY_SUFFIX_DAILY           # Initial 8-char suffix (e.g., "ABCD1234")
KEY_SUFFIX_DAILY_OLD       # Previous suffix (starts empty or placeholder)
API_KEY_DAILY_ABCD1234     # API key for current suffix
API_KEY_SECONDARY_ABCD1234 # Secondary API key for current suffix
SIGN_KEY_DAILY_ABCD1234    # Signature key for current suffix
SIGN_KEY_DAILY_ABCD1234_SECONDARY  # Secondary signature key
```

### Backup Secrets
```yaml
BACKUP_API_KEYS_DAILY      # Backup of rotated keys (auto-managed)
BACKUP_KEYS_DAILY          # Additional backup (auto-managed)
```

## Setup Instructions

### 1. Create GitHub App (if not exists)

```bash
# GitHub App should have permissions:
# - Actions: read/write
# - Secrets: read/write
# - Environments: read/write
# - Organization secrets: read/write (if org-level)
```

### 2. Add Secrets to Production Environment

In GitHub: **Settings → Environments → production → Environment secrets**

```yaml
# 1. GitHub App credentials
GITHUB_APP_ID=<your-app-id>
GITHUB_APP_PRIVATE_KEY=<your-app-private-key>

# 2. Initial key suffix
KEY_SUFFIX_DAILY=INITKEY0

# 3. Initial API keys (generate with: openssl rand -hex 32)
API_KEY_DAILY_INITKEY0=<64-char-hex-string>
API_KEY_SECONDARY_INITKEY0=<64-char-hex-string>

# 4. Initial signature keys (generate with: openssl rand -base64 32)
SIGN_KEY_DAILY_INITKEY0=<base64-32-bytes>
SIGN_KEY_DAILY_INITKEY0_SECONDARY=<base64-32-bytes>

# 5. Old suffix (placeholder initially)
KEY_SUFFIX_DAILY_OLD=XXXXXXXX
```

### 3. Generate Initial Keys

```bash
# Suffix (8 chars, uppercase alphanumeric)
openssl rand -base64 128 | tr "[:lower:]" "[:upper:]" | tr -d '/+=' | head -c 8

# API keys (32 bytes as hex = 64 chars)
openssl rand -hex 32

# Signature keys (32 bytes as base64)
openssl rand -base64 32
```

## Secret Naming Convention

All secrets follow the pattern:
```
{KEY_TYPE}_{SCOPE}_{SUFFIX}
```

Examples:
- `API_KEY_DAILY_ABC12345` — Primary API key for current suffix
- `API_KEY_SECONDARY_ABC12345` — Secondary API key for current suffix
- `SIGN_KEY_DAILY_ABC12345` — Signature key for current suffix
- `SIGN_KEY_DAILY_ABC12345_SECONDARY` — Secondary signature key for current suffix

## How It Works

### Step 1: Suffix Rotation
```yaml
Old Suffix: INITKEY0
New Suffix: RANDOMAB (generated)
```

### Step 2: API Key Rotation
```yaml
Before:
  - API_KEY_DAILY_INITKEY0 = <old-key>
  - API_KEY_SECONDARY_INITKEY0 = <old-key>

After:
  - API_KEY_DAILY_RANDOMAB = <new-key>
  - API_KEY_SECONDARY_RANDOMAB = <new-key>
  - Old keys deleted
  - Backup saved to BACKUP_API_KEYS_DAILY
```

### Step 3: Signature Key Rotation
```yaml
Before:
  - SIGN_KEY_DAILY_INITKEY0 = <old-key>
  - SIGN_KEY_DAILY_INITKEY0_SECONDARY = <old-key>

After:
  - SIGN_KEY_DAILY_RANDOMAB = <new-key>
  - SIGN_KEY_DAILY_RANDOMAB_SECONDARY = <new-key>
  - Old keys deleted
  - Backup available
```

### Step 4: Verification
```yaml
✓ KEY_SUFFIX_DAILY = RANDOMAB
✓ API_KEY_DAILY_RANDOMAB exists
✓ SIGN_KEY_DAILY_RANDOMAB exists
✓ Rotation completed at [timestamp]
```

## Usage

### Automatic (Scheduled)
Workflow runs automatically every day at 22:02 UTC.

### Manual Trigger
```bash
gh workflow run rotate_keys_daily.yml --ref main
```

### Monitor Execution
```bash
# List recent runs
gh workflow runs rotate_keys_daily.yml --limit 5

# Watch specific run
gh run watch <run-id>
```

## Testing

A comprehensive test workflow (`test_rotate_keys_daily.yml`) validates:

1. **YAML Syntax** — Workflow file structure
2. **Job Dependencies** — Correct job chain
3. **Secret References** — All required secrets referenced
4. **Schedule** — Cron configured correctly
5. **Key Generation** — Simulated key generation logic

Run tests:
```bash
gh workflow run test_rotate_keys_daily.yml --ref main
```

## Key Retrieval in Workflows

To use rotated keys in other workflows:

```yaml
jobs:
  use-rotated-keys:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Use API Key
        shell: bash
        env:
          # Dynamically reference current suffix
          CURRENT_SUFFIX: ${{ secrets.KEY_SUFFIX_DAILY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Example: Fetch current API key
          CURRENT_API_KEY="${{ secrets[format('API_KEY_DAILY_{0}', secrets.KEY_SUFFIX_DAILY)] }}"
          echo "Using API key for suffix: ${CURRENT_SUFFIX}"
```

## Backup and Recovery

### View Backups
```bash
gh secret list --env production | grep BACKUP
```

### Restore from Backup (if needed)
```bash
# Manually restore from BACKUP_API_KEYS_DAILY
gh secret set API_KEY_DAILY_NEWKEY --env production --body "$(gh secret view BACKUP_API_KEYS_DAILY --env production)"
```

## Security Considerations

✓ **GitHub App Token** — Uses temporary app-generated token instead of GITHUB_TOKEN  
✓ **Secret Masking** — All secrets are masked in logs with `::add-mask::`  
✓ **Automatic Cleanup** — Old keys deleted immediately after new ones verified  
✓ **Backup Trail** — Previous keys backed up before deletion  
✓ **Restricted Scope** — Permissions limited to necessary operations  

⚠️ **Important:**
- Keep GitHub App private key secure
- Rotate GitHub App key annually
- Monitor backup secrets for sensitive data exposure
- Review old key backups monthly

## Troubleshooting

### Workflow Failed: "Failed to set secret"
**Cause:** GitHub App doesn't have `secrets: write` permission  
**Solution:** Ensure app permissions include organization secrets write

### Workflow Failed: "Failed to delete old key"
**Cause:** Old key might have already been deleted  
**Solution:** This is non-fatal; workflow continues (logged as warning)

### Missing New Keys
**Cause:** Workflow failed silently or permissions issue  
**Solution:** Check workflow run logs; verify environment access

### Manual Secret Recovery
If keys become corrupted:
```bash
# Restore from backup
gh secret view BACKUP_API_KEYS_DAILY --env production

# Manually set if backup exists
gh secret set API_KEY_DAILY_NEWSUFFIX --env production --body "<key-value>"
```

## Monitoring

### Health Check Query
```bash
# Check last rotation time
gh secret view KEY_SUFFIX_DAILY --env production

# List all daily rotation secrets
gh secret list --env production | grep -E "^(API_KEY_DAILY|SIGN_KEY_DAILY|KEY_SUFFIX_DAILY)"
```

### Metrics to Track
- Last rotation timestamp (in workflow output)
- Number of active keys (should decrease to 0 after verification)
- Backup growth (old keys accumulate; review monthly)

## Maintenance

### Monthly Tasks
- [ ] Review backup secrets size
- [ ] Verify workflow ran successfully
- [ ] Check for any failed rotations in logs

### Quarterly Tasks
- [ ] Audit GitHub App permissions
- [ ] Review secret access logs
- [ ] Test manual recovery procedure

### Annual Tasks
- [ ] Rotate GitHub App credentials
- [ ] Review key rotation strategy
- [ ] Update documentation

## Integration with CI/CD

Example: Using rotated keys in a deployment workflow

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Get Current API Key
        id: api_key
        shell: bash
        run: |
          suffix="${{ secrets.KEY_SUFFIX_DAILY }}"
          echo "suffix=$suffix" >> "$GITHUB_OUTPUT"
      
      - name: Deploy with Current Key
        env:
          API_KEY: ${{ secrets[format('API_KEY_DAILY_{0}', steps.api_key.outputs.suffix)] }}
        run: |
          ./deploy.sh --api-key "$API_KEY"
```

## References

- [GitHub Actions: Create GitHub App Token](https://github.com/actions/create-github-app-token)
- [GitHub CLI: Secrets Management](https://cli.github.com/manual/gh_secret)
- [OpenSSL Random Key Generation](https://www.openssl.org/docs/man3.0/man1/openssl-rand.html)

## Support

For issues or questions:
1. Check workflow logs: `gh run view <run-id> --log`
2. Review test results: `gh workflow runs test_rotate_keys_daily.yml`
3. Inspect current secrets: `gh secret list --env production`
