# BankTransaction.py
import oracledb as orc
from BankExcept import DepositError, WithdrawError, InsufficientFundsError

# Global variable for balance (fetched from DB per account)
bal = 0.0

def connect_db():
    return orc.connect("system/Oracle123@localhost/system")

def deposit():
    global bal
    try:
        con = connect_db()
        cur = con.cursor()

        accno = input("Enter your 11-digit Account Number: ").strip()
        if not accno.isdigit() or len(accno) != 11:
            print("❌ Invalid account number.")
            return
        accno = int(accno)

        # Get current balance
        cur.execute("SELECT BAL FROM South_Indian_Asian_Bank WHERE ACNO = :1", [accno])
        result = cur.fetchone()
        if not result:
            print("❌ Account not found.")
            return
        bal = result[0]

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

        bal += damt
        cur.execute("UPDATE South_Indian_Asian_Bank SET BAL = :1 WHERE ACNO = :2", (bal, accno))
        con.commit()

        print(f"\n✅ ₹{damt:.2f} deposited successfully.")
        print(f"💰 New Balance: ₹{bal:.2f}")

    except orc.DatabaseError as e:
        print(f"❌ Database error: {e}")
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass

def withdraw():
    global bal
    try:
        con = connect_db()
        cur = con.cursor()

        accno = input("Enter your 11-digit Account Number: ").strip()
        if not accno.isdigit() or len(accno) != 11:
            print("❌ Invalid account number.")
            return
        accno = int(accno)

        # Get current balance
        cur.execute("SELECT BAL FROM South_Indian_Asian_Bank WHERE ACNO = :1", [accno])
        result = cur.fetchone()
        if not result:
            print("❌ Account not found.")
            return
        bal = result[0]

        try:
            wamt = float(input("Enter your withdrawal amount: "))
            if wamt <= 0:
                raise WithdrawError("You must withdraw a positive amount.")
            elif (wamt + 500) > bal:
                raise InsufficientFundsError("Insufficient balance. Maintain minimum ₹500.")
        except WithdrawError as e:
            print(f"❌ WithdrawError: {e}")
            return
        except InsufficientFundsError as e:
            print(f"❌ InsufficientFundsError: {e}")
            return
        except ValueError:
            print("❌ Invalid amount entered.")
            return

        bal -= wamt
        cur.execute("UPDATE South_Indian_Asian_Bank SET BAL = :1 WHERE ACNO = :2", (bal, accno))
        con.commit()

        print(f"\n✅ ₹{wamt:.2f} withdrawn successfully.")
        print(f"💰 Remaining Balance: ₹{bal:.2f}")

    except orc.DatabaseError as e:
        print(f"❌ Database error: {e}")
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass

def balance_enquiry():
    try:
        con = connect_db()
        cur = con.cursor()

        accno = input("Enter your 11-digit Account Number: ").strip()
        if not accno.isdigit() or len(accno) != 11:
            print("❌ Invalid account number.")
            return
        accno = int(accno)

        cur.execute("SELECT BAL FROM South_Indian_Asian_Bank WHERE ACNO = :1", [accno])
        result = cur.fetchone()
        if not result:
            print("❌ Account not found.")
            return

        print(f"💰 Account xxxxxxx{str(accno)[-3:]} Balance: ₹{result[0]:.2f}")

    except orc.DatabaseError as e:
        print(f"❌ Database error: {e}")
    finally:
        try:
            cur.close()
            con.close()
        except:
            pass

deposit()
withdraw()
balance_enquiry()



