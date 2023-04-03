import sqlite3

class db_connector:
  
  def __init__(
      self, 
      fname):
    self.conn = sqlite3.connect(fname)


  def close(self):
    self.conn.close()


  def get_connection(self):
    return self.conn

