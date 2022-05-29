from tkinter import *
from tkinter import ttk
from threading import *
from PIL import Image, ImageFont, ImageDraw
import requests

class sim(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        myfont = family = ("Century Gothic", 10)
        Green = "#00FF80"
        canvas = Canvas(self, bg="#141d2b")
        canvas.pack(fill=BOTH, expand=1)
        # Text Label
        self.label1 = Label(root, font=("Century Gothic", 10), text="Meetup N°", bg='#141d2b', fg='white')
        self.label1.place(x=15, y=10)
        self.label2 = Label(root, font=("Century Gothic", 8), text="(Ex: 0x08)", bg='#141d2b', fg='yellow')
        self.label2.place(x=90, y=10)
        self.label6 = Label(root, font=("Century Gothic", 14), text="OSCP-Like ", bg='#141d2b', fg='white')
        self.label6.place(x=15, y=35)
        self.label3 = Label(root, font=("Century Gothic", 10), text="Machine 1", bg='#141d2b', fg='white')
        self.label3.place(x=15, y=75)
        self.label4 = Label(root, font=("Century Gothic", 10), text="Machine 2", bg='#141d2b', fg='white')
        self.label4.place(x=15, y=105)
        self.label5 = Label(root, font=("Century Gothic", 10), text="Machine 3", bg='#141d2b', fg='white')
        self.label5.place(x=15, y=135)
        MeetupN = Text(root, height=1, width=10, relief="sunken")
        MeetupN.place(x=120, y=40)
        outbot = Text(root, height=6, width=38, relief="sunken",font=('Consolas', 8) , bg='#000000', fg=Green)
        outbot.place(x=15, y=210)
        #-------------------------------------------------------------
        # Function to retrieve avatar of a specific machine
        def get_machine_avatar(machine, machines):
            for i in range(0, len(machines)):
                if machines[i]['name'].lower() == machine.lower():
                    # print(f'Bingo : {machines[i]["name"]} avatar is {machines[i]["avatar"]}')
                    return machines[i]["avatar"]
            else:
                outbot.delete(1.0, 'end')
                outbot.insert('end', 'Error, '+machine+' not found in retired machines.'+'\n')
                # raise SystemExit
        #-------------------------------------------------------------
        # Import HTB token
        with open('token.txt', 'r') as t:
            token = t.read()#.strip('\n')
        #-------------------------------------------------------------
        # Get retired machine list
        base_url = "https://www.hackthebox.com"
        api_url = "/api/v4/machine/list/retired"
        headers = {'content-type': 'application/json','user-agent': 'HTB-API', 'Authorization': 'Bearer ' + token}
        machines = requests.get(base_url + api_url, headers=headers, allow_redirects=True).json()['info']
        MachineList = ['']
        for i in range(0, len(machines)): MachineList.extend({machines[i]["name"]})
        #-------------------------------------------------------------
        MachineList1 = ttk.Combobox(root, width=20, values=MachineList)
        MachineList1.place(x=100, y=75)
        MachineList2 = ttk.Combobox(root, width=20, values=MachineList)
        MachineList2.place(x=100, y=105)
        MachineList3 = ttk.Combobox(root, width=20, values=MachineList)
        MachineList3.place(x=100, y=135)
        #-------------------------------------------------------------
        def GenImage():
            MeetupNumber = MeetupN.get(1.0, "end-1c")
            m1List = MachineList1.get()
            m2List = MachineList2.get()
            m3List = MachineList3.get()
            
            width = 2560
            height = 1440
            background = Image.open('background.png')
            font1 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 190)
            font2 = ImageFont.truetype("Zeitung_Micro_Pro.ttf", 80)
            meetup = f"OSCP-Like {MeetupNumber}"
            draw = ImageDraw.Draw(background)

            w, h = draw.textsize(meetup, font=font1)
            draw.text(((width-w)/2, 50), meetup, (255,255,255), font=font1)

            m1_avatar = get_machine_avatar(m1List, machines)
            m2_avatar = get_machine_avatar(m2List, machines)    
            m3_avatar = get_machine_avatar(m3List, machines)

            if m1List != None:
                machine1 = m1List;w1, h = draw.textsize(machine1, font=font2)
                im1 = Image.open(requests.get(base_url + m1_avatar, headers=headers, stream=True).raw)
            if m2List != None:
                machine2 = m2List;w2, h = draw.textsize(machine2, font=font2)
                im2 = Image.open(requests.get(base_url + m2_avatar, headers=headers, stream=True).raw)
            if m3List != None:
                machine3 = m3List;w3, h = draw.textsize(machine3, font=font2)
                im3 = Image.open(requests.get(base_url + m3_avatar, headers=headers, stream=True).raw)
            
            outbot.delete(1.0, 'end')
            
            if MeetupN.get(1.0, "end-1c"):
                outbot.insert('end', 'Title : '+meetup+'\n')
            else:
                outbot.insert('end', '[x] You need a Meetup Number'+'\n')
            if m1List and not m2List and not m3List:
                outbot.insert('end', "Machine 1 : "+m1List+'\n')
                draw.text(((width-w1)/2, 900), machine1, (255,255,255), font=font2)
                background.paste(im1, (int((width-300)/2), 570), im1)
            if m1List and m2List and not m3List:
                outbot.insert('end', "Machine 1 : "+m1List+'\n')
                outbot.insert('end', "Machine 2 : "+m2List+'\n')
                draw.text((800 - (w1/2), 900), machine1, (255,255,255), font=font2)
                background.paste(im1, (650, 570), im1)
                draw.text((1760 - (w2/2), 900), machine2, (255,255,255), font=font2)
                background.paste(im2, (1605, 570), im2)
            if m1List and m2List and m3List:
                outbot.insert('end', "Machine 1 : "+m1List+'\n')
                outbot.insert('end', "Machine 2 : "+m2List+'\n')
                outbot.insert('end', "Machine 3 : "+m3List+'\n')
                draw.text((565 - (w1/2), 830), machine1, (255,255,255), font=font2)
                background.paste(im1, (415, 500), im1)
                draw.text((1280 - (w2/2), 830), machine2, (255,255,255), font=font2)
                background.paste(im2, (1130, 500), im2)
                draw.text((1995 - (w3/2), 830), machine3, (255,255,255), font=font2)
                background.paste(im3, (1845, 500), im3)
            background.save(f'{MeetupNumber}.png')
        #-------------------------------------------------------------
        self.button1 = Button(root, font=myfont, bg='#dbdbdb', text="Generate", command=GenImage, height=1, width=28, borderwidth=0, relief=SOLID)
        self.button1.place(x=15, y=170)
        #-------------------------------------------------------------

root = Tk()
mygui = sim(root).configure(bg='#141d2b')
root.wm_title("HTB Meetup France")
#root.configure(bg='#141d2b')
root.geometry("265x310")
root.iconbitmap("favicon.ico")
root.resizable(width=False, height=False)
root.eval('tk::PlaceWindow . center')
root.mainloop()
