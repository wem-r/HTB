from PIL import Image, ImageFont, ImageDraw
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number', dest='num_meetup', help="Numéro du Meetep. Exemple: 0x09", type=str, required=True)
parser.add_argument('-m1', '--machine1', dest='machine1', help="Nom de la Machine 1", type=str, nargs='?', default=' ')
parser.add_argument('-m2', '--machine2', dest='machine2', help="Nom de la Machine 2", type=str, nargs='?', default=' ')
parser.add_argument('-m3', '--machine3', dest='machine3', help="Nom de la Machine 3", type=str, nargs='?', default=' ')
args = parser.parse_args()

#-------------------------------------------------------------
# Base Image & Meetup Title
width = 2560
height = 1440
background = Image.open('background.png')

font1 = ImageFont.truetype("Zeitung Micro Pro.ttf", 190)
font2 = ImageFont.truetype("Zeitung Micro Pro.ttf", 80)

meetup = f"OSCP-Like {args.num_meetup}"
draw = ImageDraw.Draw(background)
w, h = draw.textsize(meetup, font=font1)
draw.text(((width-w)/2, 50), meetup, (255,255,255), font=font1)

#-------------------------------------------------------------
# Box
machine1 = args.machine1;w1, h = draw.textsize(machine1, font=font2)
machine2 = args.machine2;w2, h = draw.textsize(machine2, font=font2)
machine3 = args.machine3;w3, h = draw.textsize(machine3, font=font2)

if len(sys.argv)==5:
    draw.text(((width-w1)/2, 900), machine1, (255,255,255), font=font2)

if len(sys.argv)==7:
    draw.text(((width-w1)/3, 900), machine1, (255,255,255), font=font2)
    draw.text(((width-w2)*0.7, 900), machine2, (255,255,255), font=font2)

if len(sys.argv)==9:
    draw.text(((width-w1)/5, 900), machine1, (255,255,255), font=font2)
    draw.text(((width-w2)/2, 900), machine2, (255,255,255), font=font2)
    draw.text(((width-w3)*0.8, 900), machine3, (255,255,255), font=font2)

#-------------------------------------------------------------
background.save(f'{args.num_meetup}.png')
