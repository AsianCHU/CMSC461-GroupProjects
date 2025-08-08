import sqlite3
from datetime import date

db_name = 'project.db'
try:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    connection.execute("PRAGMA foreign_keys = 1")
except sqlite3.Error as e:
    print("Error connecting to database: {e}")
    exit()

def insert_office(office_name, city, area):
    cursor.execute('INSERT INTO office (office_name, city, area) VALUES (?, ?, ?)', 
    (office_name, city, area))
    connection.commit()

def select_office():
    cursor.execute('SELECT * FROM office')
    rows = cursor.fetchall()
    print(rows)

def delete_office(office_name):
    cursor.execute('DELETE FROM office WHERE office_name = ?', (office_name,))
    connection.commit()

def delete_agency(agency_name):
    cursor.execute(
        "DELETE FROM agency WHERE agency_name = ?",
        [agency_name],
    )
    print(f"{cursor.rowcount} rows deleted.")
    connection.commit()

def insert_agency(agency_name, address, city, phone):
    cursor.execute(
        "INSERT INTO agency (agency_name, address, city, phone) VALUES (?, ?, ?, ?)",
        [agency_name, address, city, phone],
    )
    connection.commit()

def select_agency():
    cursor.execute("SELECT * FROM agency")
    rows = cursor.fetchall()
    print(rows)

def delete_rental(rental_id):
    cursor.execute(
        "DELETE FROM rental WHERE rental_id = ?",
        [rental_id],
    )
    cursor.execute(
        "DELETE FROM agency_and_rental WHERE rental_id = ?",
        [rental_id],
    )
    print(f"{cursor.rowcount} rows deleted.")
    connection.commit()

def insert_rental(agency_id, office_name, amount, end_date):
    end_date = end_date.isoformat()

    cursor.execute(
        "INSERT INTO rental (office_name, amount, end_date) VALUES (?, ?, ?)",
        [office_name, amount, end_date],
    )

    rental_id = cursor.lastrowid
    cursor.execute(
        "INSERT INTO agency_and_rental (agency_id, rental_id) VALUES (?, ?)",
        [agency_id, rental_id],
    )

    connection.commit()

def select_rental():
    cursor.execute("SELECT * FROM rental")
    rows = cursor.fetchall()
    print(rows)

while True:
    print("Database Project 1 Menu")
    print("1. Insert into Office")
    print("2. Select from Office") 
    print("3. Delete from Office")
    print("4. Insert into Agency")
    print("5. Select from Agency")
    print("6. Delete from Agency")
    print("7. Insert into Rental")
    print("8. Select from Rental")
    print("9. Delete from Rental")
    print("0. Exit")
    
    choice = input("Enter menu option (0-9): ")
    
    if choice == "1":
        office_name = input("Enter office name: ")
        city = input("Enter city: ")
        area = int(input("Enter area: "))
        insert_office(office_name, city, area)
        print("Data inserted into OFFICE")
        
    elif choice == "2":
        print("Offices:")
        select_office()
        
    elif choice == "3":
        office_name = input("Enter office name to delete: ")
        delete_office(office_name)
        print("Data in OFFICE deleted")
        
    elif choice == "4":
        agency_name = input("Enter agency name: ")
        address = input("Enter address: ")
        city = input("Enter city: ")
        phone = input("Enter phone: ")
        insert_agency(agency_name, address, city, phone)
        print("Data in Agency inserted")
        
    elif choice == "5":
        print("Agencies:")
        select_agency()
        
    elif choice == "6":
        agency_name = input("Enter agency name to delete: ")
        delete_agency(agency_name)
        print("Data in Agency deleted")
        
    elif choice == "7":
        agency_id = int(input("Enter agency ID: "))
        office_name = input("Enter office name: ")
        amount = float(input("Enter rental amount: "))
        year = int(input("Enter end year (YYYY): "))
        month = int(input("Enter end month (MM): "))
        day = int(input("Enter end day (DD): "))
        end_date = date(year, month, day)

        insert_rental(agency_id, office_name, amount, end_date)
        print("Data in Rental inserted")
        
    elif choice == "8":
        print("Rentals:")
        select_rental()
        
    elif choice == "9":
        rental_id = int(input("Enter rental ID to delete: "))
        delete_rental(rental_id)
        print("Data in Rentals deleted")
        
    elif choice == "0":
        print("Exiting program...")
        break
    else:
        print("Invalid option! Please try again.")

connection.close()