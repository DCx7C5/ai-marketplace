---
name: crypto-hardware-hsm-configure
description: Hardware Security Modules (HSMs) are tamper-resistant physical devices that safeguard cryptographic keys and perform cryptographic operations in a hardened environment. Keys stored in an HSM never leave the device boundary, providing the highest level of key protection. This skill covers configuring HSMs using the PKCS#11 standard interface, includ
domain: cybersecurity
---
--------|-----------|----------|
| FIPS 140-2 Level 1 | Software only | Development |
| FIPS 140-2 Level 2 | Tamper-evident, role-based auth | General production |
| FIPS 140-2 Level 3 | Tamper-resistant, identity-based auth | Financial, government |
| FIPS 140-2 Level 4 | Physical tamper response | Military, classified |

### PKCS#11 Architecture

```
Application --> PKCS#11 API --> HSM Provider --> Hardware HSM
                                    |
                              (SoftHSM2 for dev)
```

### Key Objects in PKCS#11

| Object Type | Description | Operations |
|-------------|-------------|-----------|
| CKO_SECRET_KEY | Symmetric keys (AES) | Encrypt, Decrypt, Wrap |
| CKO_PUBLIC_KEY | Public keys (RSA, EC) | Verify, Encrypt, Wrap |
| CKO_PRIVATE_KEY | Private keys (RSA, EC) | Sign, Decrypt, Unwrap |
| CKO_CERTIFICATE | X.509 certificates | Storage, retrieval |

## Security Considerations

- Never export private keys from HSM (use CKA_EXTRACTABLE=False)
- Use separate slots/partitions for different applications
- Implement multi-person key ceremony for CA root keys
- Enable audit logging for all HSM operations
- Implement HSM backup and disaster recovery
- Use strong PINs and enable SO (Security Officer) PIN

## Validation Criteria

- [ ] SoftHSM2 initializes with token and user PIN
- [ ] AES key generates inside HSM
- [ ] RSA key pair generates inside HSM
- [ ] Encryption/decryption uses HSM-resident keys
- [ ] Signing/verification uses HSM-resident keys
- [ ] Keys cannot be exported (non-extractable)
- [ ] Key listing shows all HSM-stored objects