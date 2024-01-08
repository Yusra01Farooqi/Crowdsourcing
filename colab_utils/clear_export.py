import os
import shutil

def empty_export():
  os.system('rm -r /content/cs_sem_template/export')
  os.system('mkdir /content/cs_sem_template/export')
  os.system('mkdir /content/cs_sem_template/export/zip')

  # Create an empty .gitkeep file in the target directory (gitkeep not visible in Colab!)
  with open('/content/cs_sem_template/export/zip/.gitkeep', 'w') as gitkeep_file:
      # Write an empty string to the file
      gitkeep_file.write('')

really_delete = input('Type "yes" to really delete all EXPORT data: ')
if really_delete == 'yes':
    empty_export()
    print('Emptied all export directories')
else:
    print('Canceled deletion!')