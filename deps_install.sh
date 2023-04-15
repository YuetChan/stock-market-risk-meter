#!/bin/sh

rm ./code_meta.desktop
python3 -m venv myenv
. myenv/bin/activate

pip install -r requirements.txt

python3 db_schema_bootstrap.py

pyinstaller main.py

deactivate

rm -r myenv

cp code_meta_template.desktop code_meta.desktop
cp -r resources ./dist/main/resources