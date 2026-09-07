import requests
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Led Controller")
root.geometry("300x125")
root.resizable(False, False)

def togglePin(pinNum):
    try:
        response = requests.get('http://192.168.1.167/pin?gpio=' + str(pinNum))
        #response = requests.get('http://97.99.90.190:5000/pin?gpio=' + str(pinNum))
        ledStatus = response.text
    except:
        print("Something went wrong")
        return

    if (ledStatus == "0"):
        print("Pin " + str(pinNum) + " off")
    else:
        print("Pin " + str(pinNum) + " on")

redButton = ttk.Button(root, text="Red", width=25, command=lambda: togglePin(12))
redButton.pack(pady=3)

greenButton = ttk.Button(root, text="Green", width=25, command=lambda: togglePin(13))
greenButton.pack(pady=3)

blueButton = ttk.Button(root, text="Blue", width=25, command=lambda: togglePin(14))
blueButton.pack(pady=3)

blueButton = ttk.Button(root, text="Close", width=25, command=lambda: root.destroy())
blueButton.pack(pady=3)



root.mainloop()