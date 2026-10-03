# 🔐 Secret Scanner

Automatically detect exposed credentials in your codebase before they reach production.

## Features
- **Pattern-based detection** - Finds API keys, passwords, database URLs, AWS keys, SSH keys, tokens
- **Entropy-based detection** - Identifies high-entropy strings likely to be secrets
- **JSON reports** - Machine-readable output for CI/CD integration
- **HTML reports** - Visual dashboard of findings with severity levels
- **Command-line interface** - Easy to use for local scanning
- **Pre-commit hook** - Blocks commits with secrets automatically
- **Exclusion support** - Skip specific files/folders (README, examples, etc.)
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

### Exclude Files
```bash
python -m src.cli . --exclude README.md,examples/
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
| High-Entropy Strings | Random-looking strings | MEDIUM |

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

### 2. Entropy-Based Detection
Finds high-entropy strings (8+ characters with randomness) that likely contain secrets, even without pattern matches.

**How it works:**
- Calculates Shannon entropy for each word
- Entropy > 4.5 = likely a secret
- Example: `aK9$mP2@xL7` has high entropy (random), `admin123` has low entropy (predictable)

**Why it matters:**
- Catches API keys without standard prefixes
- Finds custom secret formats
- Reduces false negatives from pattern matching alone

### 3. Pre-Commit Hook
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

### 4. HTML Reports
Visual dashboard showing:
- Total secrets found
- Breakdown by severity (CRITICAL/HIGH/MEDIUM)
- File location, line number, secret type
- Color-coded table for easy scanning

**Usage:** `python -m src.cli . --html`

### 5. Exclusion Support
Skip false positives in documentation and examples:

```bash
python -m src.cli . --exclude README.md,examples/
```

Useful for:
- Keeping secret examples in documentation
- Excluding third-party dependencies
- Skipping non-source files

### 6. JSON Reports
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

- [x] **Pattern-based detection** - Regex patterns for common secrets
- [x] **Entropy-based detection** - Shannon entropy for high-randomness strings
- [x] **Pre-commit hook** - Prevent secrets from reaching GitHub
- [x] **HTML/JSON reports** - Visual and machine-readable output
- [ ] **GitHub Actions CI/CD** - Automatically scan on every push
- [ ] **Slack notifications** - Alert team when secrets are found
- [ ] **Whitelist/ignore list** - Configurable false positives
- [ ] **Performance optimization** - Faster scanning for large repos
- [ ] **Machine learning model** - ML-based secret detection

## Why This Matters

Exposed secrets are the #1 cause of data breaches. This tool:
- Prevents accidental leaks before they happen
- Saves companies from regulatory fines (GDPR, SOC 2)
- Demonstrates security awareness to employers
- Integrates into real development workflows


<img width="1107" height="486" alt="image" src="https://github.com/user-attachments/assets/6a726cd9-bec4-4ad5-ac5f-2dc73c328a51" />


<img width="554" height="284" alt="image" src="https://github.com/user-attachments/assets/c18f0f94-7740-4350-9db2-1e91d091bf58" />


<img width="554" height="312" alt="image" src="https://github.com/user-attachments/assets/04da2d8f-e63e-4812-a78d-d575c8df9560" />

