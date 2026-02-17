import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_table():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    date TEXT
);
                   """)
    conn.commit()
    conn.close()
def add_expenses():
    from datetime import datetime
     
    conn=sqlite3.connect("tracker.db")

    cursor=conn.cursor()


    name=input("Enter Category (food/travel/other): ")
    while True:
        try:
            amount=float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Please enter the valid number")
    # date=input("Enter date (DD-MM-YYYY): ")
    date=datetime.now().strftime("%Y-%m-%d")


    cursor.execute(
        "INSERT INTO Expenses (name,amount,date) VALUES(?,?,?)",
        (name,amount, date)
    )

    conn.commit()
    conn.close()


    print("Expenses saved successfully!")

def view_expenses():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM Expenses")
    rows=cursor.fetchall()

    print("\nID | Name | Amount | Date")
    print('-'*35)

    for row in rows:
        print(row[0], "|",row[1],"|", row[2],"|", row[3])  
    conn.close()


def total_expenses():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("SELECT sum(amount) FROM Expenses")
    total=cursor.fetchone()[0]

    if total is None:
        total=0
    else:
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

def search_expenses():
    keyword=input("Enter name to search: ")

    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM Expenses WHERE name LIKE ?", ( "%"+ keyword +"%",))
    results=cursor.fetchall()

    if len(results)==0:
        print("No matching expenses found")
    else:
        for r in results:
            print(r)
    
    conn.close()

def export_csv():
    conn=sqlite3.connect("tracker.db")
    query="SELECT * FROM Expenses"
    df=pd.read_sql_query(query,conn)

    if df.empty:
        print("No Data to export")
    df['date']=pd.to_datetime(df['date'])

    df['month']=df['date'].dt.strftime("%Y-%m")
    df['day_name']=df['date'].dt.day_name()

    monthly_summary = df.groupby('month')['amount'].sum().reset_index()
    df.to_csv("Expenses_full_report.csv", index=False)
    monthly_summary.to_csv("Monthly_summary.csv", index=False)  

    print("Reports Generated:")
    print(" - Expenses_full_report.csv")
    print(" - Monthly_summary.csv")  
    
    conn.close()
def plot_monthly_chart():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()
    query1="""SELECT strftime('%Y-%m',DATE("date")) AS month,
    SUM(amount) as total
    FROM Expenses 
    GROUP BY month
    ORDER BY month;
    """
    cursor.execute(query1)
    data=cursor.fetchall()

    if len(data)==0:
        print("No Data to plot sorry!")
        return
    month=[row[0]for row in data]
    totals=[row[1]for row in data]

    plt.figure()
    plt.plot(month,totals,marker='o')
    plt.xlabel("MONTHS")
    plt.ylabel("TOTAL SPENDING")
    plt.title("MONTHLY SPENDING CHART")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    conn.close()

# def monthly_summary():
#     conn=sqlite3.connect("tracker.db")
#     cursor=conn.cursor()

#     cursor.execute("""
#         SELECT  substr(date,1,7) AS month, SUM(amount)
#         FROM expenses
#         GROUP BY month
#         ORDER BY month
#                   """)
#     results=cursor.fetchall()

#     if len(results)==0:
#         print("No data available")
#     else:
#         print("\nMonthly Spending:")
#         print("-------------------")
#         for row in results:
#             print(row[0],":$",row[1])

    conn.close()
def cateogry_summary():
    conn=sqlite3.connect("tracker.db")
    cursor=conn.cursor()

    cursor.execute( """SELECT Name, SUM(amount)
            FROM Expenses    
            GROUP BY Name
            ORDER BY SUM(amount) DESC       
                   """)
    results = cursor.fetchall()

    print("\nSpending by Category")
    print("----------------------")

    for row in results:
        print(row[0], ": ₹", row[1])

    conn.close()

def monthly_report():
    conn=sqlite3.connect('tracker.db')
    cursor=conn.cursor()
    query=""" SELECT 
    strftime('%Y-%m',DATE("date"))AS month,
    SUM(amount) AS total_spent
FROM Expenses
GROUP BY month
ORDER BY month;
"""
    cursor.execute(query)
    rows=cursor.fetchall()
    print("\n Monthly spending")
    print("-------------------")
    for row in rows:
        print(f"{row[0]}:$ {row[1]}")
    conn.close()

def main():
    create_table()

    while True:
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Delete Expenses")
        print("5. Update Expenses")
        print("6. Search Expenses")
        # print("7. Monthly Summary")
        print("7. Category Summary")
        print("8. Monthly report")
        print("9. Monthly Chart")
        print("10. Export Report(CSV)")
        print("11. Exit")

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
            search_expenses()
        # elif choice=="7":
        #     monthly_summary()
        elif choice=="7":
            cateogry_summary()
        elif choice=="8":
            monthly_report()
        elif choice=="9":
            plot_monthly_chart()
        elif choice=="10":
            export_csv()
        elif choice=="11":
            print("Thank you!") 
            break
        else:
            print("Invaild choice. Try again. \n ")   



if __name__ =="__main__":
    main()

