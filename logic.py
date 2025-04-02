#Gerekli kütüphanelerin kod dosyasının içine aktarılması.

import sqlite3
from config import DATABASE

#Bazı tablo oluşumları

skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Discord']) ]
statuses = [ (_,) for _ in (['Prototip Oluşturma', 'Geliştirme Aşamasında', 'Tamamlandı, kullanıma hazır', 'Güncellendi', 'Tamamlandı, ancak bakımı yapılmadı']) ]

#Database bağlantısı

class DB_Manager:
    def __init__(self, database):
        self.database = database
    
    #Tablo oluşturma
        
        

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:

            #Projects tablosu  

            conn.execute('''CREATE TABLE IF NOT EXISTS projects (
                            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 

           #Skills tablosu

            conn.execute('''CREATE TABLE IF NOT EXISTS skills (
                            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            skill_name TEXT UNIQUE
                        )''')

            #project_skills tablosu

            conn.execute('''CREATE TABLE IF NOT EXISTS project_skills (
                            project_id INTEGER,
                            skill_id INTEGER,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id),
                            PRIMARY KEY (project_id, skill_id)
                        )''')

            #status tablosu

            conn.execute('''CREATE TABLE IF NOT EXISTS status (
                            status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            status_name TEXT UNIQUE
                        )''')

            #users tablosu

            conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name TEXT UNIQUE
                        )''')

            #usets_projects tablosu

            conn.execute('''CREATE TABLE IF NOT EXISTS user_projects (
                            user_id INTEGER,
                            project_id INTEGER,
                            FOREIGN KEY(user_id) REFERENCES users(user_id),
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            PRIMARY KEY (user_id, project_id)
                        )''')
            
            conn.commit()

    #sql sorguları

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data=tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def default_insert(self):
        self.__executemany('INSERT OR IGNORE INTO skills (skill_name) VALUES(?)', skills)
        self.__executemany('INSERT OR IGNORE INTO status (status_name) VALUES(?)', statuses)

    def insert_project(self, data):
        sql = '''INSERT INTO projects (user_id, project_name, description, url, status_id) 
                 VALUES (?, ?, ?, ?, ?)'''
        self.__executemany(sql, data)

    def insert_skill(self, user_id, project_name, skill):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        res = self.__select_data(sql, (project_name, user_id))
        if res:
            project_id = res[0][0]
            skill_id = self.__select_data('SELECT skill_id FROM skills WHERE skill_name = ?', (skill,))
            if skill_id:
                data = [(project_id, skill_id[0][0])]
                self.__executemany('INSERT OR IGNORE INTO project_skills VALUES(?, ?)', data)

    def get_statuses(self):
        sql = "SELECT * FROM status"
        return self.__select_data(sql)

    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        return res[0][0] if res else None

    def get_projects(self, user_id):
        sql = "SELECT project_id, project_name, description, url, status_id FROM projects WHERE user_id = ?"
        return self.__select_data(sql, (user_id,))

    def get_project_id(self, project_name, user_id):
        sql = "SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?"
        res = self.__select_data(sql, (project_name, user_id))
        return res[0][0] if res else None

    def get_skills(self):
        return self.__select_data('SELECT * FROM skills')

    def get_project_skills(self, project_name):
        sql = '''SELECT skill_name FROM skills 
                 JOIN project_skills ON skills.skill_id = project_skills.skill_id 
                 JOIN projects ON projects.project_id = project_skills.project_id 
                 WHERE project_name = ?'''
        res = self.__select_data(sql, (project_name,))
        return ', '.join([x[0] for x in res])

    def get_project_info(self, user_id, project_name):
        sql = '''SELECT project_name, description, url, status_name 
                 FROM projects 
                 JOIN status ON status.status_id = projects.status_id
                 WHERE project_name = ? AND user_id = ?'''
        return self.__select_data(sql, (project_name, user_id))

    def update_projects(self, param, data):
        sql = f"UPDATE projects SET {param} = ? WHERE project_id = ?"
        self.__executemany(sql, [data])

    def delete_project(self, user_id, project_id):
        sql = "DELETE FROM projects WHERE user_id = ? AND project_id = ?"
        self.__executemany(sql, [(user_id, project_id)])

    def delete_skill(self, project_id, skill_id):
        sql = "DELETE FROM project_skills WHERE project_id = ? AND skill_id = ?"
        self.__executemany(sql, [(project_id, skill_id)])

#kodun doğru düzgün çalışması için  komut

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
    print(manager.get_statuses())

    
