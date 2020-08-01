import socket
import pyautogui
import time
import threading

pyautogui.FAILSAFE = False
SERVER = "irc.twitch.tv"
PORT = 6667
PASS = "YOU PASSWORD TOKEN HERE"
BOT = "TwitchBot"
CHANNEL = "CHANNEL NAME"
OWNER = "CHANNEL NAME"
message = ""
oneButton = {'w' : 4, 'a' : 1, 's' : 2, 'd' : 1}
twoButtons = {'wa' : 1, 'wd' : 1}
allButtons = list(oneButton.keys())+list(twoButtons.keys())
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" +
          "NICK " + BOT + "\n" +
          "JOIN #" + CHANNEL + "\n").encode())
n = 5
threads = []
for i in range(n):
    num = 0
    threads.append(threading.Thread())

def gamecontrol(message):
    key = message.lower()
    print(key)
    if False not in [threads[i].is_alive() for i in range(n)]:
        print("no threads available, request deleted")
    else:
        if key in allButtons:
            for i in range(n):
                if not threads[i].is_alive():
                    if key in oneButton.keys():
                        target = pressButton
                        holdTime = oneButton[key]
                    else:
                        target = pressTwoButtons
                        holdTime = twoButtons[key]
                    threads[i] = threading.Thread(target=target, args=(key, holdTime))
                    threads[i].start()
                    break
    message = ""

def pressTwoButtons(keys, holdTime):
    keyMain, keyAdditional  = ' '.join(keys).split()
    start = time.time()
    tick = 0
    while time.time() - start < holdTime:
        pyautogui.keyDown(keyMain)
        if tick % 10000 == 0:
            pyautogui.keyDown(keyAdditional)
    pyautogui.keyUp(keyMain)
    pyautogui.keyUp(keyAdditional)

def pressButton(key, holdTime):
    start = time.time()
    while time.time() - start < holdTime:
        pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def Twitch():
    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(line):
        global message
        try:
            message = (line.split(":", 2))[2]
        except:
            message = ""
        return message

    def sendMessage(message="default message", irc=irc):
        messageTemp = f'PRIVMSG #{CHANNEL} :{message}'
        irc.send(f'{messageTemp}\n'.encode())

    def messageFromConsole(line):
        return False if "PRIVMSG" in line else True

    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
            elif messageFromConsole(line):
                if "PING" in line:
                    msgg = "PONG tmi.twitch.tv\r\n".encode()
                    irc.send(msgg)
                else:
                    pass
            else:
                message = getMessage(readbuffer).split()[0]
                gamecontrol(message)

    def printMessage(line):
        user = getUser(line)
        message = getMessage(line)
        print(f'{user}: {message}', end="")


if __name__ == '__main__':
    t0 = threading.Thread(target=Twitch)
    t0.start()
    t1 = threading.Thread(target=gamecontrol, args=(message,))
    t1.start()
