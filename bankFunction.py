#coding=utf-8
import random
import pymysql
import time
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio import start_server
import webbrowser

global db
db = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='cyj20011105',
    db='bank',
    charset='utf8mb4'
)
global cursor
cursor = db.cursor()


class BankFunction(object):
    def __init__(self, dictUser):
        self.dictUser = dictUser

    # 开户
    def createUser(self):
        # Input name
        name = input("Please input your name: ")
        # Input ID number
        idCard = input("Please input you ID number: ")
        # Input tel number
        phone = input("Please input your phone number: ")
        cardNumber = self.createCardNumber()
        passwd = self.setPasswd()
        if passwd == -1:
            put_text("Failed to create")
            return -1
        # Set the value of money
        money = float(input("Please enter the amount you would like to deposit: "))
        # Create a user
        sql = "INSERT INTO user VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (name, idCard, phone, cardNumber))
        db.commit()
        sql = "INSERT INTO card VALUES(%s,%s,%s,%s)"
        cursor.execute(sql, (cardNumber, passwd, money, 1))
        db.commit()
        put_text("Hello, %s! Your bank card ID is %s" % (name, cardNumber))

    # set password
    def setPasswd(self):
        for i in range(3):
            passwd1 = input("please enter your password: ")
            passwd2 = input("Please enter your password again: ")
            if passwd1 == passwd2:
                return passwd1
            if i == 2:
                return -1
            put_text("Sorry, the password you entered twice is not the same, please re-enter")

    # Generate card number ramdomly
    def createCardNumber(self):
        while True:
            cardNumber = ""
            for i in range(6):
                cardNumber += str(random.randrange(0, 10))
            cursor.execute("SELECT * FROM card where cardNumber = '%s' " % cardNumber)
            card = cursor.fetchone()
            # put_text("card", card)
            if card is None:
                return cardNumber
        #put_text(cardNumber)

    def questUser(self):
        cardNumber = input("Please enter your card number: ")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        # print(card)

        if card is None:
            put_text("Sorry, the card number you entered does not exist!")
        elif card[3]=='0':
            put_text("Sorry, your card is locked")
        else:
            cursor.execute("SELECT * FROM user where cardNumber='%s' " % cardNumber)
            data = cursor.fetchall()[0]
            put_text(data[0], "Hello!")
            for i in range(3):
                pswd = input("Please enter your password: ")
                if pswd == card[1]:
                    put_text("You have the amount: ", card[2])
                    break
                else:
                    put_text("Sorry, the password you entered is incorrect")
                if i == 2:
                    put_text("Illegal user! Force quit!")

    def saveMoney(self):
        put_text('Enter account')
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1

        cursor.execute("SELECT * FROM user where cardNumber='%s' " % cardNumber)
        data = cursor.fetchall()[0]
        put_text(data[0], "Hello!")
        if card[3] == '0':
            put_text("Your card is locked and cannot be deposited")
            return -1
        res = self.checkPwd(cardNumber)
        if res == -1:  # Wrong pswd to many times
            card[3] = '0'
            return -1
        savemoney = float(input("Please enter the amount you want to deposit："))
        money = str(float(card[2]) + savemoney)
        cursor.execute("UPDATE card SET money = '%s' WHERE cardNumber = '%s' " % (money,cardNumber))
        db.commit()
        put_text("The deposit is successful, the available balance of your current user is：$ %s" % (money))

    def getMoney(self):
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1

        cursor.execute("SELECT * FROM user where cardNumber='%s' " % cardNumber)
        data = cursor.fetchall()[0]
        put_text(data[0], "Hello!")
        if card[3] == '0':
            put_text("Your card is locked and cannot be deposited")
            return -1
        res = self.checkPwd(cardNumber)
        if res == -1:  # Wrong pswd too many times
            card[3] = '0'
            return -1
        
        getmoney = float(input("Please enter the amount you want to withdraw："))
        if getmoney > float(card[2]):
            put_text("Sorry, your current balance is $ %s，insufficient balance！！！" % float(card[2]))
            return -1
        else:
            card_money = str(float(card[2]) - getmoney)
            cursor.execute("UPDATE card SET money = '%s' WHERE cardNumber = '%s' " % (card_money,cardNumber))
            db.commit()
            put_text("The withdrawal is successful, the available balance of your current user is：$ %s" % (card_money))


    def transferMoney(self):
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1
        elif card[3] == '0':
            put_text("Your card is locked and cannot be deposited")
            return -1
        else:
            cursor.execute("SELECT * FROM user where cardNumber='%s' " % cardNumber)
            data = cursor.fetchall()[0]
            put_text(data[0], "Hello!")
            for i in range(3):
                pswd = input("Please enter your password: ")
                if pswd == card[1]:
                    have_money = float(card[2])
                    put_text("You have an amount: $ ", have_money)
                    cardNumber2 = input("Please enter the card number you want to transfer: ")
                    cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber2)
                    card2 = cursor.fetchone()
                    if card2 is None:
                        put_text("Sorry, the card number you entered does not exist!")
                    elif card2[3] == '0':
                        put_text("This person's card is locked and cannot transfer money")
                    else:
                        while True:
                            turn_money = float(input("Please enter the amount you want to transfer: "))
                            if turn_money > have_money:
                                put_text("Sorry, you don't have that much money, please re-enter")
                            else:
                                your_card_money =str( float(card[2])-turn_money)
                                his_card_money =str( float( card2[2])+turn_money)
                                cursor.execute("UPDATE card SET money = '%s' WHERE cardNumber = '%s' " % (your_card_money,cardNumber))
                                db.commit()
                                cursor.execute("UPDATE card SET money = '%s' WHERE cardNumber = '%s' " % (his_card_money,cardNumber2))
                                db.commit()
                                put_text("Congratulations on your successful transfer, you still have $ ", your_card_money)
                                break
                    break
                else:
                    put_text("Sorry, the password you entered is incorrect")
                if i == 2:
                    put_text("Illegal user! Force quit!")

    def checkPwd(self, cardNumber):
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        card_p = card[1]
        for i in range(3):
            Pwd = input("Please enter your password:")
            if Pwd == card_p:
                return 0
            if i == 2:
                return -1  # Wrong pswd 3 times
            put_text("Your password is incorrect, please try again：")

    def editPasswd(self):
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
        else:
            cursor.execute("SELECT * FROM user where cardNumber='%s' " % cardNumber)
            data = cursor.fetchall()[0]
            put_text(data[0], "Hello!")
            for i in range(3):
                pswd = input("please enter your password: ")
                if pswd == card[1]:
                    put_text("You have an amount: $ ", card[2])
                    while True:
                        new_passwd1 = input("Please enter your new password: ")
                        new_passwd2 = input("Please enter your new password again: ")
                        if new_passwd1 != new_passwd2:
                            put_text("Please enter your new password again!")
                        else:
                            cursor.execute("UPDATE card SET passwd = '%s' WHERE cardNumber = '%s' " % (new_passwd1,cardNumber))
                            db.commit()
                            put_text("Congratulations! Change the password successfully!")
                            break
                    break
                else:
                    put_text("Sorry, the password you entered is incorrect")
                if i == 2:
                    put_text("Illegal user! Force quit!")

    def lockCard(self):
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1
        res = self.checkPwd(cardNumber)
        if res == -1:
            card[3] = '0'
            return -1
        flag = input("Could you please confirm the lock card?（YES/NO）")
        if flag == "YES":
            cursor.execute("UPDATE card SET isLock = '%s' WHERE cardNumber = '%s' " % ('0',cardNumber))
            db.commit()
            put_text("Your account has been successfully locked")
        else:
            return

    def unlockCard(self):
        cardNumber = input("Please enter your card number：")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1
        res = self.checkPwd(cardNumber)
        if res == -1:
            card[3] = '0'
            return -1
        cursor.execute("UPDATE card SET isLock = '%s' WHERE cardNumber = '%s' " % ('1',cardNumber))
        db.commit()
        put_text("Your account has been successfully unlocked")

    def Gotostreamlit(self):
        url = 'http://aichen35.mynatapp.cc'
        put_link("Click here to try our ML function", url, new_window=True).show()

    def killCard(self):
        cardNumber = input("Please enter your card number:")
        cursor.execute("SELECT * FROM card where cardNumber=  '%s' " % cardNumber)
        card = cursor.fetchone()
        if card is None:
            put_text("The card number you entered is incorrect, please re-enter:")
            return -1
        res = self.checkPwd(cardNumber)
        if res == -1:
            card[3] = '0'
            return -1
        if input("Whether to confirm the cancellation card number is: %s(y/n)" % cardNumber) == "y":
            sql = "DELETE FROM card WHERE cardNumber = %s"
            cursor.execute(sql, (cardNumber))
            db.commit()
            sql = "DELETE FROM user WHERE cardNumber = %s"
            cursor.execute(sql, (cardNumber))
            db.commit()
            put_text("The account has been cancelled successfully, and the account has been cancelled: %s" % cardNumber)
            put_text("Coming soon to feature selection page...")
            time.sleep(2)
            return 0

