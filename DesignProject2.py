###Bing Chiling Batallion - Design Project 2: Music Game
from machine import Pin, ADC, PWM, I2C
from mfrc522 import MFRC522
from pico_i2c_lcd import I2cLcd
from time import sleep
from random import randint, uniform


onPin = 1
buttonPin = 2
micPin = 26
speakerPin = 15

onOff = Pin(onPin, Pin.OUT)
button = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)
mic = ADC(Pin(micPin))
speaker = PWM(Pin(speakerPin))


class player:
    def __init__(self, uid):
        self.uid = uid
        self.score = 0
        self.winCon = False
        self.level = 0
        self.speed = 0

    def getID(self):
        return self.uid
    def getScore(self):
        return self.score
    def getLevel(self):
        return self.level
    def getSpeed(self):
        return self.speed

    def changeLevel(self, levelChange):
        self.level += levelChange
    def changeSpeed(self, speedChange):
        self.speed += speedChange
    def changeScore(self, points):
        self.score += points
    def win(self):
        self.winCon = True

    def toString(self):
        return f"Player ID: {self.uid}, Score: {self.score}"
    def checkWin(self):
        return self.winCon

def game(level, p, s): #level - list containing scale, p - player number in list
    #print to LCD screen
    #player {p + 1} clocked into shift, get ready to tune this instrument
    #here is your note, make sure you get this right
    correctNote = randint(0, level.length()-1)
    currNote = 0
    while(button.value() == 0):
        speed = s
        for i in range(len(level)*2-1):
            if(i < len(level)):
                currNote = i
            if(i >= len(level)):
                currNote = len(level) - (i - len(level) + 1)
            speaker.freq(level[currNote])
            for i in range(5):
                if(mic.read_u16() > 50000):
                    change = round(((mic.read_u16() - 50000)/1000), 3)  #tune these numbers, random guess rn
                    speed += uniform(-change, change)
                sleep(speed/5)
    if(currNote == correctNote):
        p.changeScore(1)
        #some message
    else:
        p.changeScore(-1)
        #some message


while True:
    anyWin = False
    playerList = []
    rfidList = []
    #LDC Screen Print Introduction, later problem
    #prints first time switch is turned on, while loop runs after until turned of
    '''
    if(onOff.value() == 1):
        print("Welcome")
    #scan RFID, num players, create objects
    while(button.value() == 0):
        if(readrfid in rfidList):
            print("Player already registered")
        else:
            playerList.append(player(rfid.read_id()))
    if(rfidList.length() == 0):
        print("No players registered, please register players")
        continue
    '''
    #main game loop
    p = 0
    tot = 0
    while(anyWin == False):
        p = tot % len(playerList)
        game(playerList[p].getLevel(), playerList[p], playerList[p].getSpeed())
        tot += 1