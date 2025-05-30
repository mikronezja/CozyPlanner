import sqlite3

class DatabaseManager:
    def __init__(self, db_name='calendar.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        import threading
        self.lock = threading.Lock()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS date (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         day INTEGER,
                         month INTEGER,
                         year INTEGER,
                         UNIQUE(day, month, year)
                         )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS journal (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         date_id INTEGER,
                         journal TEXT,
                         mood_score INTEGER,
                         FOREIGN KEY (date_id) REFERENCES date(id)
                         )""") # mood_score 1-5
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         date_id INTEGER,
                         name TEXT,
                         desc TEXT,
                         completed INTEGER DEFAULT 0,
                         urgency INTEGER,
                         importance INTEGER,
                         FOREIGN KEY (date_id) REFERENCES date(id)
                         )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pomodoro(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date_id INTEGER,
                        total_seconds INTEGER,
                        FOREIGN KEY (date_id) REFERENCES date(id)
                        )""")
        self.conn.commit()

    def get_date_id(self, day, month, year):
        self.cursor.execute("SELECT id FROM date WHERE day=? AND month=? AND year=?", 
                           (day, month, year))
        result = self.cursor.fetchone()
        
        if not result:
            self.cursor.execute("INSERT INTO date (day, month, year) VALUES (?,?,?)", 
                               (day, month, year))
            self.conn.commit()
            return self.cursor.lastrowid
        return result[0]

    def add_task(self, day, month, year, name, desc, urgency, importance):
        with self.lock:
            date_id = self.get_date_id(day, month, year)
            self.cursor.execute("""INSERT INTO tasks (date_id, name, desc, urgency, importance)
                                VALUES (?,?,?,?,?)""", 
                            (date_id, name, desc, urgency, importance))
            self.conn.commit()
            return self.cursor.lastrowid # zwraca jego id

    def change_task_completion(self, task_id):
        try: 
            with self.lock: # zeby wszystko bylo na jednym watku - wymaga tego sqlite3
                self.cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
                self.conn.commit()

                value = 1 if self.cursor.fetchone() == 0 else 0

                self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (value, task_id))
                self.conn.commit()
                return value
        except Exception as db_error:
            print(f"[ERROR] w dodawaniu do bazy danych: {db_error}")
            return None

    def get_tasks(self, day, month, year):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("SELECT * FROM tasks WHERE date_id = ?", (date_id,))
        return self.cursor.fetchall()

    def remove_task(self, task_id):
        with self.lock:
            self.cursor.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
            self.conn.commit()
    
    def get_date(self, date_id):
        self.cursor.execute("SELECT * FROM date WHERE id = ?", (date_id,))
        return self.cursor.fetchone()

    def get_task_with_id(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
        return self.cursor.fetchone()

    def add_journal(self, day, month, year, journal, mood_score):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("INSERT INTO journal (date_id, journal, mood_score) VALUES (?,?,?)", 
                           (date_id, journal, mood_score))
        self.conn.commit()

    def get_journal(self, day, month, year):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("SELECT * FROM journal WHERE date_id = ?", (date_id,))
        return self.cursor.fetchone()
    
    def change_journal(self, day, month, year, journal, mood_score):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("""
            UPDATE journal SET journal = ?, mood_score = ? WHERE date_id = ?
        """, (journal, mood_score, date_id))
        self.conn.commit()

    def add_pomodoro(self, day, month, year, seconds):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("INSERT INTO pomodoro (date_id, total_seconds) VALUES (?,?)", 
                           (date_id, seconds))
        self.conn.commit()

    def close(self):
        self.conn.close()