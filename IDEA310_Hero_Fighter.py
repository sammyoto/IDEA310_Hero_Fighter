from gpiozero import RotaryEncoder, RGBLED, Button
from PIL import Image, ImageDraw, ImageFont
import board
import digitalio
import adafruit_rgb_display.ili9341 as ili9341
import json
import requests
from time import sleep
import urllib.request
from io import BytesIO

accessToken = "303196328363975"


#initialize rotary encoder
rotor = RotaryEncoder(20, 21, wrap=True, max_steps=26)



############################LCD CODE#############################################
#set up LCD
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
BAUDRATE = 48000000
BORDER = 20
FONTSIZE = 12
button = Button(26)

# Setup SPI bus using hardware SPI:
spi = board.SPI()


disp = ili9341.ILI9341(
    spi,
    rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
    
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Draw a green filled box as the background
draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
disp.image(image)
    
# Load a TTF Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

############################LCD CODE#############################################


heroList = []

#Get JSON Response and Parse
def getHero(id):
    request = requests.get("https://superheroapi.com/api/" + accessToken + "/" + str(id) + "/")
    sam = request.json()
    return sam

#Choose a hero from the list by index
def viewHero(id):
    return heroList[id]["name"]

#Choose a hero and view their stats by index
def viewHeroStats(id):
    return heroList[id]["powerstats"]
            

#Load select heros into a list of dictionaries
def addHeros():
    print("Loading Heros...")
    heroList.append(getHero(17))
    heroList.append(getHero(30))
    heroList.append(getHero(38))
    heroList.append(getHero(69))
    heroList.append(getHero(78))
    heroList.append(getHero(127))
    heroList.append(getHero(149))
    heroList.append(getHero(176))
    heroList.append(getHero(208))
    heroList.append(getHero(213))
    heroList.append(getHero(298))
    heroList.append(getHero(303))
    heroList.append(getHero(310))
    heroList.append(getHero(332))
    heroList.append(getHero(341))
    heroList.append(getHero(346))
    heroList.append(getHero(352))
    heroList.append(getHero(370))
    heroList.append(getHero(389))
    heroList.append(getHero(476))
    heroList.append(getHero(489))
    heroList.append(getHero(510))
    heroList.append(getHero(527))
    heroList.append(getHero(655))
    heroList.append(getHero(659))
    heroList.append(getHero(720))
    heroList.append(getHero(729))
    print("Heros loaded!")
    
def chooseHeros():
    print("Choose two Heros!")
    chosenHeros = []
    lastValue = rotor.steps
    while len(chosenHeros) < 2:
        if button.is_pressed:
            chosenHeros.append(heroList[rotor.steps])
            print("Hero Chosen!")
            sleep(1)
        if rotor.steps < 0:
            rotor.steps == 26
        if rotor.steps != lastValue:
            text = viewHero(rotor.steps)
            stats = viewHeroStats(rotor.steps)
            draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
            (font_width, font_height) = font.getsize(text)
        
            draw.text(
            (10, 10),
            text,
            font=font,
            fill=(0, 0, 0),
            )
            
            i = 2
            for stat in stats:
                draw.text(
                (10, 30*i),
                stat,
                font=font,
                fill=(0, 0, 0),
                )
            
                draw.text(
                (200, 30*i),
                heroList[rotor.steps]["powerstats"][stat],
                font=font,
                fill=(0, 0, 0),
                )
                i = i + 1
            
            disp.image(image)
            lastValue = rotor.steps
            
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    return chosenHeros

#how the player chooses what to fight over
def statChoose():
    rotor.steps = 0
    lastValue = rotor.steps
    statChoices = list(heroList[0]["powerstats"])
    
    print("Choose a stat!")
    draw.text(
    (10, 10),
    "Which stat will they fight with?",
    font=font,
    fill=(0, 0, 0),
    )
    disp.image(image)
    while True:
        if button.is_pressed:
            return statChoices[rotor.steps]
        if rotor.steps < 0:
            rotor.steps = 5
        if rotor.steps > 5:
            rotor.steps = 0
        if rotor.steps != lastValue:
            draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
            draw.text(
            (10, 10),
            "Which stat will they fight with?",
            font=font,
            fill=(0, 0, 0),
            )
            draw.text(
            (100, 100),
            statChoices[rotor.steps],
            font=font,
            fill=(0, 0, 0),
            )
            disp.image(image)
            lastValue = rotor.steps
    
def displayImage(url):
    # Scale the image to the smaller screen dimension
    request = requests.get(url)
    #urllib.request.urlretrieve(url, "temp.jpg")
    image = Image.open(BytesIO(request.content))
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    disp.image(image)



def battleSim():
    print("Simulating battle...")
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    heros = chooseHeros()
    stat = statChoose()
    
    #First Hero name
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    draw.text(
    (125, 100),
    heros[0]["name"],
    font=font,
    fill=(0, 0, 0),
    )
    disp.image(image)
    sleep(2)
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    
    #First Hero Image
    displayImage(heros[0]["image"]["url"])
    sleep(2)
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    
    #Versus
    draw.text(
    (125, 100),
    "Versus",
    font=font,
    fill=(0, 0, 0),
    )
    disp.image(image)
    sleep(2)
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    
    #Second hero name
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    draw.text(
    (125, 100),
    heros[1]["name"],
    font=font,
    fill=(0, 0, 0),
    )
    disp.image(image)
    sleep(2)
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    
    #Second hero image
    displayImage(heros[1]["image"]["url"])
    sleep(2)
    draw.rectangle((0, 0, width, height), outline=0, fill=(255, 255, 255))
    
    
    difference = int(heros[0]["powerstats"][stat]) - int(heros[1]["powerstats"][stat])
    #display winner   
    
    if difference == 0:
        draw.text(
        (50, 100),
        heros[0]["name"] + " and " + heros[1]["name"] + " are equally strong!",
        font=font,
        fill=(0, 0, 0),
        )
        disp.image(image)
        sleep(2)
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        
    if difference > 0:
        draw.text(
        (50, 100),
        heros[0]["name"] + " is " + str(difference) + " points stronger!",
        font=font,
        fill=(0, 0, 0),
        )
        disp.image(image)
        sleep(2)
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        
    if difference < 0:
        draw.text(
        (50, 100),
        heros[1]["name"] + " is " + str(abs(difference)) + " points stronger!",
        font=font,
        fill=(0, 0, 0),
        )
        disp.image(image)
        sleep(2)
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
        
    draw.text(
    (50, 100),
    "Press the button to choose different heros.",
    font=font,
    fill=(0, 0, 0),
    )
    disp.image(image)
    #Play again
    while True:
        if button.is_pressed:
            sleep(1)
            break
    battleSim()
    
addHeros()
battleSim()




