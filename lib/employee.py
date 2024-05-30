import sqlite3

CONN = sqlite3.connect('database.db')
CURSOR = CONN.cursor()

class Employee:
    all = {}

    def __init__(self, name, job_title, department_id, id=None):
        self.name = name
        self.job_title = job_title
        self.department_id = department_id
        self.id = id

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                job_title TEXT,
                department_id INTEGER
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()

    def save(self):
        if not self.id:
            CURSOR.execute("INSERT INTO employees (name, job_title, department_id) VALUES (?, ?, ?)",
                           (self.name, self.job_title, self.department_id))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE employees SET name = ?, job_title = ?, department_id = ? WHERE id = ?",
                           (self.name, self.job_title, self.department_id, self.id))
        CONN.commit()
        type(self).all[self.id] = self

    def delete(self):
        CURSOR.execute("DELETE FROM employees WHERE id = ?", (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        employee = cls.all.get(row[0])
        if employee:
            employee.name = row[1]
            employee.job_title = row[2]
            employee.department_id = row[3]
        else:
            employee = cls(row[1], row[2], row[3], row[0])
            cls.all[employee.id] = employee
        return employee

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM employees")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM employees WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM employees WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None