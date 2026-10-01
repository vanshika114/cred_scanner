# 🔐 Secret Scanner

Automatically detect exposed credentials in your codebase.

## Features
- Detects API keys, passwords, database URLs, AWS keys, SSH keys, tokens
- Generates JSON reports
- HTML report generation (coming soon)
- Command-line interface

## Usage
```bash
python cli.py /path/to/scan --output findings.json
```

## What It Finds
- API keys (OpenAI, Stripe, etc.)
- Database passwords (postgres, MySQL, MongoDB)
- AWS access keys
- GitHub tokens
- SSH private keys

## Example
```bash
$ python cli.py ./my-project
🔍 Scanning ./my-project...
🚨 Found 2 potential secrets:
  CRITICAL: 1
  HIGH: 1

[CRITICAL] private_key in config/keys.py:5
[HIGH] database_url in .env:2
```

## Next Steps
- Pre-commit hook integration
- CI/CD pipeline integration
- Entropy-based detection for stronger passwords