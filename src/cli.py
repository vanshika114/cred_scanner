import argparse
from html import parser
import sys
from .scanner import SecretScanner

def main():
    parser = argparse.ArgumentParser(
        description='🔐 Secret Scanner - Find exposed credentials in your code'
    )
    parser.add_argument('path', help='Directory to scan')
    parser.add_argument('--output', '-o', default='findings.json', help='Output JSON file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all details')
    parser.add_argument('--html', action='store_true', help='Generate HTML report')
    parser.add_argument('--exclude', default='', help='Comma-separated files/folders to exclude')
    
    args = parser.parse_args()
    
    scanner = SecretScanner()
    findings = scanner.scan_directory(args.path, exclude=args.exclude)
    
    scanner.print_summary()
    if args.html:
        scanner.generate_html_report('reports/report.html')
    
    if findings:
        scanner.save_json(args.output)
        print(f"\n💾 Results saved to {args.output}")
        return 1  # Exit with error code if secrets found
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
