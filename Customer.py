import cx_Oracle
from Account import Account
from CustomerMenu import CustomerMenu
db=cx_Oracle.connect('banking/bankingdb@localhost/xe')
cur=db.cursor()
class Customer:
    def sign_up(self): #Sign Up
        print("\nSIGN UP")
        print("Enter the details below")
        while True:
            self.first_name=(input("First name : "))
            if self.first_name != "":
                break
            else:
                print("First name cannot be blank.")
        while True:
            self.last_name=(input("Last name : "))
            if self.first_name != "":
                break
            else:
                print("First name cannot be blank.")
        self.get_address()
        while True:
            account_type=input("Account type (SB/CA) : ")
            if account_type.upper()=="SB" or account_type.upper()=="CA":
                break
            else:
                print("Invalid account type\n")
        while True:
            while True:
                password=input("Password : ")
                if len(password) < 8:
                    print("Password should contain atleast 8 characters.")
                else:
                    break
            cpassword=input("Confirm password : ")
            if password!=cpassword:
                print("Passwords doesn't match\n")
            else:
                break
        self.create_new_customer(password,account_type)
        
    def create_new_customer(self,password,account_type):
        self.create_customer_id()
        #Inserting customer details in the customer table
        cur.execute("insert into customers values("+ str(self.customer_id) + ",'" + self.first_name +"','"
                    + self.last_name + "','" + self.address_line1 + "','" + self.address_line2 + "','" + self.city + "','" + self.state + "'," + str(self.pincode) +")")
        #Inserting the customer's login credentials into the table
        cur.execute("insert into logincredentials values(" + str(self.customer_id) + ",'" + password + "','ACTIVE',0)")
        db.commit();
        #Creating new account for the customer
        Account().create_new_account(self.customer_id,account_type)
        print("Account created successfully. Your customer ID is " + str(self.customer_id))
        
    def create_customer_id(self): #gets the Customer ID from sequence in datebase
        cur.execute("select customerid.nextval from dual");
        self.customer_id=cur.fetchone()[0]
        
    def sign_in(self):
        print("\nSIGN IN")
        try:
            customer_id=int(input("Customer ID : "))
        except ValueError:
            print("Invalid Customer ID")
            self.sign_in()
        password=input("Password : ")
        cur.execute("select * from logincredentials where customerid=" + str(customer_id) + " and password='" + password + "'")
        result=cur.fetchone()
        if(cur.rowcount!=0): #if the Customer ID and password are valid
            status=result[2]
            if status.upper()=="CLOSED": #if the customer has closed the account
                print("Your account has been closed.")
            elif status.upper()=="LOCKED":#if the account is locked due to invalid attempts
                print("Your account has been locked.")
            else:
                cur.execute("update logincredentials set invalidattempts=0 where customerid=" + str(customer_id))
                db.commit()
                CustomerMenu().show_menu(customer_id)
        else: #if Customer ID or Password is invalid
            #getting the invalid attempts count and status from the table
            cur.execute("select invalidattempts,status from logincredentials where customerid="+str(customer_id))
            result=cur.fetchone()
            if cur.rowcount!=0: #if the Customer ID is valid
                status=result[1]
                if status.upper()=="LOCKED":#if the account is locked due to invalid attempts
                    print("Your account has been locked.")
                elif status.upper()=="CLOSED": #if the customer has closed the account
                    print("Your account has been closed.")
                else: 
                    print("Invalid credentials")
                    attempts=result[0]
                    if attempts < 2: #if invalid attempts is less than 2
                        print("Attempts remaining : " + str(2-(attempts)))
                        #incrementing the invalid attempts count in LoginCredentials table
                        cur.execute("update logincredentials set invalidattempts=invalidattempts+1 where customerid=" + str(customer_id))
                    else: #if the invalid attempts is 3
                        #changing the status to 'Locked' in LoginCredentials table
                        cur.execute("update logincredentials set invalidattempts=0,status='LOCKED' where customerid=" + str(customer_id))
                        print("Your attempts are over. Your account has been locked")
                    db.commit()
            else: #if the Customer ID is invalid
                print("Invalid Customer ID")
            
    def get_address(self): #get the address from the user
        self.address_line1=(input("Address line 1 : "))
        self.address_line2=(input("Address line 2 : "))
        self.city=(input("City           : "))
        self.state=     (input("State          : "))
        while True:
            try:
                self.pincode=int(input("Pincode        : "))
                if self.pincode < 100000 or self.pincode > 999999:
                    print("Invalid pincode\n")
                else:
                     break
            except ValueError:
                print("Invalid pincode")
        
    def change_address(self,customer_id): #gets the new address from the user and updates in the database
        print("\nYour Address")
        self.display_address(customer_id)
        print("\nEnter your new Address")
        self.get_address()
        cur.execute("update customers set addressline1='" + self.address_line1
                    + "',addressline2='" + self.address_line2 + "',city='"
                    +self.city+"',state='"+self.state+"',pincode="+str(self.pincode)+" where customerid="+str(customer_id))
        db.commit()
        print("Address updated sucessfully")
        
    def display_address(self,customer_id): #displays the customer's address
        cur.execute("select addressline1,addressline2,city,state,pincode from customers where customerid="
                    + str(customer_id))
        address=cur.fetchone()
        print("Address line 1 : " + address[0])
        print("Address line 2 : " + address[1])
        print("City           : " + address[2])
        print("State          : " + address[3])
        print("Pincode        : " + str(address[4]))
        
        
        
        
        
        



