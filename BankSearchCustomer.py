# BankSearchCustomer.py
import oracledb as orc
from BankExcept import DepositError, WithdrawError, InsufficientFundsError

def connect_db():
    """Establish and return a new database connection."""
    try:
        return orc.connect("system/Oracle123@localhost/system")
    except orc.DatabaseError as e:
        print(f"❌ Database connection failed: {e}")
        return None

def get_balance(cursor, accno):
    """Retrieve the current balance for the given account number."""
    cursor.execute("SELECT BAL FROM South_Indian_Asian_Bank WHERE ACNO = :1", [accno])
    result = cursor.fetchone()
    return result[0] if result else None

def update_balance(cursor, accno, new_balance):
    """Update the account balance in the database."""
    cursor.execute("UPDATE South_Indian_Asian_Bank SET BAL = :1 WHERE ACNO = :2", (new_balance, accno))

def deposit():
    """Handle the deposit transaction."""
    accno = input("Enter your 11-digit Account Number: ").strip()
    if not accno.isdigit() or len(accno) != 11:
        print("❌ Invalid account number.")
        return

    try:
        damt = float(input("Enter your deposit amount: "))
        if damt <= 0:
            raise DepositError("You must deposit a positive amount.")
    except DepositError as e:
        print(f"❌ DepositError: {e}")
        return
    except ValueError:
        print("❌ Invalid amount entered.")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            bal = get_balance(cur, accno)
            if bal is None:
                print("❌ Account not found.")
                return

            new_balance = bal + damt
            update_balance(cur, accno, new_balance)
            con.commit()

            print(f"\n✅ ₹{damt:.2f} deposited successfully.")
            print(f"💰 New Balance: ₹{new_balance:.2f}")
        except orc.DatabaseError as e:
            print(f"❌ Database error: {e}")
        finally:
            con.close()

def withdraw():
    """Handle the withdrawal transaction."""
    accno = input("Enter your 11-digit Account Number: ").strip()
    if not accno.isdigit() or len(accno) != 11:
        print("❌ Invalid account number.")
        return

    try:
        wamt = float(input("Enter your withdrawal amount: "))
        if wamt <= 0:
            raise WithdrawError("You must withdraw a positive amount.")
    except WithdrawError as e:
        print(f"❌ WithdrawError: {e}")
        return
    except ValueError:
        print("❌ Invalid amount entered.")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            bal = get_balance(cur, accno)
            if bal is None:
                print("❌ Account not found.")
                return
            if (wamt + 500) > bal:
                raise InsufficientFundsError("Insufficient balance. Maintain minimum ₹500.")

            new_balance = bal - wamt
            update_balance(cur, accno, new_balance)
            con.commit()

            print(f"\n✅ ₹{wamt:.2f} withdrawn successfully.")
            print(f"💰 Remaining Balance: ₹{new_balance:.2f}")
        except (orc.DatabaseError, InsufficientFundsError) as e:
            print(f"❌ {type(e).__name__}: {e}")
        finally:
            con.close()

def balance_enquiry():
    """Display the current balance for the account."""
    accno = input("Enter your 11-digit Account Number: ").strip()
    if not accno.isdigit() or len(accno) != 11:
        print("❌ Invalid account number.")
        return

    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            bal = get_balance(cur, accno)
            if bal is None:
                print("❌ Account not found.")
                return

            print(f"💰 Account xxxxxxx{str(accno)[-3:]} Balance: ₹{bal:.2f}")
        except orc.DatabaseError as e:
            print(f"❌ Database error: {e}")
        finally:
            con.close()

if __name__ == "__main__":
    deposit()
    withdraw()
    balance_enquiry()


