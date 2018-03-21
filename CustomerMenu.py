import cx_Oracle
from Account import Account
import Customer
db=cx_Oracle.connect('banking/bankingdb@localhost/xe')
cur=db.cursor()

class CustomerMenu:
    def show_menu(self,customer_id):
        self.customer_id=customer_id
        cur.execute("select firstname,lastname from customers where customerid="+str(self.customer_id))
        result=cur.fetchone()
        name= str(result[0]) + " " + str(result[1])
        print("\nWelcome " + name + "!")
        print("\n1.Deposit Money")
        print("2.Withdraw Money")
        print("3.Transfer Money")
        print("4.Print Statement")
        print("5.Change Address")
        print("6.Close account")
        print("7.Logout")
        self.get_option()
        
    def get_option(self):
        try:
            option=int(input("Enter your option "))
            if option >= 1 and option <= 7:
                self.go_to_option(option)
            else:
                self.show_invalid_option()
        except ValueError:
            self.show_invalid_option()
            
    def show_invalid_option(self):
        print("Invalid option")
        self.show_menu(self.customer_id)
        
    def go_to_option(self,option):
        if option==1:
            Account().deposit_money(self.customer_id)
        elif option==2:
            Account().withdraw_money(self.customer_id)
        elif option==3:
            Account().transfer_money(self.customer_id)
        elif option==4:
            Account().print_statement(self.customer_id)
        elif option==5:
            Customer.Customer().change_address(self.customer_id)
        elif option==6:
            Account().close_account(self.customer_id)
        if option==7:
            print("Successfully logged out")
        else:
            self.show_menu(self.customer_id)
