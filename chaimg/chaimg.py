import json
import time

import PySimpleGUI as sg
from chaim.chaimmodule import Chaim
import ccautils.utils as UT

# sg.theme("DarkAmber")  # Add a touch of color
# # All the stuff inside your window.
# layout = [
#     [sg.Text("Some text on Row 1")],
#     [sg.Text("Enter something on Row 2"), sg.InputText()],
#     [sg.Button("Ok"), sg.Button("Cancel")],
# ]
#
# # Create the Window
# window = sg.Window("Window Title", layout)
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event in (None, "Cancel"):  # if user closes window or clicks cancel
#         break
#     print("You entered ", values[0])
#
# window.close()


def statusDisplay(ch):
    df = ch.getDefaultSection()
    texp = int(df["tokenexpires"])
    now = int(time.time())
    timeleft = texp - now
    stimeleft = f"{UT.hms(timeleft, small=False, short=False, colons=True)}"
    myaccts = ch.myAccountList()
    alayout = []
    for acct in myaccts:
        xdef = "" if not acct[3] else "(Default)"
        arow = [sg.Text(acct[0]), sg.Text(acct[2]), sg.Text(xdef)]
        alayout.append(arow)
    layout = [[sg.Text("User Token:"), sg.Text(stimeleft, key="-TOKENLEFT-")]]
    layout.extend(alayout)
    elayout = [
        [sg.Button("New"), sg.Button("Quit")],
    ]
    layout.extend(elayout)
    window = sg.Window("Chaim Accounts", layout)
    while True:
        event, values = window.read(timeout=1000)
        if event in (
            None,
            "New",
            "Quit",
        ):  # if user closes window or clicks New or Quit
            break
        elif event in ("__TIMEOUT__"):
            now = int(time.time())
            timeleft = texp - now
            if timeleft <= 0:
                stimeleft = "Expired"
            else:
                stimeleft = f"{UT.hms(timeleft, short=False, small=False, colons=True)}"
            window["-TOKENLEFT-"].update(stimeleft)
    window.close()
    return event


def getPerms(ch):
    layout = [[sg.Text("Obtaining your permissions ...")]]
    win = sg.Window("Please Wait ...", layout)
    win.Read(timeout=1)
    perms = ch.listUserPerms()
    pdict = json.loads(perms["text"])
    win.close()
    return pdict


def newAccount(ch):
    pdict = getPerms(ch)
    accounts = [x for x in pdict]
    layout = [
        [
            sg.Combo(key="-ACCOUNTS-", values=accounts, enable_events=True),
            sg.Combo(key="-ROLES-", values=["Role"]),
        ],
        [sg.Text("Duration"), sg.In(key="-DURATION-")],
        [sg.Button("Create"), sg.Button("Cancel")],
    ]
    win = sg.Window("New Account", layout)
    while True:
        event, values = win.Read()
        if event in ("-ACCOUNTS-"):
            acct = values["-ACCOUNTS-"]
            print(acct)
            roles = pdict[acct]
            win["-ROLES-"].update(roles)
        elif event in ("Cancel"):
            break
        else:
            print(event)
            print("-")
            print(values)
    win.close()


def main():
    sg.theme("LightGreen")  # Add a touch of color
    ch = Chaim("wibble", "wobble")
    while True:
        event = statusDisplay(ch)
        if event in ("New"):
            newAccount(ch)
        elif event not in (None, "Quit"):
            print("status again")
        elif event in (None, "Quit"):
            break


if __name__ == "__main__":
    main()
