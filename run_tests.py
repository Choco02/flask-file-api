from shutil import copy2
import hashlib
import os
from time import sleep

[ original_routes_path, test_routes_path ] = [ './routes.py', './tests/routes.py' ]
[ original_util_path, test_util_path ] = [ './util/util.py', './tests/util.py' ]
if 'routes.py' not in os.listdir('./tests') or 'util.py' not in os.listdir('./tests'):
    copy2(original_routes_path, test_routes_path)
    copy2(original_util_path, test_util_path)
elif 'routes.py' in os.listdir('.') and 'util.py' in os.listdir('.'):
    # Check file changes and update tests
    def check_file(original_file: str, test_file: str):
        original_file_hash = hashlib.sha256(open(original_file, 'rb').read()).hexdigest()
        test_file_hash = hashlib.sha256(open(test_file, 'rb').read()).hexdigest()

        if original_file_hash != test_file_hash:
            copy2(original_file, test_file)
    
    check_file(original_routes_path, test_routes_path)
    check_file(original_util_path, test_util_path)

print('\u001b[33;1m Preparing tests...\u001b[0m')
sleep(5)
os.system('pytest')
