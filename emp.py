import sqlite3

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS employee (
    emp_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
""")
conn.commit()


def add_employee():
    emp_id = int(input("Enter Employee ID: "))
    name = input("Enter Name: ")
    department = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    try:
        cursor.execute(
            "INSERT INTO employee VALUES (?, ?, ?, ?)",
            (emp_id, name, department, salary)
        )
        conn.commit()
        print("Employee added successfully!")
    except sqlite3.IntegrityError:
        print("Employee ID already exists.")


def view_employees():
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()

    if not rows:
        print("\nNo employee records found.")
    else:
        print("\nEmployee Records")
        print("-" * 50)
        print("ID\tName\tDepartment\tSalary")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t₹{row[3]:,.2f}")


def search_employee():
    emp_id = int(input("Enter Employee ID: "))
    cursor.execute("SELECT * FROM employee WHERE emp_id=?", (emp_id,))
    row = cursor.fetchone()

    if row:
        print("\nEmployee Found")
        print("ID:", row[0])
        print("Name:", row[1])
        print("Department:", row[2])
        print("Salary:", row[3])
    else:
        print("Employee not found.")


def update_employee():
    emp_id = int(input("Enter Employee ID: "))

    cursor.execute("SELECT * FROM employee WHERE emp_id=?", (emp_id,))
    if cursor.fetchone():
        name = input("Enter New Name: ")
        department = input("Enter New Department: ")
        salary = float(input("Enter New Salary: "))

        cursor.execute("""
            UPDATE employee
            SET name=?, department=?, salary=?
            WHERE emp_id=?
        """, (name, department, salary, emp_id))

        conn.commit()
        print("Employee updated successfully!")
    else:
        print("Employee not found.")


def delete_employee():
    emp_id = int(input("Enter Employee ID: "))

    cursor.execute("SELECT * FROM employee WHERE emp_id=?", (emp_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM employee WHERE emp_id=?", (emp_id,))
        conn.commit()
        print("Employee deleted successfully!")
    else:
        print("Employee not found.")

# Main Menu
while True:
    print("\n========== Employee Management System ==========")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_employee()
    elif choice == "2":
        view_employees()
    elif choice == "3":
        search_employee()
    elif choice == "4":
        update_employee()
    elif choice == "5":
        delete_employee()
    elif choice == "6":
        print("Thank you!")
        break
    else:
        print("Invalid choice. Try again.")

conn.close()