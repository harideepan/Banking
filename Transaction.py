import cx_Oracle
import datetime
db=cx_Oracle.connect('banking/bankingdb@localhost/xe')
cur=db.cursor()
class Transaction:
    def create_deposit_id(self): #gets the deposit ID from the sequence in database
        cur.execute("select depositid.nextval from dual");
        self.trans_id=cur.fetchone()[0]
    def create_withdrawl_id(self): #gets the withdrawal ID from the sequence in database
        cur.execute("select withdrawid.nextval from dual");
        self.trans_id=cur.fetchone()[0]
    def create_transfer_id(self): #gets the transfer ID from the sequence in database
        cur.execute("select transferid.nextval from dual");
        self.trans_id=cur.fetchone()[0]
    def deposit(self,account_number,amount): #performs deposit operations
        self.create_deposit_id()
        cur.execute("update accounts set balance=balance + " + str(amount) + " where accountnumber="+ str(account_number))
        cur.execute("select balance from accounts where accountnumber="+ str(account_number))
        balance = float(cur.fetchone()[0])
        cur.execute("insert into transactions values('D"+ str(self.trans_id) +
                    "',systimestamp,"+str(account_number)+",'Deposit'," + str(amount) + ",null," + str(balance) +")")
        db.commit()
        return balance
    def withdraw(self,account_number,amount):#performs withdrawal operations
        self.create_withdrawl_id()
        cur.execute("update accounts set balance=balance - " + str(amount) + " where accountnumber="+ str(account_number))
        cur.execute("select balance from accounts where accountnumber="+ str(account_number))
        balance = float(cur.fetchone()[0])
        cur.execute("insert into transactions values('W"+ str(self.trans_id) +
                    "',systimestamp,"+str(account_number)+",'Withdraw',null," + str(amount) + "," + str(balance) +")")
        db.commit()
        return balance
    def transfer(self,from_account_number,to_account_number,amount):#performs transfer operations
        self.create_transfer_id()
        cur.execute("update accounts set balance=balance - " + str(amount) + " where accountnumber=" + str(from_account_number))
        cur.execute("select balance from accounts where accountnumber="+ str(from_account_number))
        balance_sender = float(cur.fetchone()[0])
        cur.execute("update accounts set balance=balance + " + str(amount) + " where accountnumber=" + str(to_account_number))
        cur.execute("select balance from accounts where accountnumber="+ str(to_account_number))
        balance_receiver = float(cur.fetchone()[0])
        cur.execute("select firstname,lastname from customers where customerid="+str(to_account_number))
        result=cur.fetchone()
        receiver_name= str(result[0]) + " " + str(result[1])
        cur.execute("insert into transactions values('T"+ str(self.trans_id) +
                    "',systimestamp,"+str(from_account_number)+",'Transfer to "+ str(to_account_number)+ "-" + receiver_name + "',null," + str(amount) + "," + str(balance_sender) +")")
        cur.execute("select firstname,lastname from customers where customerid="+str(from_account_number))
        result=cur.fetchone()
        sender_name= str(result[0]) + " " + str(result[1])
        cur.execute("insert into transactions values('T"+ str(self.trans_id) +
                    "',systimestamp,"+str(to_account_number)+",'Transfer from " + str(from_account_number) + "-" + sender_name + "'," + str(amount) + ",null," + str(balance_receiver) +")")
        db.commit()
        return balance_sender
    def get_transactions(self,account_number,from_date,to_date): #retrieves the transactions in the given date range
        
        from_d="to_date('" + from_date +"','dd/mm/yyyy')"
        to_d="to_date('" + to_date +"','dd/mm/yyyy')"
        cur.execute("select * from transactions where accountnumber=" + str(account_number)
                    + " and transactiondate between "+str(from_d)+" and  "+str(to_d)+" order by transactiondate asc")
        return cur
        
        
        
