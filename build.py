import subprocess

subprocess.run(['python', 'db_schema_bootstrap.py'])
subprocess.run(['pyinstaller', 'main.py'])