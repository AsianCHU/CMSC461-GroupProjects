from datetime import datetime
import sqlite3

DATE_FORMAT = "%m-%d-%y"

quitApp = False

db_name = "project.db"


# Row factory that returns each row as a dict with column names mapped to values
# https://docs.python.org/3/library/sqlite3.html
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


connection = sqlite3.connect(db_name)
connection.row_factory = dict_factory
# Enable foreign key support
# https://sqlite.org/foreignkeys.html
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()


def print_rows(rows):
    if not rows:
        print("No row results.")
        return

    col_count = max([len(x) for x in rows])
    # Rental end_date in ISO format is 19 characters long
    row_format = "{:>20}  " * col_count

    # Print column headers
    print(row_format.format(*rows[0].keys()))
    for row in rows:
        # Print row values
        print(row_format.format(*[str(x)[:20] for x in row.values()]))


def delete_agency(agency_name: str):
    try:
        cursor.execute(
            "DELETE FROM agency WHERE agency_name = ?",
            [agency_name],
        )
        print(f"{cursor.rowcount} rows deleted.")
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")


def insert_agency(agency_name: str, address: str, city: str, phone: str):
    try:
        cursor.execute(
            "INSERT INTO agency (agency_name, address, city, phone) VALUES (?, ?, ?, ?)",
            [agency_name, address, city, phone],
        )
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")


def select_agency():
    try:
        cursor.execute("SELECT * FROM agency")
        rows = cursor.fetchall()
        print_rows(rows)
    except Exception as e:
        print(f"Error: {e}")


def insertOffice(name: str, city: str, area: int):
    try:
        cursor.execute(
            "INSERT INTO office (office_name, city, area) VALUES (?, ?, ?)",
            [name, city, area],
        )
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")


def getOffice():
    try:
        cursor.execute("SELECT * FROM office")
        rows = cursor.fetchall()
        print_rows(rows)
    except Exception as e:
        print(f"Error: {e}")


def deleteOffice(name):
    try:
        cursor.execute("DELETE FROM office WHERE office_name = ?", [name])
        print(f"{cursor.rowcount} rows deleted.")
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")


def delete_rental(rental_id: int):
    try:
        cursor.execute(
            "DELETE FROM agency_and_rental WHERE rental_id = ?",
            [rental_id],
        )
        cursor.execute(
            "DELETE FROM rental WHERE rental_id = ?",
            [rental_id],
        )
        print(f"{cursor.rowcount} rows deleted.")
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()


def insert_rental(agency_id: int, office_name: str, amount: float, end_date: datetime):
    try:
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
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()


def select_rental():
    try:
        cursor.execute("SELECT * FROM rental")
        rows = cursor.fetchall()
        print_rows(rows)
    except Exception as e:
        print(f"Error: {e}")


def parse_and_validate(attr, value):
    """
    Parse and validate a user-entered value.

    :param attr:
        column name
    :param value:
        value to parse
    :returns:
        parsed value
    :raises ValueError:
        if parsing/validation failed
    """
    if attr == "end_date":
        try:
            return datetime.strptime(value, DATE_FORMAT)
        except ValueError as e:
            print(f'Dates should be in "MONTH-DAY-YEAR" format.')
            raise ValueError()
    elif attr in ("agency_id"):
        try:
            value = int(value)
        except ValueError as e:
            print(f"Enter a valid primary key.")
            raise ValueError()

    return value


# Menu items
# Top-level tuples are: (label, submenu items)
# Submenu item tuples are: (label, database function, and column names)
# Submenu items with None as database function are used to exit the submenu
MENU_ITEMS = [
    (
        "Insert Agency",
        insert_agency,
        ("agency_name", "address", "city", "phone"),
    ),
    ("Select Agency", select_agency, None),
    ("Delete Agency", delete_agency, ("agency_name",)),
    ("Insert Office", insertOffice, ("office_name", "city", "area")),
    ("Select Office", getOffice, None),
    ("Delete Office", deleteOffice, ("office_name",)),
    (
        "Insert Rental",
        insert_rental,
        ("agency_id", "office_name", "amount", "end_date"),
    ),
    ("Select Rental", select_rental, None),
    ("Delete Rental", delete_rental, ("rental_id",)),
]


def execute_db_operation(db_op, attrs):
    values = []
    if attrs:
        # Get each column value from user
        for attr in attrs:
            # Loop until user value passes parsing and validation
            while True:
                try:
                    value = input(f"{attr.capitalize().replace('_', ' ')}: ")
                    value = parse_and_validate(attr, value)
                    values.append(value)
                    break
                except KeyboardInterrupt:
                    # Print a blank line after ^C
                    print()
                    # Allow Ctrl+C to cancel inputting values without exiting app
                    return
                except ValueError as e:
                    # Ignore values that fail parsing and validation
                    continue

    db_op(*values)


def main_menu():
    """
    Display a menu listing database operations for different record types.
    """
    while True:
        try:
            print("- GSA Database -")

            # Display labels for menu items
            for i, (label, _, _) in enumerate(MENU_ITEMS):
                print(f"{i+1}) {label}")

            print("q) Quit")

            # Convert user input to array index
            choice = input("> ")

            # Check for quit choice
            if choice.strip().lower() in ("0", "q"):
                return

            (label, db_op, attrs) = MENU_ITEMS[int(choice) - 1]

            if db_op:
                print(f"{label}? (Ctrl+C to cancel)")
                execute_db_operation(db_op, attrs)
            else:
                return
        except IndexError:
            # Ignore invalid menu choices
            pass
        except KeyboardInterrupt:
            # Print a blank line after ^C
            print()
            return
        except ValueError:
            # Ignore invalid menu choices
            pass


main_menu()

# at end of program
connection.close()
