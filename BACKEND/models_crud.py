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

    user_table_sql = text("""
        CREATE TABLE IF NOT EXISTS user (
            userId INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(100)
        )ENGINE=INNODB;
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

    with db.engine.begin() as connection:
        connection.execute(user_task_sql)
        connection.execute(user_table_sql)
        connection.execute(task_progress_sql)
 
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

        result = db.session.execute(create_task_sql, {
            'name': name,
            'description': description,
            'points': points,
            'image_url': image_url
        })

        db.session.commit()

        return {'taskId': result.lastrowid,
                'name': name,
                'description': description,
                'points': points,
                'image_url': image_url
        }
    
    except Exception as e:
        db.session.rollback()
        raise e

# Update task by task_id
def update_task(taskId, name, desc, points, image_url):
    try:
        update_task_sql = text("""
        UPDATE Task
        SET name = :name,
            description = :desc,
            points = :points,
            image_url = :image_url
        WHERE
            taskId = :taskId
        """)

        result = db.session.execute(update_task_sql, {
            'taskId': taskId,
            'name': name,
            'desc': desc,
            'points': points,
            'image_url': image_url
        })
        
        db.session.commit()
        
        if result.rowcount > 0:
            return {"taskId": taskId,
                    'name': name,
                    'desc': desc,
                    'points': points,
                    'image_url': image_url
            }
        else:
            return {"error": "update error"}
    except Exception as e:
        db.session.rollback()
        raise e