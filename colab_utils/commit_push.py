import sys
import os
from datetime import datetime
import subprocess

auto_message = '--auto_message' in sys.argv[1:]
do_print = '--do_print' in sys.argv[1:]

try:
    if auto_message:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        commit_message = f'{current_time}: ran app'
    else:
        commit_message = input('Enter your (mandatory) commit message or leave empty to cancel: ')
        if not commit_message.strip():
            raise ValueError('Canceled! Commit message cannot be empty.')

    # Run git queries and capture output
    pull_output = subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT, text=True)
    add_output = subprocess.check_output(['git', 'add', '.'], stderr=subprocess.STDOUT, text=True)
    commit_output = subprocess.check_output(['git', 'commit', '-m', f'"{commit_message}"'], stderr=subprocess.STDOUT, text=True)
    push_output = subprocess.check_output(['git', 'push', 'origin', 'main'], stderr=subprocess.STDOUT, text=True)

    if do_print:
        print(pull_output)
        print(add_output)
        print(commit_output)
        print(push_output)

    print('Pushed to repo')

except subprocess.CalledProcessError as e:
  if do_print: #avoiding error for empty commits
    print(f'Failed to push to repo, please avoid version conflicts. Error: {e.output}')

except ValueError as e:
    print(f'Error: {str(e)}')

except Exception as e:
    print(f'An unexpected error occurred: {e}')


'''#alternative mitigating git log output
import os
from datetime import datetime
try:
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    commit_message = f'{current_time}: ran app'
    os.system('git pull')
    os.system('git add .')
    os.system(f'git commit -m "{commit_message}"')
    os.system('git push origin main')
    print('Pushed to repo')
except Exception as e:
    print(f'Failed to push to repo, please avoid version conflicts Error: {e}')
'''
