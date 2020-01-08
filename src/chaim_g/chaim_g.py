import ccalogging
from chaim.chaimmodule import Chaim

ccalogging.setConsoleOut()
ccalogging.setDebug()
log = ccalogging.log
log.info("in chaim_g.py")


def doit():
    try:
        log.info("in doit()")
        ch = Chaim("sredev", "apu", 1, tempname="tmpnam")
        accts = ch.myAccountList()
        log.info(f"accts is {accts}")
        # print(f"accts is {accts}")
        for acct in accts:
            dmsg = " DEFAULT " if acct[3] else ""
            print(f"account: {acct[0]}, {acct[2]}{dmsg}")
    except Exception as e:
        print("An exeption occurred")
        print(f"{e}")
