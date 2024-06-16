import psycopg2

class DBConnection:
    def __init__(self, name, host, port, user, password):
        self.conn = psycopg2.connect(
            database= name,
            user=user,
            password=password,
            host=host,
            port=port
        )

    def db_conn_close(self):
        self.conn.close()