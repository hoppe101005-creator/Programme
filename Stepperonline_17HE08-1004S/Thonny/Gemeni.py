import machine
import sys
import utime

# 1. Pins am Raspberry Pi Pico definieren
PUL_PIN = 2
DIR_PIN = 3
INTERRUPT_PIN = 16
ENA_PIN = 17
NOT_AUS_PIN = 15

pul = machine.Pin(PUL_PIN, machine.Pin.OUT)
dir = machine.Pin(DIR_PIN, machine.Pin.OUT)
interrupt = machine.Pin(INTERRUPT_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
ena = machine.Pin(ENA_PIN, machine.Pin.OUT)
Not_Aus = machine.Pin(NOT_AUS_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# 2. Einstellungen für deinen Schrittmotor & TB6600
SCHRITTE_PRO_UMDREHUNGEN = 200
ZYKLEN = 5
GESCHWINDIGKEIT = 0.001 # 1ms Pause für Konstantfahrt (Schnell)
BESCHLEUNIGUNG = 0.01   # Reduziert die Pause pro Schritt um 10ms
WARTEZEIT = 0.1
ABBRUCH = False

def beschleunigen_und_drehen(schritte, richtung):
    """
    Beschleunigt den Motor, bis die Pausenzeit die Zielgeschwindigkeit erreicht.
    Fängt Fehler ab und schaltet automatisch in die Konstantfahrt um.
    """
    dir.value(richtung)
    ena.value(0) # Motor aktivieren (Kraft aufbauen)
    
    i = 0
    schritte_gefahren = 0
    
    # 1. BESCHLEUNIGUNGSPHASE
    while True:
        i += 1
        pausen_zeit = 0.2 - (i * BESCHLEUNIGUNG) # Startet bei 190ms Pause und wird schneller
        
        # Sobald die Rampe schneller als die Wunschgeschwindigkeit wird: Breche ab!
        if pausen_zeit <= GESCHWINDIGKEIT:
            break
            
        try:
            pul.value(1)
            utime.sleep(pausen_zeit) # Wenn pausen_zeit negativ würde, gäbe es hier einen Fehler
            pul.value(0)
            utime.sleep(pausen_zeit)
            schritte_gefahren += 1
        except:
            # Falls mathematisch doch ein Fehler passiert (z.B. negativer Sleep-Wert)
            break
            
    # 2. KONSTANTFAHRT (Fährt den Rest der 5 Umdrehungen)
    gesamtschritte = schritte * 5
    rest_schritte = gesamtschritte - schritte_gefahren
    
    if rest_schritte > 0:
        for _ in range(rest_schritte):
            pul.value(1)
            utime.sleep(GESCHWINDIGKEIT)
            pul.value(0)
            utime.sleep(GESCHWINDIGKEIT)
            
    ena.value(1) # Motor im Stillstand ausschalten

def not_aus(pin):
    ena.value(1)
    pul.value(0)
    print("\nNOT-AUS betätigt. Programm beendet.")
    ABBRUCH = True

# --- HAUPTPROGRAMM ---
Not_Aus.irq(handler=not_aus, trigger=machine.Pin.IRQ_FALLING)
ena.value(1)

print("System bereit. Warte auf Startsignal...")

while ABBRUCH == False:
    if ABBRUCH == True:
        sys.exit()
    elif interrupt.value() == 0:
        print("Startsignal empfangen. Beginne Zyklen...")
        for i in range(ZYKLEN):
            print(f"Zyklus {i+1}/{ZYKLEN}: Im Uhrzeigersinn...")
            beschleunigen_und_drehen(SCHRITTE_PRO_UMDREHUNGEN, 1)
            utime.sleep(WARTEZEIT)
        
            print(f"Zyklus {i+1}/{ZYKLEN}: Gegen den Uhrzeigersinn...")
            beschleunigen_und_drehen(SCHRITTE_PRO_UMDREHUNGEN, 0) # KORREKTUR: Richtung 0
            utime.sleep(WARTEZEIT)
            
        print("Alle Zyklen beendet. Bereits für nächsten Start.")
    
    ena.value(1)
    utime.sleep(0.05)
