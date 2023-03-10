import sqlite3

conn = None

def init(fname):
    global conn
    conn = sqlite3.connect(fname)


def caches_by_dir_n_commit(dir, commit_hash):
    global conn

    cursor = conn.cursor()
    cursor.execute("INSERT INTO dir_cache(dir, commit_hash) VALUES(?, ?) ON CONFLICT(dir) DO UPDATE SET commit_hash=?", 
                   (dir, commit_hash, commit_hash))
    
    num_rows_affected = cursor.rowcount

    print(f"{num_rows_affected} rows affected")

    conn.commit()


def checks_if_cache_exits(dir, commit_hash):
    global conn

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dir_cache WHERE dir=? AND commit_hash=?", 
                   (dir, commit_hash))

    row = cursor.fetchone()

    print(row)

    conn.commit()

    return row


def close():
    conn.close()