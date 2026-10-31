import subprocess, sys
result = subprocess.run([sys.executable, '/home/robin/OneDrive/University and such/LoSoRe/tools/pascal/e6_match.py', '--target', 'stickman', '--panel', '--attempts', '2'], capture_output=True, text=True, timeout=280)
print(result.stdout[-3000:])
if result.stderr:
    print('STDERR:', result.stderr[-1000:])
print('RC:', result.returncode)
