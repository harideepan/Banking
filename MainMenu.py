from Customer import Customer
from Admin import Admin
import sys
class MainMenu:
    def show_menu(self): #Displays Main Menu
        print("\nMAIN MENU")
        print("1.Sign Up (New customer)")
        print("2.Sign In (Existing customer)")
        print("3.Admin Sign In")
        print("4.Quit")
        self.get_option()
    def get_option(self): #gets the option from the user and validates it
        try:
            option=int(input("Enter your option "))
            if option >= 1 and option <= 4:
                self.go_to_option(option)
            else:
                self.show_invalid_option()
        except ValueError:
            self.show_invalid_option()
    def show_invalid_option(self):
        print("Invalid option")
        self.show_menu()
    def go_to_option(self,option): #calls apporopriate functions 
        if option==1:
            Customer().sign_up()
        elif option==2:
            Customer().sign_in()
        elif option==3:
            Admin().sign_in()
        elif option==4:
            sys.exit()
        self.show_menu()
            
        


        
