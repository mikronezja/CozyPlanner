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
                        initial_time INTEGER,
                        total_seconds INTEGER,
                        session_number INTEGER,
                        is_working INTEGER DEFAULT 1,
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
            with self.lock:
                self.cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
                result = self.cursor.fetchone()  

                if result is not None:
                    current_completed = result[0]
                    new_completed = 1 if current_completed == 0 else 0
                    self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", 
                                    (new_completed, task_id))
                    self.conn.commit()
                    return new_completed
                else:
                    print(f"[ERROR] Task with id {task_id} not found")
                    return None
        except Exception as db_error:
            print(f"[ERROR] w zmianie completion: {db_error}")
            return None

    def get_tasks(self, day, month, year):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("SELECT * FROM tasks WHERE date_id = ?", (date_id,))
        return self.cursor.fetchall()
    
    def get_tasks_from_month(self,month,year):
        self.cursor.execute("SELECT id from date WHERE month = ? AND year = ?", (month, year))
        id_list = self.cursor.fetchall()
        task_list = []

        for id in id_list:
            self.cursor.execute("SELECT * FROM tasks WHERE date_id = ?", (id,))
            task_list += self.cursor.fetchall()
        return task_list

    def get_tasks_from_year(self,year):
        self.cursor.execute("SELECT id from date WHERE year = ?", (year,))
        id_list = self.cursor.fetchall()
        task_list = []
        for id in id_list:
            self.cursor.execute("SELECT * FROM tasks WHERE date_id = ?", (id,))
            task_list += self.cursor.fetchall()
        return task_list

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

    def add_pomodoro(self, day, month, year, initial_time, total_seconds,session_number, is_working):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("INSERT INTO pomodoro (date_id, initial_time, total_seconds, session_number, is_working) VALUES (?,?,?,?,?)", 
                           (date_id, initial_time, total_seconds, session_number, is_working))
        self.conn.commit()
    
    def get_latest_pomodoro(self,day,month, year):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("SELECT * FROM pomodoro WHERE date_id = ? ORDER BY id DESC LIMIT 1", (date_id,))
        return self.cursor.fetchone()
    
    def sum_all_previous_pomodoros(self, day, month, year):
        latest = self.get_latest_pomodoro(day, month, year)
        if latest:
            id, date_id, initial_time, total_seconds, session_number, is_working = latest
            self.cursor.execute("""
                DELETE FROM pomodoro WHERE session_number = ? AND date_id = ?
            """, (session_number, date_id))
            self.conn.commit()
            self.add_pomodoro(day,month,year,initial_time,total_seconds,session_number,is_working)
    
    def get_pomodoros_from_day(self, day, month, year):
        date_id = self.get_date_id(day, month, year)
        self.cursor.execute("SELECT * FROM pomodoro WHERE date_id = ?", (date_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()