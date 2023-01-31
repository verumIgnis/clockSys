import pygame
from pygame.locals import *
import requests
import datetime
import tracer
from RPi.GPIO import GPIO

GPIO.setmode(GPIO.BOARD)

# set pins 36, 38, 40 to output and high
GPIO.setup(36, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(32, GPIO.IN)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

def getFont(size):
    var = pygame.font.SysFont("Berlin Sans FB Regular.ttf", size)
    return var

font169 = getFont(169)
font16 = getFont(16)
font45 = getFont(45)
font27 = getFont(27)
font80 = getFont(80)
font35 = getFont(35)

pos1 = (10, 10)
pos2 = (10, 50)
pos3 = (10, 90)
pos4 = (10, 130)
pos5 = (10, 170)
pos6 = (10, 210)
pos7 = (10, 250)

setpos1 = (10, 12)
setpos2 = (10, 62)
setpos3 = (10, 102)
setpos4 = (10, 142)
setpos5 = (10, 182)
setpos6 = (10, 222)
setpos7 = (10, 262)
setpos8 = (10, 300)

totalValueFloat = 0.0
totalValueStr = "0"

log1 = "-"
log2 = "-"
log3 = "-"
log4 = "-"
log5 = "-"
log6 = "-"

size = (480, 320)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("clockSys")
clock = pygame.time.Clock()

url = 'https://verumignis.com/clocksys/'

keepAliveCount = 5900
needKA = True
dispKAError = True
upload = False
KAnext = False
clockInNext = False
clockOutNext = False
clockedIn = True
total = 0
timeOffset = 0

backdrop=pygame.image.load("backdrop.png")
settingsBackdrop=pygame.image.load("settingsBackdrop.png")
serverError=pygame.image.load("serverError.png")
serverOk=pygame.image.load("serverOk.png")
uploadIcon=pygame.image.load("uploadIcon.png")
settingsIcon=pygame.image.load("settingsIcon.png")

totalLine = font80.render("Total:", 1, (255, 255, 255))
settingsTitle = font45.render("Settings", 1, (255, 255, 255))
setting1 = font35.render("Pay", 1, (255, 255, 255))
setting2 = font35.render("Time offset", 1, (255, 255, 255))
setting3 = font35.render("Server URL", 1, (255, 255, 255))
setting4 = font35.render("setting4", 1, (255, 255, 255))
setting5 = font35.render("setting5", 1, (255, 255, 255))
setting6 = font35.render("setting6", 1, (255, 255, 255))
settingsFooter = font16.render("Made by verumIgnis for a GCSE project. github.com/verumIgnis", 1, (255, 255, 255))

settingsBtn = pygame.Rect(430, 8, 48, 48)

# Get the current total and clocked in status from the server
response = requests.get(f"{url}clocklogs.json")
data = response.json()
print(data)
latestLog = data[-1]
total = latestLog["total"]
clockedIn = latestLog["clockedin"]

"""
except requests.exceptions.RequestException as e:
    print('Failed to connect to server:', e)
    total = None
    clockedIn = None
"""

if True:
    level = 0
    abort = False
    while not abort:
        
        if clockInNext:
            currentTime = datetime.datetime.now()
            log1 = f"Clock in @{currentTime.hour}:{currentTime.minute}"
            sendJson = {"minute": currentTime.minute, "hour": currentTime.hour}
            x = requests.post(url=f"{url}clockin", json=sendJson)
            clockInNext = False
            upload = False

        if clockOutNext:
            currentTime = datetime.datetime.now()
            log1 = f"Clock out @{currentTime.hour}:{currentTime.minute}"
            sendJson = {"minute": currentTime.minute, "hour": currentTime.hour}
            x = requests.post(url=f"{url}clockout", json=sendJson)
            total = x
            clockOutNext = False
            upload = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                abort = True

            elif event.type == MOUSEBUTTONDOWN:
                if settingsBtn.collidepoint(event.pos):
                    if level == 2:
                        level = 1
                        tracer.trace(143, "level", level)
                    elif level == 1:
                        level = 2
                        tracer.trace(146, "level", level)
        if GPIO.input(32):
            if level == 1:
                clockedIn = not clockedIn
                upload = True

                log6 = log5
                log5 = log4
                log4 = log3
                log3 = log2
                log2 = log1

                if not clockedIn:
                    clockInNext = True
                else:
                    clockOutNext = True

        if KAnext:
            KAnext = False
            keepAliveCount = 0
            needKA = True

            x = requests.get(f"{url}keepalive")
            if x.text == "True":
                needKA = False
            upload = False

        else:
            keepAliveCount+=1

        if keepAliveCount == 6000:
            KAnext = True
            upload = True
        if level == 0:
            level = 1

        elif level == 1:
            screen.blit(backdrop, (0, 0))
            if needKA:
                screen.blit(serverError, (247, 8))
            else:
                screen.blit(serverOk, (247, 8))

            if upload:
                screen.blit(uploadIcon, (290, 8))

            screen.blit(settingsIcon, (430, 8))

            textLine1 = font35.render(log1, 1, (255, 255, 255))
            textLine2 = font35.render(log2, 1, (255, 255, 255))
            textLine3 = font35.render(log3, 1, (255, 255, 255))
            textLine4 = font35.render(log4, 1, (255, 255, 255))
            textLine5 = font35.render(log5, 1, (255, 255, 255))
            textLine6 = font35.render(log6, 1, (255, 255, 255))

            screen.blit(textLine1, pos1)
            screen.blit(textLine2, pos2)
            screen.blit(textLine3, pos3)
            screen.blit(textLine4, pos4)
            screen.blit(textLine5, pos5)
            screen.blit(textLine6, pos6)

            totalValueLine = font35.render(f"{totalValueStr}hours <min>min", 1, (255, 255, 255))
            screen.blit(totalLine, (280, 90))
            screen.blit(totalValueLine, (280, 145))
            
        elif level == 2:
            screen.blit(settingsBackdrop, (0, 0))

            screen.blit(settingsIcon, (430, 2))

            screen.blit(settingsTitle, setpos1)
            screen.blit(setting1, setpos2)
            screen.blit(setting2, setpos3)
            screen.blit(setting3, setpos4)
            screen.blit(setting4, setpos5)
            screen.blit(setting5, setpos6)
            screen.blit(setting6, setpos7)
            screen.blit(settingsFooter, setpos8)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
