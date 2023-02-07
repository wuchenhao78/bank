from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio import start_server
import os
import pickle
from bankFunction import BankFunction
import time

def main():
    put_markdown("Modern Bank System")

    def check_both(info):
        dictUser = {"wch": "1", "cyj": "2"}
        if info.get("accout") not in dictUser:
            return ('accout', "The account you entered does not exist! Please try again")
        if info.get("password") != dictUser[info.get("accout")]:
            return ('password', "The password you entered is incorrect! Please try again")

    info = input_group(
        "Welcome to our bank system",
        inputs=[
            input('Please enter your administrator accout: ', name='accout'),
            input('Please enter your administrator password: ', name='password', type=PASSWORD)
        ],
        validate=check_both
    )

    # Use Bank Function
    bank = BankFunction({})
    while True:
        number = select(
            label = "Please enter the function number you want to select: ",
            options = [
                {"label": 'Open An Account', "value": 1},
                {"label": 'Information Of Account', "value": 2},
                {"label": 'Deposit', "value": 3},
                {"label": 'Withdraw Money', "value": 4},
                {"label": 'Transfer', "value": 5},
                {"label": 'Change Password', "value": 6},
                {"label": 'Lock Card', "value": 7},
                {"label": 'Unlock card', "value": 8},
                {"label": 'Apply For A Credit Card (Trial version)', "value": 9},
                {"label": 'Replenish Card', "value": 0},
                {"label": 'Quit',"value": 'q'}
            ]
        )
        if number == 1:
            bank.createUser()
        elif number == 2:
            bank.questUser()
        elif number == 3:
            bank.saveMoney()
        elif number == 4:
            bank.getMoney()
        elif number == 5:
            bank.transferMoney()
        elif number == 6:
            bank.editPasswd()
        elif number == 7:
            bank.lockCard()
        elif number == 8:
            bank.unlockCard()
        elif number == 9:
            bank.Gotostreamlit()
        elif number == 0:
            bank.killCard()
        elif number == 'q':
            put_text("System is rolling out, please wait...")
            time.sleep(2)
            put_text("Quit successfully！")
            break





if __name__ == '__main__':
    start_server(main,port=8035,cdn=False,auto_open_webbrowser=True)

