# 🔐 Secret Scanner

Automatically detect exposed credentials in your codebase before they reach production.

## Features
- **Pattern-based detection** - Finds API keys, passwords, database URLs, AWS keys, SSH keys, tokens
- **JSON reports** - Machine-readable output for CI/CD integration
- **HTML reports** - Visual dashboard of findings with severity levels
- **Command-line interface** - Easy to use for local scanning
- **Pre-commit hook** - Blocks commits with secrets automatically
- **Severity scoring** - Labels findings as CRITICAL, HIGH, or MEDIUM

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/secret-scanner.git
cd secret-scanner
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python setup_hook.py
```

## Usage

### Local Scan
```bash
python -m src.cli /path/to/scan
```

### Generate Reports
```bash
# JSON report
python -m src.cli /path/to/scan --output findings.json

# HTML report
python -m src.cli /path/to/scan --html
```

### View HTML Report
```bash
start reports/report.html  # Windows
open reports/report.html   # Mac
```

## What It Detects

| Type | Example | Severity |
|------|---------|----------|
| API Keys | `sk-1234567890abcdef` | MEDIUM |
| Passwords | `password='admin123'` | HIGH |
| Database URLs | `postgres://user:pass@localhost/db` | HIGH |
| AWS Keys | `AKIA0123456789ABCDEF` | CRITICAL |
| GitHub Tokens | `ghp_1234567890abcdefghijklmnop` | CRITICAL |
| SSH Private Keys | `-----BEGIN RSA PRIVATE KEY-----` | CRITICAL |
| Slack Tokens | `xoxb-1234567890123-1234567890123` | CRITICAL |

## Features Explained

### 1. Pattern-Based Detection
Your scanner uses regex patterns to find common secret formats. It looks for:
- Variable assignments with secret keywords (`api_key =`, `password =`)
- Known secret prefixes (AWS keys start with `AKIA`, GitHub tokens start with `ghp_`)
- Database connection strings (postgres://, mysql://, etc.)

**How it works:**
```python
if re.search(r'api[_-]?key\s*[:=]', content):
    # Found a secret!
```

### 2. Pre-Commit Hook
Runs automatically before you push code to GitHub. If secrets are found:
- ❌ Commit is blocked
- You fix the secrets
- ✅ Commit succeeds

**Setup:** `python setup_hook.py`

**What happens:**
```bash
$ git commit -m "my changes"
Running secret scanner...
Secrets found! Fix before committing.
# Fix the file, then commit again
```

### 3. HTML Reports
Visual dashboard showing:
- Total secrets found
- Breakdown by severity (CRITICAL/HIGH/MEDIUM)
- File location, line number, secret type
- Color-coded table for easy scanning

**Usage:** `python -m src.cli . --html`

### 4. JSON Reports
Machine-readable format for integration with:
- GitHub Actions (CI/CD)
- Slack notifications
- Security dashboards
- Automated remediation tools

**Example output:**
```json
[
  {
    "file": "config.py",
    "type": "api_key",
    "line": 5,
    "severity": "MEDIUM",
    "match_preview": "api_key = 'sk-123...'"
  }
]
```

## Example Workflow

```bash
# 1. Scan your project
$ python -m src.cli my-project --output findings.json --html

# 2. View HTML report
$ start reports/report.html

# 3. Fix secrets (move to .env, use environment variables)

# 4. Re-scan to verify
$ python -m src.cli my-project
✨ No secrets found!

# 5. Commit and push
$ git add .
$ git commit -m "Remove hardcoded secrets"
$ git push
```

## Roadmap

- [ ] **Entropy-based detection** - Find high-entropy strings (likely secrets) even without pattern matches
- [ ] **GitHub Actions CI/CD** - Automatically scan on every push
- [ ] **Slack notifications** - Alert team when secrets are found
- [ ] **Ignore list** - Whitelist false positives
- [ ] **Performance optimization** - Faster scanning for large repos

## Why This Matters

Exposed secrets are the #1 cause of data breaches. This tool:
- Prevents accidental leaks before they happen
- Saves companies from regulatory fines (GDPR, SOC 2)
- Demonstrates security awareness to employers
- Integrates into real development workflows

<img width="1107" height="486" alt="image" src="https://github.com/user-attachments/assets/d36d4935-861e-4099-bf80-e18be1be91b2" />


## License
MIT
