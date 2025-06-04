import oracledb as orc
import random

def openaccount():
    def generate_acno():
        return random.randint(10 ** 10, 10 ** 11 - 1)  # 11-digit account number

    try:
        # Establish connection
        con = orc.connect("system/Oracle123@localhost/system")
        cur = con.cursor()

        # Try to create the table
        try:
            cur.execute("""
                CREATE TABLE South_Indian_Asian_Bank (
                    ACNO NUMBER PRIMARY KEY,
                    CNAME VARCHAR2(50),
                    BAL NUMBER,
                    PIN VARCHAR2(4),
                    ADCNO VARCHAR2(12),
                    PAN VARCHAR2(10),
                    BNAME VARCHAR2(50)
                )
            """)
            print("✅ Table 'South_Indian_Asian_Bank' created.")
        except orc.DatabaseError as e:
            if "ORA-00955" in str(e):  # Table already exists
                print("ℹ️ Table 'South_Indian_Asian_Bank' already exists.")
            else:
                raise

        # Generate a unique account number
        while True:
            acno = generate_acno()
            cur.execute("SELECT 1 FROM South_Indian_Asian_Bank WHERE ACNO = :1", [acno])
            if not cur.fetchone():
                break

        # Get customer input
        cname = input("Enter Customer Name: ").strip()
        bal = int(input("Enter Initial Balance: "))
        adcno = input("Enter Aadhaar Number (12 digits): ").strip()
        pan = input("Enter PAN Number (10 characters): ").strip().upper()
        bname = input("Enter Branch Name: ").strip()

        # Validate PAN
        if len(pan) != 10 or not (pan[:5].isalpha() and pan[5:9].isdigit() and pan[9].isalpha()):
            print("❌ Invalid PAN format.")
            return

        # Validate Aadhaar
        if len(adcno) != 12 or not adcno.isdigit():
            print("❌ Invalid Aadhaar number.")
            return

        # PIN setup
        pin = input("Set your 4-digit PIN: ")
        if len(pin) != 4 or not pin.isdigit():
            print("❌ PIN must be exactly 4 digits.")
            return

        # Insert into DB
        cur.execute("""
            INSERT INTO South_Indian_Asian_Bank (ACNO, CNAME, BAL, PIN, ADCNO, PAN, BNAME)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (acno, cname, bal, pin, adcno, pan, bname))

        con.commit()

        print("\n✅ Account created successfully!")
        print(f"🆔 Account Number: {acno}")
        print("✅ Thank you for using this program.")

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

# Run the function
openaccount()
#38747343380
#1122
