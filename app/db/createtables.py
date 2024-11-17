import psycopg2
from app.db.users import conn_info


def create_tables():
    # Establish the connection
    conn = psycopg2.connect(
        database=conn_info.database,
        user=conn_info.user,
        password=conn_info.password,
        host=conn_info.host,
        port=conn_info.port
    )

    cursor = conn.cursor()

    # Queries to create tables
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS USERS (
        username VARCHAR(255) PRIMARY KEY,
        password VARCHAR(255),
        phone VARCHAR(50),
        email VARCHAR(255),
        name VARCHAR(255)
    );
    """

    create_user_purchase_query = """
    CREATE TABLE IF NOT EXISTS PURCHASES (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        value FLOAT,
        description TEXT,
        major_category INTEGER,
        general_category TEXT,
        FOREIGN KEY (username) REFERENCES USERS(username) ON DELETE CASCADE
    );
    """

    # Execute the table creation queries
    cursor.execute(create_user_table_query)
    cursor.execute(create_user_purchase_query)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
