import os
import shutil
import argparse

def create_gitkeep(target_directory_path):
    gitkeep_path = os.path.join(target_directory_path, '.gitkeep')

    # Create an empty .gitkeep file in the target directory (gitkeep not visible in Colab!)
    with open(gitkeep_path, 'w') as gitkeep_file:
        # Write an empty string to the file
        gitkeep_file.write('')

    # Display the file path (optional)
    print(f'created .gitkeep: {gitkeep_path}')

def empty_directories(directory_path, target_directories):
    for root, dirs, files in os.walk(directory_path):
        for target_directory in target_directories:
            target_directory_path = os.path.join(root, target_directory)
            if os.path.isdir(target_directory_path): 
                try:
                    # Remove contents of the directory without removing the directory itself
                    for filename in os.listdir(target_directory_path):
                        file_path = os.path.join(target_directory_path, filename)
                        try:
                            if os.path.isfile(file_path): 
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            print(f'Failed to delete {file_path}: {e}')
                    print(f'Emptied {target_directory_path}')

                    # Create a .gitkeep file after emptying the directory
                    create_gitkeep(target_directory_path)
                except Exception as e:
                    print(f'\nFailed to empty {target_directory_path}: {e}')

def main():
    parser = argparse.ArgumentParser(description='Empty specified directories and create .gitkeep files.')
    parser.add_argument('--target_directories', nargs='+', default=['csv', 'files'], help='List of target directories to empty')

    args = parser.parse_args()
    
    results_directory = '/content/cs_sem_template/results/'
    target_directories = args.target_directories

    really_delete = input('Type "yes" to really delete all RESULT data: ')
    if really_delete == 'yes':
        empty_directories(results_directory, target_directories)
        print('Emptied all result directories')
    else:
        print('Canceled deletion!')

if __name__ == "__main__":
    main()
