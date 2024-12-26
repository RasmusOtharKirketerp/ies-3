#add rewrite_text to db
import sqlite3
     
def add_rewrite_text_to_db():
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    cursor.execute('''    
         ALTER TABLE articles ADD COLUMN rewrite_text TEXT DEFAULT NULL
     ''')  
    conn.commit()
    conn.close()
   
if __name__ == '__main__':
    add_rewrite_text_to_db()


