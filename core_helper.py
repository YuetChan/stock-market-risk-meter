import uuid
import json

class core_helper:

    def __init__(
            self, 
            conn
            ):
        self.conn = conn


    def init_project(
            self, 
            name
            ):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO project(id, name) VALUES(?, ?)", 
                   (str(uuid.uuid4()), name, ))

        num_rows_affected = cursor.rowcount
        self.conn.commit()
        
        return num_rows_affected


    def select_project_by_id(
            self, 
            id
            ):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM project WHERE id = ?", 
                   (id, ))

        row = cursor.fetchone()
        self.conn.commit()

        return row


    def add_note_by_filepath_n_project_id(
            self, 
            note, 
            plain_text_note,
            fpath, 
            project_id
            ):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO note(project_id, filepath, note, plain_text_note) VALUES(?, ?, ?, ?)", 
                   (project_id, fpath, note, plain_text_note))
        
        num_rows_affected = cursor.rowcount
        self.conn.commit()
        
        return num_rows_affected

    def select_filepaths_with_non_empty_plain_text_note_by_project_id_n_filepaths_in(self, project_id, fpaths):
        cursor = self.conn.cursor()
        cursor.execute("SELECT filepath FROM note WHERE project_id = ? and plain_text_note != '' and filepath IN {}".format(tuple(fpaths)), 
                       (project_id, ))
        
        rows = cursor.fetchall()
        self.conn.commit()

        return rows


    def select_filepaths_with_non_empty_plain_text_note_by_project_id_n_filepaths_not_in(self, project_id, fpaths):
        cursor = self.conn.cursor()
        cursor.execute("SELECT filepath FROM note WHERE project_id = ? and plain_text_note != '' and filepath NOT IN {}".format(tuple(fpaths)), 
                       (project_id, ))
        
        rows = cursor.fetchall()
        self.conn.commit()

        return rows


    def select_note_by_filepath_n_project_id(
            self, 
            fpath, 
            project_id
            ):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT note FROM note WHERE filepath = ? AND project_id = ?", 
                    (fpath, project_id, ))

        row = cursor.fetchone()
        self.conn.commit()

        return row
    

    def search_filepaths_by_project_id(
            self, 
            project_id
            ):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT filepaths FROM note WHERE project_id = ?", 
                    (project_id, ))

        row = cursor.fetchall()
        self.conn.commit()

        return row


    def init_config(
            id, 
            name, 
            fpaths):
        json_data = {
          "id": id,
          "name": name,
          "filepaths": fpaths
        }

        with open("s_config.json", "w") as outfile:
            json.dump(json_data, outfile)

