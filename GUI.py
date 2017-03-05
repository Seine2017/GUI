import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import serial
from drawnow import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as Tk

window = Tk.Tk()
window.wm_title("Seine2017 Drone GUI")
window.configure(background='white')
window.geometry("1000x800")

fig1 = plt.figure()
a = fig1.add_subplot(511)
b = fig1.add_subplot(513)
c = fig1.add_subplot(515)
fig1.suptitle('IMU Data Received From Drone', fontsize=14, fontweight='bold')

xAcc = 0
yAcc = 0
zAcc = 0

aValues = []
bValues = []
cValues = []

a.plot(aValues)
a.set_title("X")
a.set_xlabel("Time (s)")
a.set_ylabel("Gyro (Degrees/s)")
b.plot(bValues)
b.set_title("Y")
b.set_xlabel("Time (s)")
b.set_ylabel("Gyro (Degrees/s)")
c.plot(cValues)
c.set_title("Z")
c.set_xlabel("Time (s)")
c.set_ylabel("Gyro (Degrees/s)")

canvas = FigureCanvasTkAgg(fig1, master=window)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

logo = Image.open("Logo.jpg")
logo = logo.resize((120,90),Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
panel = Tk.Label(window, image = logo, bg ="white")
panel.pack(side = Tk.RIGHT)

window.wm_iconbitmap("icon.ico")

if (serial == False):
    e = Tk.Label(window, text = "Error: Lost connection to drone", bg ="white")
    e.pack(side = "left")
else:
    co = Tk.Label(window, text = "Connected to drone", bg ="white")
    co.pack(side = "left")

def _quit():
    window.quit()
    window.destroy()

button = Tk.Button(master=window, text='Quit', command=_quit, bg ="white")
button.pack(side=Tk.BOTTOM)

zAccLabel = Tk.Label(window, text = "Z accleration: %d g" %zAcc, bg ="white")
zAccLabel.pack(side = Tk.BOTTOM)
yAccLabel = Tk.Label(window, text = "Y accleration: %d g" %yAcc, bg ="white")
yAccLabel.pack(side = Tk.BOTTOM)
xAccLabel = Tk.Label(window, text = "X accleration: %d g" %xAcc, bg ="white")
xAccLabel.pack(side = Tk.BOTTOM)

for i in range(0,26):
    aValues.append(0)
    bValues.append(0)
    cValues.append(0)
    
while True:
    while (serialArduino.inWaiting()==0):
        pass
    valueRead = serialArduino.readline()

    #check if valid value can be casted
    try:
        valueInInt = int(valueRead)
        print(valueInInt)
        if valueInInt <= 1024:
            if valueInInt >= 0:
                values.append(valueInInt)
                values.pop(0)
                drawnow(plotValues)
                Tk.mainloop()
            else:
                print ("Invalid! negative number")
        else:
            print ("Invalid! too large")
    except ValueError:
        print ("Invalid! cannot cast")
