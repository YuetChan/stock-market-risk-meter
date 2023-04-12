import subprocess

subprocess.run(['python3', 'db_schema_bootstrap.py'])
subprocess.run(['pyinstaller', 'main.py'])