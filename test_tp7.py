import os
from tools.pascal.tp7_fix import auto_tp7_fix

base = '/home/robin/OneDrive/University and such/LoSoRe/reports/overnight_stickman'
fn = 'FUN_0000_0075'
dir_path = os.path.join(base, fn)
base_files = [f for f in os.listdir(dir_path) if f.startswith('base')]
if base_files:
    with open(os.path.join(dir_path, base_files[0])) as bf:
        pas_content = bf.read()
    result = auto_tp7_fix(pas_content, fn, max_iterations=1)
    print('compile_ok: ' + str(result.get('compile_ok')))
    print('iterations: ' + str(result.get('iterations')))
    print('fixed first 300: ' + result.get('fixed', '')[:300])
