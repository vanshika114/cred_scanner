import re
import os
from pathlib import Path
import json
from datetime import datetime

# Secret patterns to detect
PATTERNS = {
    'api_key': r'(api[_-]?key|apikey)\s*[:=]', 
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

    def generate_html_report(self, output_file='report.html'):
        """Generate HTML report from findings"""
    
        html = """
        <html>
        <head>
            <title>Secret Scanner Report</title>
            <style>
                body { font-family: Arial; margin: 20px; background: #f5f5f5; }
                h1 { color: #333; }
                .summary { background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }
                table { width: 100%; border-collapse: collapse; background: white; }
                th { background: #333; color: white; padding: 10px; text-align: left; }
                td { padding: 10px; border-bottom: 1px solid #ddd; }
                .CRITICAL { background: #ffcccc; color: #cc0000; font-weight: bold; }
                .HIGH { background: #ffe6cc; color: #ff6600; font-weight: bold; }
                .MEDIUM { background: #ffffcc; color: #ff9900; font-weight: bold; }
                tr:hover { background: #f9f9f9; }
            </style>
        </head>
        <body>
            <h1>🔐 Secret Scanner Report</h1>
        """
    
    # Summary
        if self.findings:
            by_severity = {}
            for finding in self.findings:
                sev = finding['severity']
                by_severity[sev] = by_severity.get(sev, 0) + 1
        
            html += f"<div class='summary'><h2>Summary</h2>"
            html += f"<p><strong>Total Secrets Found:</strong> {len(self.findings)}</p>"
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM']:
                if severity in by_severity:
                    html += f"<p><span class='{severity}'>{severity}</span>: {by_severity[severity]}</p>"
            html += "</div>"
        else:
            html += "<div class='summary'><p>✨ No secrets found!</p></div>"
    
    # Table
        html += """
        <h2>Findings</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Type</th>
                <th>File</th>
                <th>Line</th>
                <th>Match Preview</th>
            </tr>
        """
    
        for finding in self.findings:
            html += f"""
            <tr>
                <td class="{finding['severity']}">{finding['severity']}</td>
                <td>{finding['type']}</td>
                <td>{finding['file']}</td>
                <td>{finding['line']}</td>
                <td><code>{finding['match_preview']}</code></td>
            </tr>
            """
    
        html += """
        </table>
        </body>
        </html>
        """
    
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
        print(f"📄 HTML report saved to {output_file}")