import os
import subprocess
import pandas as pd
from datetime import datetime

# Function to get file timestamps
def get_files_with_timestamps():
    files = {}
    for root, dirs, filenames in os.walk('.'):
        # Skip unwanted directories
        if any(skip in root for skip in ['.git', 'venv', '__pycache__', '.idea', 'node_modules']):
            continue
        
        for filename in filenames:
            # Only include Python files and key config files
            if filename.endswith(('.py', '.txt', '.xlsx', '.csv', '.html', '.css')) or filename in ['Procfile', 'requirements.txt']:
                filepath = os.path.join(root, filename)
                filepath = filepath.replace('./', '', 1)  # Remove leading ./
                try:
                    stat = os.stat(filepath)
                    files[filepath] = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
    return files

# Get local files
print("Getting local files...")
local_files = get_files_with_timestamps()

# Get remote files
print("Switching to remote branch...")
subprocess.run(['git', 'checkout', 'origin-main'], capture_output=True)
remote_files = get_files_with_timestamps()

# Switch back
print("Switching back to main...")
subprocess.run(['git', 'checkout', 'main'], capture_output=True)

# Create comparison
all_files = sorted(set(local_files.keys()) | set(remote_files.keys()))
data = []

for file in all_files:
    local_time = local_files.get(file, '')
    remote_time = remote_files.get(file, '')
    
    # Determine which is newer
    if local_time and remote_time:
        newer = 'Local' if local_time > remote_time else 'Remote' if remote_time > local_time else 'Same'
    elif local_time:
        newer = 'Local only'
    elif remote_time:
        newer = 'Remote only'
    else:
        newer = 'Unknown'
    
    data.append({
        'File': file,
        'Local Timestamp': local_time,
        'Remote Timestamp': remote_time,
        'Newer Version': newer
    })

df = pd.DataFrame(data)

# Add summary sheet
summary_data = {
    'Category': ['Total Files', 'Local Only', 'Remote Only', 'Both Repos', 'Local Newer', 'Remote Newer', 'Same Timestamp'],
    'Count': [
        len(df),
        len(df[df['Newer Version'] == 'Local only']),
        len(df[df['Newer Version'] == 'Remote only']),
        len(df[(df['Local Timestamp'] != '') & (df['Remote Timestamp'] != '')]),
        len(df[df['Newer Version'] == 'Local']),
        len(df[df['Newer Version'] == 'Remote']),
        len(df[df['Newer Version'] == 'Same'])
    ]
}
summary_df = pd.DataFrame(summary_data)

# Write to Excel with multiple sheets
with pd.ExcelWriter('repository_comparison.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    df.to_excel(writer, sheet_name='File Details', index=False)
    
    # Auto-adjust column widths
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

print(f'Created repository_comparison.xlsx with {len(df)} files')
print(f'Local only: {len(df[df["Newer Version"] == "Local only"])}')
print(f'Remote only: {len(df[df["Newer Version"] == "Remote only"])}')
print(f'Local newer: {len(df[df["Newer Version"] == "Local"])}')
print(f'Remote newer: {len(df[df["Newer Version"] == "Remote"])}')