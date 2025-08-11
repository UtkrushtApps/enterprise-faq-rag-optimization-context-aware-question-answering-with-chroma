import subprocess
import sys
commands = [
    ['python', 'scripts/fetch_documents.py'],
    ['python', 'scripts/process_fetched_docs.py'],
    ['python', 'scripts/process_documents.py'],
    ['python', 'scripts/verify_setup.py']
]
for i, cmd in enumerate(commands):
    print(f"\nRunning pipeline step {i+1}: {' '.join(cmd)}\n{'='*40}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        print(f"Step failed: {cmd}")
        sys.exit(1)
print("Pipeline completed successfully.")
