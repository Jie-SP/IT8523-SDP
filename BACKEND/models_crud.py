from extensions import db
from sqlalchemy import text, exc
 
def create_user_tables():
    user_task_sql = text("""
        CREATE TABLE IF NOT EXISTS Task (
            taskId INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            points INT,
            image_url TEXT
        )ENGINE=InnoDB;
    """)

    task_progress_sql = text("""
        CREATE TABLE IF NOT EXISTS TaskProgress (
            progressId INT AUTO_INCREMENT PRIMARY KEY,
            userId INT NOT NULL,
            taskId INT NOT NULL,
            completion_date TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (userId) REFERENCES user(userId),
            FOREIGN KEY (taskId) REFERENCES Task(taskId)
        )ENGINE=INNODB;
    """)

    user_table_sql = text("""
        CREATE TABLE IF NOT EXISTS user (
            userId INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100)
        )ENGINE=INNODB;
    """)

    with db.engine.begin() as connection:
        connection.execute(user_task_sql)
        connection.execute(task_progress_sql)
        connection.execute(user_table_sql)
 
def initialize_database():
    """Create user tables if they don't exist before the first request."""
    create_user_tables()


# create task
def create_task(name, description, points, image_url):
    try:
        create_task_sql = text ("""
            INSERT INTO Task (name, description, points, image_url) 
            VALUES (:name, :description, :points, :image_url)
        """)

        db.session.execute(create_task_sql, {'name': name, 'description': description, 'points': points, 'image_url': image_url})
        task = db.session.execute(text('SELECT LAST_INSERT_ID()')).fetchone()[0]
        db.session.commit()

        return task
    except Exception as e:
        db.session.rollback()
        raise e
