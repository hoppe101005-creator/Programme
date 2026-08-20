import tkinter  as tk
from tkinter import ttk
import controler

controler = controler()

root = tk.Tk()
root.title("Steuerung Motorversuch NSE-E mini 90-25 IOL")
root.geometry("800x600")

Drehzahl = tk.IntVar(value=1000)
Beschlaeunigung = tk.IntVar(value=5000)
Bremsen = tk.IntVar(value=5000)

Offen = controler.position_einlesen("end_position_lose.txt")
Spannen = controler.position_einlesen("end_position_gespannt.txt")
Werkstück = controler.position_einlesen("position_werkstück_wechsel.txt")

tk.Label(root, text = "Drehzahl").grid(row=0, column=0)
Drehzahl = tk.Entry(root)
Drehzahl.insert(0, "2000")
Drehzahl.grid(row = 0, column = 1)

tk.Label(root, text = "Beschläunigung").grid(row=1, column=0)
Beschlaeunigung = tk.Entry(root)
Beschlaeunigung.insert(0, "10000")
Beschlaeunigung.grid(row = 1, column = 1)

tk.Label(root, text = "Bremsen").grid(row=2, column=0)
Bremsen = tk.Entry(root)
Bremsen.insert(0, "10000")
Bremsen.grid(row = 2, column = 1)

def parameter_übernehmen():
    controler.geschwindigkeit = int(Drehzahl.get())
    controler.beschleunigung = int(Beschlaeunigung.get())
    controler.verzögerung = int(Bremsen.get())
    print("Neue Parameter gesetzt")
    
    
def fahre_zu_position(position):
    parameter_übernehmen()
    controler.nse_zu_position_bewegen(position)

def fahren(position):
    vel = Drehzahl.get()
    acc = Beschlaeunigung.get()
    dec = Bremsen.get()
    
    print ("Fahre nach", position, "mit v=", vel, ",a=", acc, ", d=", dec)
    
    fahre_zu_position(position)
    
    
offen = ttk.Button(
    root,
    text = "Offen",
    command = lambda: fahren(Offen)
)

offen.grid(row = 4, column = 0, pady = 20)
    
    
werkstück = ttk.Button(
    root,
    text = "Werkstück",
    command = lambda: fahren(Werkstück)
)

werkstück.grid(row = 4, column = 1, pady = 20)

spannen = ttk.Button(
    root,
    text = "Spannen",
    command = lambda: fahren(Spannen)
)

spannen.grid(row = 4, column = 2, pady = 20)

position_Label = tk.label(root, text="Position:---")

position_Label.grid(row=5, column=0, columnspan=3)


def position_aktualisieren():
    pos = controler.aktuelle_position_auslesen()
    position_Label.config(text=f"Position: {pos}")
    root.after(500, position_aktualisieren)



controler.open_device()
position_aktualisieren()
root.mainloop()