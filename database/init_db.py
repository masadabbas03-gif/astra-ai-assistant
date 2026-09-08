from connection import get_connection

connection = get_connection()

cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS tasks (

    id INT AUTO_INCREMENT PRIMARY KEY,

    task_name VARCHAR(255),

    status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

connection.commit()

print("Table created successfully!")

cursor.close()

connection.close()
