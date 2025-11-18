# Email Authentication Verification Guide

## ✅ Quick Verification

After receiving a test email, verify that **SPF**, **DKIM**, and **DMARC** all passed.

**What to Look For:**
- ✅ `spf=pass`
- ✅ `dkim=pass` 
- ✅ `dmarc=pass`

All three must show `pass` for proper email authentication.

---

## 📧 How to Check Email Headers by Client

### Gmail

1. Open the email in Gmail
2. Click the **three dots (⋮)** in the top-right corner of the email
3. Select **"Show original"** from the dropdown menu
4. Look for the **"Authentication-Results"** section

**What you'll see:**
```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of noreply@distributedcreatives.org designates X.X.X.X as permitted sender) smtp.mailfrom=noreply@distributedcreatives.org;
       dkim=pass header.i=@distributedcreatives.org;
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from=distributedcreatives.org
```

✅ **Success indicators:**
- `spf=pass`
- `dkim=pass`
- `dmarc=pass`

❌ **If you see failures:**
- `spf=fail` → DNS SPF record not configured or incorrect
- `dkim=fail` → DKIM signature missing or invalid
- `dmarc=fail` → DMARC policy violation or missing DMARC record

---

### Outlook (Web)

1. Open the email in Outlook
2. Click the **three dots (⋯)** next to Reply/Forward
3. Select **"View"** → **"View message source"** or **"Show message details"**

**Alternative method:**
1. Open the email
2. Click **"..."** → **"View"** → **"Message details"**
3. Look for **"Authentication-Results"** header

---

### Outlook (Desktop)

1. Open the email in Outlook desktop app
2. Right-click on the email
3. Select **"Options"** from the context menu
4. Look at the **"Internet Headers"** section
5. Find the **"Authentication-Results"** header

---

### Apple Mail (macOS)

1. Open the email in Apple Mail
2. Right-click on the email in the message list
3. Select **"View Source"** (or press `Cmd+Option+U`)
4. Look for **"Authentication-Results"** in the raw headers

**Alternative method:**
1. Select the email
2. Go to **"View"** → **"Message"** → **"Raw Source"**

---

### Yahoo Mail

1. Open the email in Yahoo Mail
2. Click the **three dots (⋯)** menu
3. Select **"View raw message"** or **"Show headers"**
4. Look for **"Authentication-Results"** section

---

### Thunderbird

1. Open the email in Thunderbird
2. Right-click on the email
3. Select **"View Source"** from the context menu
4. Search for **"Authentication-Results"**

---

## 🔍 What to Look For in Headers

### SPF (Sender Policy Framework)

**Look for:**
```
spf=pass (google.com: domain of noreply@distributedcreatives.org 
         designates X.X.X.X as permitted sender) 
         smtp.mailfrom=noreply@distributedcreatives.org
```

**Statuses:**
- ✅ `spf=pass` - Sender authorized
- ⚠️ `spf=neutral` - Not explicitly authorized (may still pass DMARC)
- ❌ `spf=fail` - Sender not authorized (authentication failed)
- ❓ `spf=softfail` - Not authorized, but not explicitly rejected

---

### DKIM (DomainKeys Identified Mail)

**Look for:**
```
dkim=pass header.i=@distributedcreatives.org;
```

**Statuses:**
- ✅ `dkim=pass` - Signature valid, email authenticated
- ❌ `dkim=fail` - Signature invalid or missing
- ⚠️ `dkim=neutral` - No signature found (not necessarily a failure)

**Key fields:**
- `header.i=` - The domain that signed the email
- Should match your sending domain (`@distributedcreatives.org`)

---

### DMARC (Domain-based Message Authentication, Reporting & Conformance)

**Look for:**
```
dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) 
           header.from=distributedcreatives.org
```

**Statuses:**
- ✅ `dmarc=pass` - Email authenticated and authorized
- ⚠️ `dmarc=quarantine` - Authentication failed, but email accepted (may go to spam)
- ❌ `dmarc=reject` - Authentication failed, email rejected
- ❌ `dmarc=fail` - Policy violation

**Policy values:**
- `p=none` - Monitor only (no action)
- `p=quarantine` - Place in spam if auth fails
- `p=reject` - Reject if auth fails

**Alignment:**
- Must see `header.from=distributedcreatives.org` matching your domain

---

## 📊 Complete Authentication-Results Example

Here's what a properly authenticated email should look like:

```
Authentication-Results: mx.google.com;
       spf=pass (google.com: domain of noreply@distributedcreatives.org 
                 designates 54.240.X.X as permitted sender) 
                 smtp.mailfrom=noreply@distributedcreatives.org;
       dkim=pass header.i=@distributedcreatives.org 
                 header.s=amazonses 
                 header.b="...signature...";
       dmarc=pass (p=QUARANTINE sp=QUARANTINE dis=NONE) 
                 header.from=distributedcreatives.org
```

**Key elements:**
1. ✅ `spf=pass` - SPF check passed
2. ✅ `dkim=pass` - DKIM signature valid
3. ✅ `dmarc=pass` - DMARC policy passed
4. ✅ Domain alignment: `header.from=distributedcreatives.org` matches sender domain

---

## 🔧 Troubleshooting Failed Authentication

### SPF Failure

**Issue:** `spf=fail` or `spf=softfail`

**Check:**
1. SPF DNS record exists: `dig TXT distributedcreatives.org | grep spf`
2. AWS SES IPs included in SPF record
3. SPF record syntax is correct

**AWS SES SPF record should include:**
```
v=spf1 include:amazonses.com ~all
```

---

### DKIM Failure

**Issue:** `dkim=fail` or no DKIM signature

**Check:**
1. DKIM enabled in AWS SES Console
2. DKIM DNS records published correctly
3. Selector matches (check `header.s=` in email headers)

**Verify DKIM records:**
```bash
dig TXT <selector>._domainkey.distributedcreatives.org
```

---

### DMARC Failure

**Issue:** `dmarc=fail` or `dmarc=quarantine`

**Check:**
1. DMARC DNS record exists: `dig TXT _dmarc.distributedcreatives.org`
2. SPF or DKIM alignment passes
3. `From:` domain matches authenticated domain

**Basic DMARC record:**
```
v=DMARC1; p=none; rua=mailto:dmarc-reports@distributedcreatives.org
```

**For production (after testing):**
```
v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@distributedcreatives.org
```

---

## ✅ Verification Checklist

After receiving a test email, verify:

- [ ] Email arrived in inbox (not spam)
- [ ] `spf=pass` in Authentication-Results
- [ ] `dkim=pass` in Authentication-Results  
- [ ] `dmarc=pass` in Authentication-Results
- [ ] Domain alignment correct (`header.from=distributedcreatives.org`)
- [ ] From address matches verified domain
- [ ] No authentication warnings in email client

---

## 🧪 Quick Test Command

If you saved the email as a file, you can check headers with:

```bash
# If you saved the email as email.eml
grep -i "authentication-results" email.eml
grep -i "spf=" email.eml
grep -i "dkim=" email.eml
grep -i "dmarc=" email.eml
```

---

## 📚 Additional Resources

- [AWS SES Email Authentication Guide](https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication.html)
- [SPF Record Syntax](https://tools.ietf.org/html/rfc7208)
- [DKIM Overview](https://tools.ietf.org/html/rfc6376)
- [DMARC Specification](https://tools.ietf.org/html/rfc7489)
- [Gmail Postmaster Tools](https://postmaster.google.com/)

---

## 🎯 Success Criteria

Your email authentication is properly configured when:

1. ✅ All three authentication methods pass (`spf=pass`, `dkim=pass`, `dmarc=pass`)
2. ✅ Domain alignment is correct
3. ✅ Emails arrive in inbox (not spam folder)
4. ✅ No authentication warnings in email client
5. ✅ Ready for bulk sending (important for Gmail/Yahoo 2024 requirements)

---

**Next Steps:**
- If all checks pass ✅ → Ready for production newsletter sending
- If any checks fail ❌ → Review DNS configuration in AWS SES Console
- Need help? → See troubleshooting section above or check AWS SES documentation


