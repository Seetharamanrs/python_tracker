import sqlite3

def add_expenses():
    conn=sqlite3.connect("tracker.db")

    cursor=conn.cursor()

    amount=float(input("Enter expense amount: "))
    category=input("Enter Category (food/travel/other): ")
    date=input("Enter date (DD-MM-YYYY): ")


    cursor.execute(
        "INSERT INTO Expenses (amount,category,date) VALUES(?,?,?)",
        (amount, category, date)
    )

    conn.commit()
    conn.close()


    print("Expenses saved successfully!")

def view_expenses():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM Expenses")
    rows=cursor.fetchall()

    print("\n--- Your Expenses ---")
    for row in rows:
        print(f"ID{row[0]}| Amount: {row[1]} | category: {row[2]} | Date: {row[3]}")  
    print("-------------\n")
    conn.close()


def total_expenses():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("SELECT sum(amount) FROM Expenses")
    total=cursor.fetchone()[0]

    if total is None:
        total=0
    print(f"\n Total money spent: {total}\n")
    conn.close()

def delete_expenses():
    view_expenses()
    expense_id=input("Enter the ID to Delete: ")

    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("DELETE FROM Expenses WHERE id=?", (expense_id,))
    if cursor.rowcount==0:
        print("ID not found please provide correct ID")
    else:
        print("Expenses Deleted Sucessfully! ")
    conn.commit()
    conn.close()
    

def update_expenses():
    view_expenses()
    expense_id=input("Enter the ID to update: ")
    new_amount=input("Enter new amount: ")

    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    conn.execute("UPDATE Expenses SET amount=? WHERE id=?",(new_amount,expense_id))
    if cursor.rowcount==0:
        print("No Expenses found with that ID.")
    else:
        print("Expenses updated Sucessfully!")
    conn.commit()
    conn.close()


while True:
    print("1. Add Expenses")
    print("2. View Expenses")
    print("3. Total Expenses")
    print("4. Delete Expenses")
    print("5. Update Expenses")
    print("6. Exit")

    choice= input("Choose option: ")

    if choice=="1":
        add_expenses()
    elif choice=="2":
        view_expenses()
    elif choice=="3":
        total_expenses()
    elif choice=="4":
        delete_expenses()
    elif choice=="5":
        update_expenses()
    elif choice=="6":
        print("Thank you!") 
        break
    else:
        print("Invaild choice. Try again. \n ")   

