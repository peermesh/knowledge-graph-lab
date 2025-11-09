# DNS Configuration

## What's Already Done

DNS is configured and live. You don't need to touch this.

This doc explains what was set up, in case you need to troubleshoot.

## Records Added

### 1. Domain Verification
```
Name: _amazonses.distributedcreatives.org
Type: TXT
Value: TE66lbYIPqac+aNTDisfCdY1P/CNBOhLkup03Zhk7MU=
```
**Purpose:** Proves you own the domain.

### 2. DKIM Authentication (3 records)
```
ulzliv7hjv4q3xj6eioo77evzj2dfldq._domainkey → ulzliv7hjv4q3xj6eioo77evzj2dfldq.dkim.amazonses.com
uonp5rrph56sqbffrd7trpbkpov5xxak._domainkey → uonp5rrph56sqbffrd7trpbkpov5xxak.dkim.amazonses.com
twifdy26tajah4ahwkpq2j4kplhwexqg._domainkey → twifdy26tajah4ahwkpq2j4kplhwexqg.dkim.amazonses.com
```
**Purpose:** Cryptographic signing to prove emails are authentic.

### 3. SPF Authorization
```
Name: distributedcreatives.org
Type: TXT
Value: "v=spf1 include:_spf.google.com include:amazonses.com -all"
```
**Purpose:** Authorizes both Google Workspace and Amazon SES to send email.

### 4. DMARC Policy
```
Name: _dmarc.distributedcreatives.org
Type: TXT
Value: "v=DMARC1; p=none; rua=mailto:team@distributedcreatives.org,..."
```
**Purpose:** Tells receivers how to handle authentication failures.

## Checking DNS

### Verify Domain
```bash
aws ses get-identity-verification-attributes \
  --identities distributedcreatives.org \
  --region us-east-2
```
Should show: `"VerificationStatus": "Success"`

### Check DKIM
```bash
aws ses get-identity-dkim-attributes \
  --identities distributedcreatives.org \
  --region us-east-2
```
Should show: `"DkimVerificationStatus": "Success"`

### Manual DNS Check
```bash
# Domain verification
dig _amazonses.distributedcreatives.org TXT

# DKIM (check one)
dig ulzliv7hjv4q3xj6eioo77evzj2dfldq._domainkey.distributedcreatives.org CNAME

# SPF
dig distributedcreatives.org TXT | grep spf

# DMARC
dig _dmarc.distributedcreatives.org TXT
```

## Email Authentication Explained

When you send an email, receivers check:

1. **SPF** - "Is this server authorized to send for this domain?"
   - Checks IP address against SPF record
   - Pass = Server is in the list

2. **DKIM** - "Is this email cryptographically signed?"
   - Checks signature using public key in DNS
   - Pass = Signature valid and matches

3. **DMARC** - "Do SPF and DKIM align with the From address?"
   - Pass = Both SPF and DKIM pass AND match From domain
   - Fail = Email goes to spam or is rejected

**All three must pass** for best deliverability.

## Viewing Email Headers

To see if authentication passed:

**Gmail:**
1. Open email
2. Three dots → Show original
3. Look for:
   ```
   spf=pass
   dkim=pass
   dmarc=pass
   ```

**Outlook:**
1. Open email
2. File → Properties
3. Look in "Internet headers"

## Troubleshooting

### SPF Fails
- DNS issue with SPF record
- Sending from wrong server/IP
- SPF record too long (>255 chars)

### DKIM Fails
- Domain not verified yet (wait for DNS)
- DKIM records missing/incorrect
- Clock skew on sending server

### DMARC Fails
- SPF or DKIM not passing
- Domain mismatch (From vs envelope)
- Strict alignment mode (aspf=s, adkim=s)

## When to Update DNS

You only need to touch DNS if:
- Moving to different email provider
- Adding another sender (e.g., Mailchimp)
- Setting up custom MAIL FROM domain
- Domain changes

Otherwise, leave it alone - it's working.
