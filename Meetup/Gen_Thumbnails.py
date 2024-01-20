from PIL import Image, ImageFont, ImageDraw
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', dest='num_meetup', help="Numero du Meetup. Exemple: 0x09", type=str, required=True)
parser.add_argument('-d', '--date', dest='date_meetup', help="Date du Meetup", type=str, required=True)
parser.add_argument('-m1', '--machine1', dest='machine1', help="Nom de la Machine 1", type=str, nargs='?')
parser.add_argument('-m2', '--machine2', dest='machine2', help="Nom de la Machine 2", type=str, nargs='?')
parser.add_argument('-m3', '--machine3', dest='machine3', help="Nom de la Machine 3", type=str, nargs='?')
args = parser.parse_args()

#-------------------------------------------------------------
# Function to retrieve avatar of a specific machine 
def get_machine_details(machine, machines):
    for i in range(0, len(machines)):
        if machines[i]['name'].lower() == machine.lower():
            print(f'Bingo : {machines[i]["name"]} avatar is {machines[i]["avatar"]}')
            return machines[i]["avatar"], machines[i]["os"]
    else:
        print(f"Error, machine {machine} not found in retired machines. EXITING")
        raise SystemExit

def os_picture(os):
    if os == "Windows":
        return "win.png"
    elif os == "Linux":
        return "linux.png"
    elif os == "Solaris":
        return "solaris.png"
    elif os == "Freebsd":
        return "freebsd.png"
    else:
        return "Error"
#-------------------------------------------------------------
# Import HTB token
with open('token.txt', 'r') as t:
    token = t.read().strip('\n')

# Get retired machine list
base_url = "https://labs.hackthebox.com"
api_url = "/api/v4/machine/list/retired/paginated?per_page=100"
headers = {
    "user-agent": "HTB-API",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token}

machines = requests.get(base_url + api_url, headers=headers, allow_redirects=True).json()['data']

#-------------------------------------------------------------
# Implementation logic : check if machines exists first !
if args.machine3 != None:
    if args.machine2 == None:
        print('[!] You defined machine 3 without a machine 2. EXITING')
        raise SystemExit
    elif args.machine1 == None:
        print('[!] You defined machine 3 without a machine 1. EXITING')
        raise SystemExit
    else:
        m3_avatar = get_machine_details(args.machine3, machines)

if args.machine2 != None:
    if args.machine1 == None:
        print('[!] You defined machine 2 without a machine 1. EXITING')
        raise SystemExit
    else:
        m2_avatar, m2_os = get_machine_details(args.machine2, machines)    

if args.machine1 != None:
    m1_avatar, m1_os = get_machine_details(args.machine1, machines)
    #print(m1_avatar, m1_os)

#-------------------------------------------------------------
# Base Image & Meetup Title
width = 2560
height = 1440
background = Image.open('background-v2.png')
draw = ImageDraw.Draw(background)

font1 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 150) # Title
font2 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 80) # Box Name
font3 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 65) # Date

meetup = f"Meetup HTB France {args.num_meetup}"
w, h = draw.textsize(meetup, font=font1)
# 500 pîxels from the left and 50 from the top, with font1 reduced to 150
draw.text((500, 50), meetup, fill="white", font=font1)

date = f"{args.date_meetup}"
w1, h1 = draw.textsize(date, font=font3)
# Text set in the remaining 2/3 of the image, to center in the "blank space" between the rooster and right
draw.text(((width+765-w1)/2, 1275), date, fill="white", font=font3)

#-------------------------------------------------------------
# Box
if args.machine1 != None:
    machine1 = args.machine1
    w1, h1 = draw.textsize(machine1, font=font2)
    im1 = Image.open(requests.get(base_url + m1_avatar, headers=headers, stream=True).raw)
    os1 = Image.open(os_picture(m1_os))
if args.machine2 != None:
    machine2 = args.machine2
    w2, h2 = draw.textsize(machine2, font=font2)
    im2 = Image.open(requests.get(base_url + m2_avatar, headers=headers, stream=True).raw)
if args.machine3 != None:
    machine3 = args.machine3
    w3, h3 = draw.textsize(machine3, font=font2)
    im3 = Image.open(requests.get(base_url + m3_avatar, headers=headers, stream=True).raw)

# Notes for test 
# Poison , FreeBSD, medium
# Code, Windows, insane
# Sunday, Solaris, easy
# Falafel, Linux, hard

rooster_offset = 765
logo_y = 525
text_y = logo_y + 80

if len(sys.argv)==7:
    # Width - rooster offset - 300 = 1510. Split in two parts = 755
    spacer = 50
    offset = int(755 - (w1 / 2) - spacer)
    # Base for y for 1 box : 605 for text , 525 for img
    background.paste(im1, ((rooster_offset + offset), 525), im1)
    # 300 is the width of the box image, spacer is 50
    draw.text(((rooster_offset + offset + 300 + spacer), 605), machine1, (255,255,255), font=font2)
    # Add the OS logo, logo is 90x90 , so we have 525 + 300 and want it to be centered so we add (300 - 90)/2
    background.paste(os1, ((rooster_offset + offset + 300 + spacer + w1 + spacer), 630), os1)


if len(sys.argv)==9:
    # A machine logo is 300 x 300, quick maths : width - rooster_offset - (2 * 300 ) = 1210. So we need to split this in three : 400, 410, 400
    draw.text((rooster_offset + 400 + ((300 - w1)/2) , text_y), machine1, (255,255,255), font=font2)
    background.paste(im1, ((rooster_offset + 400), logo_y), im1)
    draw.text(((width - 700 + + ((300 - w2)/2)), text_y), machine2, (255,255,255), font=font2)
    # 700 because we need one third of 1210 , rounded to 400, + 300
    background.paste(im2, ((width - 700), logo_y), im2)

if len(sys.argv)==11:
    # A machine logo is 300 x 300, quick maths : width - rooster_offset - (3 * 300 ) = 910. So we need to split this in four segments : 155 , 300 , 300 , 155
    draw.text((565 - (w1/2), text_y), machine1, (255,255,255), font=font2)
    background.paste(im1, (415, logo_y), im1)
    draw.text((1280 - (w2/2), text_y), machine2, (255,255,255), font=font2)
    background.paste(im2, (1130, logo_y), im2)
    draw.text((1995 - (w3/2), text_y), machine3, (255,255,255), font=font2)
    background.paste(im3, (1845, logo_y), im3)

#-------------------------------------------------------------
background.save(f'{args.num_meetup}.png')
