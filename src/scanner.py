import re
import os
from pathlib import Path
import json
from datetime import datetime

# Secret patterns to detect
PATTERNS = {
    'api_key': r'(api[_-]?key|apikey)[\'"]?\s*[:=]\s*[\'"]?([a-zA-Z0-9_\-]+)',
    'password': r'(password|passwd|pwd)[\'"]?\s*[:=]\s*[\'"]([^\'"\n]+)[\'"]',
    'database_url': r'(postgres|mysql|mongodb|redis)://[^\s\n]+',
    'aws_access_key': r'AKIA[0-9A-Z]{16}',
    'private_key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
    'github_token': r'ghp_[a-zA-Z0-9_]{36,255}',
    'slack_token': r'xox[baprs]-[a-zA-Z0-9_\-]{10,}',
}

# Files to ignore
IGNORE_PATHS = {'.git', '.env.example', 'node_modules', '.venv', '__pycache__', '.DS_Store'}

class SecretScanner:
    def __init__(self):
        self.findings = []
    
    def scan_directory(self, root_path):
        """Scan directory recursively for secrets"""
        print(f"🔍 Scanning {root_path}...")
        
        for file in Path(root_path).rglob('*'):
            # Skip ignored paths
            if any(ignored in file.parts for ignored in IGNORE_PATHS):
                continue
            
            if file.is_file():
                self._scan_file(file)
        
        return self.findings
    
    def _scan_file(self, file_path):
        """Scan single file for secrets"""
        try:
            # Skip binary files
            if file_path.suffix in ['.pyc', '.so', '.o', '.bin', '.pdf']:
                return
            
            content = file_path.read_text(errors='ignore')
            
            for secret_type, pattern in PATTERNS.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    # Get line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    self.findings.append({
                        'file': str(file_path),
                        'type': secret_type,
                        'line': line_num,
                        'severity': self._get_severity(secret_type),
                        'match_preview': match.group(0)[:50] + '...' if len(match.group(0)) > 50 else match.group(0)
                    })
        
        except Exception as e:
            print(f"⚠️  Error scanning {file_path}: {e}")
    
    def _get_severity(self, secret_type):
        """Assign severity based on secret type"""
        critical = ['private_key', 'aws_access_key', 'github_token']
        high = ['database_url', 'slack_token', 'password']
        medium = ['api_key']
        
        if secret_type in critical:
            return 'CRITICAL'
        elif secret_type in high:
            return 'HIGH'
        else:
            return 'MEDIUM'
    
    def save_json(self, output_file='findings.json'):
        """Save findings to JSON"""
        with open(output_file, 'w') as f:
            json.dump(self.findings, f, indent=2)
        print(f"✅ Report saved to {output_file}")
    
    def print_summary(self):
        """Print summary of findings"""
        if not self.findings:
            print("✨ No secrets found!")
            return
        
        print(f"\n🚨 Found {len(self.findings)} potential secrets:\n")
        
        by_severity = {}
        for finding in self.findings:
            sev = finding['severity']
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        for severity, count in sorted(by_severity.items(), key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM'].index(x[0])):
            print(f"  {severity}: {count}")
        
        print("\nTop findings:")
        for i, finding in enumerate(self.findings[:5], 1):
            print(f"  {i}. [{finding['severity']}] {finding['type']} in {finding['file']}:{finding['line']}")