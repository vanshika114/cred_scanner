import os

hook_content = '''#!/bin/bash
echo "Running secret scanner..."
python -m src.cli . --exclude README.md,examples/ --output /tmp/findings.json
if [ $? -ne 0 ]; then
    echo "Secrets found! Fix before committing."
    exit 1
fi
echo "No secrets found."
exit 0
'''

hook_path = '.git/hooks/pre-commit'
os.makedirs(os.path.dirname(hook_path), exist_ok=True)
with open(hook_path, 'w', encoding='utf-8') as f:
    f.write(hook_content)

os.chmod(hook_path, 0o755)
print("Pre-commit hook installed with exclusions")