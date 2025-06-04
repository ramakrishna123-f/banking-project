#BankDeposit.py
import oracledb as orc
from BankExcept import DepositError

def deposit():
    try:
        # Connect to Oracle database
        con = orc.connect("system/Oracle123@localhost/system")
        cur = con.cursor()

        # Input and validate account number
        accno = input("Enter Your 11-digit Account Number: ").strip()
        if not accno.isdigit() or len(accno) != 11:
            print("❌ Invalid account number format.")
            return
        accno = int(accno)

        # Check if account exists
        cur.execute("SELECT BAL FROM South_Indian_Asian_Bank WHERE ACNO = :1", [accno])
        result = cur.fetchone()
        if not result:
            print("❌ Account not found.")
            return
        current_bal = result[0]

        # Input and validate deposit amount
        try:
            damt = float(input("Enter your deposit amount: ").strip())
            if damt <= 0:
                raise DepositError("You must deposit a positive amount.")
        except DepositError as e:
            print(f"❌ DepositError: {e}")
            return
        except ValueError:
            print("❌ Invalid amount entered.")
            return

        # Update balance in the database
        new_bal = current_bal + damt
        cur.execute("UPDATE South_Indian_Asian_Bank SET BAL = :1 WHERE ACNO = :2", (new_bal, accno))
        con.commit()

        # Output success message
        print(f"\n✅ Your account xxxxxxx{str(accno)[-3:]} credited with ₹{damt:.2f}")
        print(f"💰 New balance: ₹{new_bal:.2f}")

    except orc.DatabaseError as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass

# Run the function if this script is executed directly
if __name__ == "__main__":
    deposit()




