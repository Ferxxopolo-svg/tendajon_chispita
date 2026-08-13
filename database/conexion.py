import psycopg2

def Conexion():
    return psycopg2.connect(
        dbname="tendajon_chispita",
        user="postgres",
        password="donanfermc",
        host="localhost",
        port="5432"
    )