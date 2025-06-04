#BankViewCustomers.py
import oracledb

def view_customer(customer_id):
    """Fetch and display details of a single customer."""
    try:
        # Establish the database connection
        con = orc.connect("system/Oracle123@localhost/system")
            cur = con.cursor()
                # Prepare and execute the SQL query
            query = "SELECT * FROM customers WHERE customer_id = :id"
            cur.execute(query, id=customer_id)

                # Fetch and display the result
                row = cur.fetchone()
                if row:
                    print("Customer Details:")
                    print(f"ID: {row[0]}")
                    print(f"Name: {row[1]}")
                    print(f"Email: {row[2]}")
                    print(f"Phone: {row[3]}")
                else:
                    print(f"No customer found with ID {customer_id}.")
    except oracledb.Error as e:
        print(f"Database error occurred: {e}")

def view_customers():
    """Fetch and display details of all customers."""
    try:
        # Establish the database connection
        con = orc.connect("system/Oracle123@localhost/system")
            cur = con.cursor()
                # Execute the SQL query
                query = "SELECT * FROM customers"
                cur.execute(query)

                # Fetch and display all results
                rows = cur.fetchall()
                if rows:
                    print("All Customers:")
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Phone: {row[3]}")
                else:
                    print("No customers found.")
    except oracledb.Error as e:
        print(f"Database error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    customer_id = 101  # Replace with an actual customer ID
    view_customer(customer_id)
    view_customers()
