from database.creation import conn_to_db


def fetch_customer_data():
    conn = conn_to_db()

    if not conn:
        return []

    dist = conn.cursor()
    dist.execute("SELECT * FROM ewii_customer_data;")
    data = dist.fetchall()
    
    dist.close()
    conn.close()
    return data