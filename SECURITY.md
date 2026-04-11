# Security Policy — The Amaravati Record

## Reporting a Vulnerability

If you have discovered a security vulnerability in this repository or in the deployed site at <https://sahitkogs.github.io/TheAmaravatiRecord/>, please report it privately to:

**<sahit.koganti@gmail.com>**

You can also use the machine-readable security contact at <https://sahitkogs.github.io/TheAmaravatiRecord/.well-known/security.txt>.

## What to include

A useful report contains:

- A description of the vulnerability and its potential impact
- Steps to reproduce it (URLs, payloads, affected files)
- Your assessment of severity (low, medium, high, critical)
- Whether the vulnerability has been disclosed publicly
- Whether you would like to be credited in the public fix announcement (and if so, how)

## What to expect

- **Acknowledgement within 72 hours.** This is a one-person operation, so "urgent" requests might still take a couple of days, but 72 hours is the commitment.
- **A plain-English explanation** of what we are going to do about it, on what timeline, and whether we consider it in scope.
- **No legal action** against good-faith security research. If you stick to reporting and responsible disclosure, you will not hear from a lawyer.
- **Credit where you want it.** Public acknowledgement in the fix commit and a line in the corrections ledger, if the vulnerability was meaningful and you have asked for credit.

## Scope

**In scope:**

- The static site at <https://sahitkogs.github.io/TheAmaravatiRecord/> and all its subpages
- The source code, scripts, and pipelines in this repository
- The GitHub Actions, secrets, and deployment flow for this repository
- Privacy and data-handling issues in our analytics configuration (Google Analytics 4)
- Issues with the PGP public key, security.txt, or any other security-adjacent metadata

**Out of scope:**

- Issues in GitHub Pages itself (report those to [GitHub Security](https://github.com/security))
- Issues in Google Analytics or other third-party services (report directly to the service owner)
- Social-engineering attacks against the editor as an individual
- Theoretical weaknesses without a practical attack (we welcome these, but they are advisory rather than treated as vulnerabilities)
- Denial-of-service attacks or attempts to overwhelm the site infrastructure

## Legal safe harbour

Good-faith security research on this site is welcomed and will not be met with legal action, provided you:

1. Do not access, modify, or delete data belonging to readers or the publisher
2. Do not degrade the site's availability for others
3. Do not publicly disclose the vulnerability before it has been acknowledged and, ideally, fixed
4. Respect the privacy of any user data you might incidentally encounter
5. Comply with applicable Indian and international law

In the extremely unlikely event that your good-faith research produces a complaint from a third party, we will make clear publicly that you acted with authorization under this policy.

## Our own commitments

As a one-desk newsroom, we take the following practical measures:

- We keep dependencies minimal and static. There is no backend database to leak.
- We disclose every third-party script on the site in the privacy policy and cookie notice.
- We do not log reader IP addresses beyond what GitHub Pages does for all sites.
- We encrypt sensitive source material and hold it offline.
- We rotate any credentials that are exposed accidentally.

If any of these commitments breaks, we will log the breach in the [corrections ledger](https://sahitkogs.github.io/TheAmaravatiRecord/corrections.html) and explain what happened.

## Thank You

If you are a security researcher considering reporting something here: thank you. Independent newsrooms rely on the goodwill of people like you to stay trustworthy.
