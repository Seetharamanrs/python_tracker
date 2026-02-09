import sqlite3
conn=sqlite3.connect("tracker.db")
cursor=conn.cursor()

print("You saved expenses:\n")

cursor.execute("SELECT * FROM Expenses")

rows=cursor.fetchall()

for row in rows:
    print("ID", row[0])
    print("Amount",row[1])
    print("category",row[2])
    print("Date",row[3])
    print("-------------------")

conn.close()

