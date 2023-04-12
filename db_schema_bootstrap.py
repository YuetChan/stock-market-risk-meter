import sqlite3

conn = sqlite3.connect('./resources/sc_note.db')
curosr = conn.cursor()

# Create the table(s) and define the schema
curosr.execute('CREATE TABLE IF NOT EXISTS project (id TEXT PRIMARY KEY, name TEXT )')
          
curosr.execute('CREATE TABLE IF NOT EXISTS note (project_id TEXT, filepath TEXT, note TEXT, plain_text_note TEXT, PRIMARY KEY (project_id, filepath))')

conn.commit()
conn.close()