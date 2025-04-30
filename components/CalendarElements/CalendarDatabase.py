import sqlite3

# singleton
class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('calendar.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS date (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         day INTEGER,
                         month INTEGER,
                         year INTEGER
                         )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS journal (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         date_id INTEGER,
                         journal TEXT,
                         mood_score INTEGER,
                         FOREIGN KEY (date_id) REFERENCES date(id)
                         )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                         daily_task_id INTEGER,
                         date_id INTEGER,
                         desc TEXT,
                         completed INTEGER,
                         FOREIGN KEY (date_id) REFERENCES date(id)
                         )""")
        self.conn.commit()

    def add_task_to_day(self, date_id,index, desc):
        self.cursor.execute("""INSERT INTO task (daily_task_id, date_id, desc, completed)
                                  VALUES (?,?,?,?)
        """,(index, date_id, desc, 0))
        self.conn.commit()

    def complete_task_from_day(self,date_id,daily_task_id):
        self.cursor.execute("""UPDATE task 
                                  SET completed = ?
                                  WHERE date_id = ? AND daily_task_id = ?""", (1, date_id, daily_task_id))
        self.conn.commit()

    def add_to_journal(self, date_id, desc, mood_score):
        self.cursor.execute("""INSERT INTO journal (date_id, journal, mood_score) 
                                  VALUES (?,?,?)
                                """,(date_id,desc,mood_score))
        self.conn.commit()
    
    def fetch_tasks_from_day(self,date_id):
        self.cursor.execute("""SELECT * FROM tasks WHERE date_id = ?""",(date_id,))
        return self.cursor.fetchall()
        
    def get_date_id_from_date(self,day,month,year):
        self.cursor.execute("""SELECT id FROM date WHERE day = ? 
                                  AND month = ? 
                                  AND year = ?""", (day,month,year))
        result = self.cursor.fetchone()
        return result[0] if result else None
