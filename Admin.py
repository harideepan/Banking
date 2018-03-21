import cx_Oracle
from Account import Account
db=cx_Oracle.connect('banking/bankingdb@localhost/xe')
cur=db.cursor()
class Admin:
    def sign_in(self): #Admin sigin
        try:
            admin_id=int(input("ID      : "))
        except ValueError:
            print("Invalid Customer ID")
        password=input("Pasword : ")
        cur.execute("select * from admin where adminid=" + str(admin_id) + " and password='" + password + "'")
        result=cur.fetchone()
        if(cur.rowcount!=0):
            status=result[2]
            if status.upper()=="LOCKED":
                print("Logon denied")
            else:
                cur.execute("update admin set invalidattempts=0 where adminid=" + str(admin_id))
                db.commit()
                self.show_menu()
        else:
            print("Invalid credentials. Logon denied")
            cur.execute("select invalidattempts,status from admin where adminid="+str(admin_id))
            result=cur.fetchone()
            status=result[1]
            if status.upper()=="LOCKED":
                print("Exceede the maximum invalid attempts limit.")
            else:
                attempts=result[0]
                if attempts < 2:
                    print("Attempts remaining : " + str(2-(attempts)))
                    cur.execute("update admin set invalidattempts=invalidattempts+1 where adminid=" + str(admin_id))
                else:
                    cur.execute("update admin set invalidattempts=0,status='LOCKED' where adminid=" + str(admin_id))
                    print("Your attempts are over.")
                db.commit()

    def show_menu(self): #displays menu for Admin
        print("\nWelcome Admin")
        print("1.View Closed Account History")
        print("2.Logout")
        self.get_option()

    def get_option(self):
        try:
            option=int(input("Enter your option "))
            if option >= 1 and option <= 2:
                self.go_to_option(option)
            else:
                self.show_invalid_option()
        except ValueError:
            self.show_invalid_option()
    d
    ef show_invalid_option(self):
        print("Invalid option")
        self.show_menu()

    def go_to_option(self,option):
        if option==1:
            Account().display_closed_accounts_history()
        if option==2:
            print("Successfully logged out")
        else:
            self.show_menu()
        
        
    
            
        
