from PIL import Image, ImageFont, ImageDraw
import requests
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', dest='num_meetup', help="Numero du Meetup. Exemple: 0x09", type=str, required=True)
parser.add_argument('-m1', '--machine1', dest='machine1', help="Nom de la Machine 1", type=str, nargs='?')
parser.add_argument('-m2', '--machine2', dest='machine2', help="Nom de la Machine 2", type=str, nargs='?')
parser.add_argument('-m3', '--machine3', dest='machine3', help="Nom de la Machine 3", type=str, nargs='?')
args = parser.parse_args()

#-------------------------------------------------------------
# Function to retrieve avatar of a specific machine 

def get_machine_avatar(machine, machines):
    for i in range(0, len(machines)):
        if machines[i]['name'].lower() == machine.lower():
            print(f'Bingo : {machines[i]["name"]} avatar is {machines[i]["avatar"]}')
            return machines[i]["avatar"]
    else:
        print(f"Error, machine {machine} not found in retired machines. EXITING")
        raise SystemExit

#-------------------------------------------------------------
# Import HTB token
with open('token.txt', 'r') as t:
    token = t.read().strip('\n')

#-------------------------------------------------------------
# Get retired machine list
base_url = "https://www.hackthebox.com"
api_url = "/api/v4/machine/list/retired"
headers = {'user-agent': 'HTB-API', 'Authorization': 'Bearer ' + token}

machines = requests.get(base_url + api_url, headers=headers, allow_redirects=True).json()['info']


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
        m3_avatar = get_machine_avatar(args.machine3, machines)

if args.machine2 != None:
    if args.machine1 == None:
        print('[!] You defined machine 2 without a machine 1. EXITING')
        raise SystemExit
    else:
        m2_avatar = get_machine_avatar(args.machine2, machines)    

if args.machine1 != None:
    m1_avatar = get_machine_avatar(args.machine1, machines)

#-------------------------------------------------------------
# Base Image & Meetup Title
width = 2560
height = 1440
background = Image.open('background.png')

font1 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 170)
font2 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 80)

meetup = f"Meetup HTB France {args.num_meetup}"
draw = ImageDraw.Draw(background)
w, h = draw.textsize(meetup, font=font1)
draw.text(((width-w)/2, 80), meetup, (20,29,44), font=font1)

#-------------------------------------------------------------
# Box
if args.machine1 != None:
    machine1 = args.machine1;w1, h = draw.textsize(machine1, font=font2)
    im1 = Image.open(requests.get(base_url + m1_avatar, headers=headers, stream=True).raw)
if args.machine2 != None:
    machine2 = args.machine2;w2, h = draw.textsize(machine2, font=font2)
    im2 = Image.open(requests.get(base_url + m2_avatar, headers=headers, stream=True).raw)
if args.machine3 != None:
    machine3 = args.machine3;w3, h = draw.textsize(machine3, font=font2)
    im3 = Image.open(requests.get(base_url + m3_avatar, headers=headers, stream=True).raw)

if len(sys.argv)==5:
    draw.text(((width-w1)/2, 925), machine1, (255,255,255), font=font2)
    background.paste(im1, (int((width-300)/2), 625), im1)

if len(sys.argv)==7:
    draw.text((800 - (w1/2), 925), machine1, (255,255,255), font=font2)
    background.paste(im1, (650, 625), im1)
    draw.text((1760 - (w2/2), 925), machine2, (255,255,255), font=font2)
    background.paste(im2, (1605, 625), im2)

if len(sys.argv)==9:
    draw.text((565 - (w1/2), 925), machine1, (255,255,255), font=font2)
    background.paste(im1, (415, 625), im1)
    draw.text((1280 - (w2/2), 925), machine2, (255,255,255), font=font2)
    background.paste(im2, (1130, 625), im2)
    draw.text((1995 - (w3/2), 925), machine3, (255,255,255), font=font2)
    background.paste(im3, (1845, 625), im3)

#-------------------------------------------------------------
background.save(f'{args.num_meetup}.png')
