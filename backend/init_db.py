from db import get_connection

with open("schema.sql") as f:
    schema_sql = f.read()
conn = get_connection()
cursor = conn.cursor()
for statement in schema_sql.split(";"):
    if statement.strip():
        print("statement:", statement)
        cursor.execute(statement)
        conn.commit()
        print("Executed statement.")
cursor.close()
conn.close()
