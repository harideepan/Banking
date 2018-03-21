import cx_Oracle
import datetime
import calendar
from Transaction import Transaction
import MainMenu
db=cx_Oracle.connect('banking/bankingdb@localhost/xe')
cur=db.cursor()
class Account:
    def create_new_account(self,account_number,account_type): #creates a new account
        cur.execute("insert into accounts values("+ str(account_number) + ",0,'" + account_type.upper() + "',systimestamp,'ACTIVE')")
        db.commit()
        if account_type.upper()=="CA":#if the account type is Current Account ₹5000 is deposited to the account 
           Transaction().deposit(account_number,5000)
           
    def deposit_money(self,account_number): #deposits money to the account
        try:
            amount=float(input("\nEnter the amount to deposit "))
            if amount>float(0):
                balance=Transaction().deposit(account_number,amount)
                print("Amount deposited successfully.\nYour balance: ₹" + str(balance))
            else:
                print("Invalid amount")
        except ValueError:
            print("Invalid amount")
            
    def get_withdrawl_count(self,account_number): #gets the numbers of withdrawals made in the current month
        now=datetime.datetime.now()
        current_month=now.strftime("%b").upper()
        current_year =now.strftime("%y")
        month_year=current_month + "-" + current_year
        cur.execute("select count(*) from transactions where accountnumber="
                            + str(account_number) + " and transactiondate like '%" + month_year + "' and description='Withdraw'")
        count=int(cur.fetchone()[0])
        return count
        
    def withdraw_money(self,account_number): #withdraws money from the account 
        try:
            cur.execute("select balance,accounttype from accounts where accountnumber=" + str(account_number))
            row=cur.fetchone()
            if row[1].upper()=="SB" and self.get_withdrawl_count(account_number) >= 10: #if the account type is Saving Account and Withdrawal count exceeds 10 in the current month
                print("You have exceeded the maximum withdrawl limit this month (Maximum 10 withdrawls per month)")
            else:
                amount=float(input("\nEnter the amount to withdraw "))
                if amount>float(0):
                    balance=float(row[0])
                    account_type=row[1]
                    if amount>balance:
                        print("Withdrawl failed. Insufficient balance. Your balance is ₹" + str(balance))
                    elif account_type.upper()=="CA" and balance-amount < 5000:
                        print("Withdrawl failed. You should maintain a minimum balance of ₹5000 \nYour balance is ₹"
                              + str(balance) + "\nYou can withdraw a maximum of ₹" + str(balance - 5000) + " as of now.")
                    else:
                        balance=Transaction().withdraw(account_number,amount)
                        print("Withdrawl success.\nYour balance: ₹" + str(balance))
                else:
                    print("Invalid amount")
        except ValueError:
            print("Invalid amount")

    def transfer_money(self,account_number): #transfers money
        try:
            to_account_number=int(input("\nEnter the account number to transfer "))
            cur.execute("select * from accounts where accountnumber=" + str(to_account_number))
            cur.fetchone()
            if cur.rowcount!=0:
                if account_number != to_account_number:
                    amount=float(input("Enter the amount to transfer "))
                    if amount>float(0):
                        cur.execute("select balance,accounttype from accounts where accountnumber=" + str(account_number))
                        row=cur.fetchone()
                        balance=float(row[0])
                        account_type=row[1]
                        if amount>balance:
                            print("Transfer failed. Insufficient balance. Your balance is ₹" + str(balance))
                        elif account_type.upper()=="CA" and balance-amount < float(5000):
                            print("Transfer failed. You should maintain a minimum balance of ₹5000 \nYour balance is ₹"
                                  + str(balance) + "\nYou can Transfer/Withdraw a maximum of ₹" + str(balance - float(5000)) + " as of now.")
                        else:
                            balance=Transaction().transfer(account_number,to_account_number,amount)
                            print("Transfer success.\nYour balance: ₹" + str(balance))
                    else:
                        print("Invalid amount")
                else:
                    print("You cannot transfer to your own account")
            else:
                print("Invalid account number")
        except ValueError:
            print("Invalid value")

    def print_statement(self,account_number): #Prints account statement
        while True:
            from_date=input("From date (DD/MM/YYYY): ")
            if(self.validate_date(from_date)):
               break
            else:
               print("Invalid date. Please enter a valid date")
        while True:
            to_date=input("To date (DD/MM/YYYY): ")
            if(self.validate_date(to_date)):
               break
            else:
               print("Invalid date. Please enter a valid date")
        if datetime.datetime.strptime(to_date,"%d/%m/%Y") > datetime.datetime.strptime(from_date,"%d/%m/%Y"):#If 'To date' is less than 'From date' 
            to_date=datetime.datetime.strptime(to_date,"%d/%m/%Y")
            to_date+= datetime.timedelta(days=1)
            to_date=to_date.strftime("%d") + "/" + to_date.strftime("%m") + "/" + to_date.strftime("%Y")
            
            transaction=Transaction().get_transactions(account_number,from_date,to_date)
            
            print("-"*120)
            print("TRANSACTION ID".center(14)+ "DATE".center(15) +"DESCRIPTION".center(45)
                  + "CREDIT".rjust(15) + "DEBIT".rjust(15) + "BALANCE".rjust(15))
            print("-"*120)
            row=transaction.fetchall()
            for i in range(0,transaction.rowcount):
                print(str(row[i][0]).center(14) + str(row[i][1].strftime("%d/%m/%Y")).center(15)
                      + str(row[i][3]).center(45) + ("".rjust(15) if row[i][4] is None else str(format(row[i][4],'.2f')).rjust(15))
                      + ("".rjust(15) if row[i][5] is None else str(format(row[i][5],'.2f')).rjust(15)) + str(format(row[i][6],'.2f')).rjust(15))
            print("-"*120)
        else:
            print("To date must be greater than from date.")
        
    def validate_date(self,date): #validates the format of date entered by the user
        try:
            datetime.datetime.strptime(date,"%d/%m/%Y")
        except ValueError:
            return False
        return True
    def close_account(self,customer_id): #closes the account
        option=input("Are you sure to close the account? (y/n) : ")
        if option.upper()=="Y":
            cur.execute("update accounts set status='CLOSED' where accountnumber=" + str(customer_id))
            cur.execute("select accounttype,balance from accounts where accountnumber=" + str(customer_id))
            result=cur.fetchone()
            account_type=result[0]
            balance=result[1]
            cur.execute("insert into closedaccounts values("+str(customer_id)+",systimestamp,'" + account_type + "')")
            cur.execute("update logincredentials set status='CLOSED' where customerid=" +str(customer_id))
            print("Account closed successfully. Your balance amount ₹" + str(balance) + " will be sent to your address soon")
            db.commit()
            MainMenu.MainMenu().show_menu()
    def display_closed_accounts_history(self): #displays the details of closed accounts
        cur.execute("select * from closedaccounts")
        result=cur.fetchall()
        print("-"*51)
        print("ACCOUNT NUMBER".center(16) + "ACCOUNT TYPE".center(20) + "CLOSE DATE".center(15))
        print("-"*51)
        for i in range(0,cur.rowcount):
            print(str(result[i][0]).center(16) + ("Savings Account".center(20) if result[i][2]=="SB" else "Current Account".center(20))
                  + str(result[i][1].strftime("%d/%m/%Y")).center(15))
        print("-"*51)
        
        
             
