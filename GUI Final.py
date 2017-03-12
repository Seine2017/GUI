import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import serial
import tkinter as Tk
import math
import random
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

pitchDiv = 200/90
yawDiv = 200/90
line_length = 150
centre_x = 250
centre_y =250

cnt = 0

ser = serial.Serial()
ser.baudrate = 57600
ser.port = 'COM7'
ser.open()

window = Tk.Tk()
window.wm_title("Seine2017 Drone GUI")
window.configure(background='white')

aValues = []
bValues = []
cValues = []
x =[]
for i in range(0,26):
    aValues.append(0)
    bValues.append(0)
    cValues.append(0)
    x.append(i)
rollVelInt = 0
pitchVelInt = 0
yawVelInt = 0

logo = Image.open("Logo.jpg")
logo = logo.resize((200,150),Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
panel = Tk.Label(window, image = logo, bg ="white")
panel.grid(row = 20, column = 1, rowspan=10, columnspan=3)

rollVel = Tk.StringVar()
pitchVel = Tk.StringVar()
yawVel = Tk.StringVar()

canvas = Tk.Canvas(window, width =500, height = 500, bg = "black")
canvas.create_text(250, 40, text="Roll", fill="green", font = 14)
canvas.create_text(15, 250, text="\n".join("Pitch"), fill="green", font = 14)
canvas.grid(row = 2, column = 6, rowspan = 27)
canvas.create_line(50, 50, 50, 450, fill="green", width = 3)
canvas.create_text(30, 50, text="90", fill="green")
canvas.create_text(30, 250, text="0", fill="green")
canvas.create_text(30, 450, text="-90", fill="green")
canvas2 = Tk.Canvas(window, width =50, height = 500, bg = "white", highlightthickness = 0)
canvas2.grid(row =2, column = 4, rowspan = 27)

window.wm_iconbitmap("icon.ico")

def _quit():
    file.close()
    window.quit()
    window.destroy()


button = Tk.Button(master=window, text='Save & Quit', command=_quit, bg ="white")
button.grid(row = 10, column = 1,rowspan = 2, columnspan = 3)

filteredLabel = Tk.Label(window, text = "Filtered Measurements", bg ="white", font = "16").grid(row = 2, column = 1, columnspan = 3)
rollVelLabel = Tk.Label(window, text = "Roll :", bg ="white").grid(row = 4, column = 1)
rollVelLabel1 = Tk.Label(window, textvariable = rollVel, bg ="white").grid(row = 4, column = 2)
rollVelLabel2 = Tk.Label(window, text = "Degrees", bg ="white").grid(row = 4, column = 3)
pitchVelLabel = Tk.Label(window, text = "Pitch:" , bg ="white").grid(row = 5, column = 1)
pitchVelLabel1 = Tk.Label(window, textvariable = pitchVel, bg ="white").grid(row = 5, column = 2)
pitchVelLabel2 = Tk.Label(window, text = "Degrees" , bg ="white").grid(row = 5, column = 3)
yawVelLabel = Tk.Label(window, text = "Yaw Velocity:", bg ="white").grid(row = 6, column = 1)
yawVelLabel1 = Tk.Label(window, textvariable = yawVel, bg ="white").grid(row = 6, column = 2)
yawVelLabel2 = Tk.Label(window, text = "Rad/s", bg ="white").grid(row = 6, column = 3)


plt.ion()
fig1 = Figure(figsize= (6,6) , frameon = False)
a = fig1.add_subplot(311)
b = fig1.add_subplot(312)
c = fig1.add_subplot(313)
a.clear()
a.set_title('Roll')
a.set_ylabel('Angle')
a.set_xticks(())
a.set_yticks(np.arange(-90,91,30))
a.set_ylim(-90,90)
a.grid()
b.clear()
b.set_title('Pitch')
b.set_ylabel('Angle')
b.set_xticks(())
b.set_yticks(np.arange(-90,91,30))
b.set_ylim(-90,90)
b.grid()
c.clear()
c.set_title('Yaw')
c.set_ylabel('Angular Velocity')
c.set_xticks(())
c.set_yticks(np.arange(-250,251,50))
c.set_ylim(-250,250)
c.grid()
fig1.suptitle('Filtered Measurements', fontsize=14, fontweight='bold')
line1, = a.plot(x,aValues, 'g')
line2, = b.plot(x,bValues, 'g')
line3, = c.plot(x,cValues, 'g')

canvas1 = FigureCanvasTkAgg(fig1, master=window)

def plotValues():
    line1.set_ydata(aValues)
    line2.set_ydata(bValues)
    line3.set_ydata(cValues)
    canvas1.show()
    canvas1.get_tk_widget().grid(row = 2, column = 5, rowspan = 27)
    canvas1.get_tk_widget().configure( background ="white")
    plt.close()

file = open("IMU_Data.txt","w")

   
while True:
    
    string = ser.readline()
    string = str(string)[2:-5]
    array = string.split(" ")
    #print(array)
    if(len(array) == 3):
        #if(array[0] != math.nan | array[1] != math.nan |array[2] != math.nan):
        if(cnt % 1 == 0):
            r = float(array[1])
            p = float(array[0])
            y = float(array[2])
            r = r * 180/math.pi
            p = p * 180/math.pi
        cnt += 1
        
        file.write("\n")
        file.write(string)
        rollVelInt = int(r)
        pitchVelInt = int(p)
        yawVelInt = int(y)
        rollVel.set(rollVelInt)
        pitchVel.set(pitchVelInt)
        yawVel.set(yawVelInt)
        aValues.append(rollVelInt)
        bValues.append(pitchVelInt)
        cValues.append(yawVelInt)
        aValues.pop(0)
        bValues.pop(0)
        cValues.pop(0)   
        #plotValues()

        angle_in_radians = rollVelInt * math.pi / 180
        end_x = centre_x + line_length * math.cos(angle_in_radians)
        end_y = centre_y + line_length * math.sin(angle_in_radians)
        l1 = canvas.create_line(centre_x, centre_y, end_x, end_y, fill="green", width = 3)
        l2 = canvas.create_line(centre_x, centre_y, 500-end_x, 500-end_y, fill="green", width = 3)
        l3 = canvas.create_line(50, 250-(pitchDiv*pitchVelInt), 65, 243-(pitchDiv*pitchVelInt), 65,
                                    257-(pitchDiv*pitchVelInt), 50, 250-(pitchDiv*pitchVelInt), fill="green", width = 2)
            

        
        window.update()
        canvas.delete(l1,l2,l3)
