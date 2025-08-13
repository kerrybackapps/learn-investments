import os
import subprocess
import pandas as pd
from datetime import datetime

# Get all files in local repository
local_files = {}
for root, dirs, files in os.walk('.'):
    # Skip .git directory
    if '.git' in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        # Get timestamp
        try:
            stat = os.stat(filepath)
            local_files[filepath] = datetime.fromtimestamp(stat.st_mtime)
        except:
            pass

# Get files from remote branch
subprocess.run(['git', 'checkout', 'origin-main'], capture_output=True)
remote_files = {}
for root, dirs, files in os.walk('.'):
    if '.git' in root:
        continue
    for file in files:
        filepath = os.path.join(root, file)
        try:
            stat = os.stat(filepath)
            remote_files[filepath] = datetime.fromtimestamp(stat.st_mtime)
        except:
            pass

# Switch back to main
subprocess.run(['git', 'checkout', 'main'], capture_output=True)

# Create dataframe
all_files = set(local_files.keys()) | set(remote_files.keys())
data = []
for file in sorted(all_files):
    data.append({
        'File': file,
        'Local Timestamp': local_files.get(file, ''),
        'Remote Timestamp': remote_files.get(file, '')
    })

df = pd.DataFrame(data)
df.to_excel('file_comparison.xlsx', index=False)
print(f'Created file_comparison.xlsx with {len(df)} files')