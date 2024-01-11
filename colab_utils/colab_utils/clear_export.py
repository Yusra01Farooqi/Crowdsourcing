import os
import shutil

def empty_export():
    # Get the path to the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Dynamic path to the 'export' directory within the parent directory
    export_directory = os.path.join(script_directory, '..', 'export')

    os.system(f'rm -r {export_directory}')
    os.system(f'mkdir {export_directory}')
    os.system(f'mkdir {os.path.join(export_directory, "zip")}')

    # Create an empty .gitkeep file in the target directory (gitkeep not visible in Colab!)
    gitkeep_path = os.path.join(export_directory, 'zip', '.gitkeep')
    with open(gitkeep_path, 'w') as gitkeep_file:
        # Write an empty string to the file
        gitkeep_file.write('')

really_delete = input('Type "yes" to really delete all EXPORT data: ')
if really_delete == 'yes':
    empty_export()
    print('Emptied all export directories')
else:
    print('Canceled deletion!')
