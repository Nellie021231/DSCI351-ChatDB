import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="project"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")
tables = [row[0] for row in cursor.fetchall()]

schema = {}

for table in tables:
    cursor.execute(f"DESCRIBE `{table}`;")
    columns = cursor.fetchall()

    cursor.execute(f"""
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'project' AND TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL;
    """)
    fks = {(row[0], row[1], row[2]) for row in cursor.fetchall()}

    column_details = []
    for col in columns:
        colname = col[0]
        key = col[3]

        if key == 'PRI':
            note = "PK"
        elif any(colname == fk[0] for fk in fks):
            ref = [fk for fk in fks if fk[0] == colname][0]
            note = f"FK → {ref[1]}.{ref[2]}"
        else:
            note = ""

        column_details.append(f"{colname} {f'({note})' if note else ''}")

    schema[table] = column_details

cursor.close()
conn.close()

for table, columns in schema.items():
    print(f"{table}:\n  " + ",\n  ".join(columns) + "\n")
