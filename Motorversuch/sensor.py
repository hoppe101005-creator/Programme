import snap7
from snap7.util import get_real
from snap7.util import set_bool
import matplotlib.pyplot as plt
from collections import deque
import time


class sensor:

    def __init__(
        self,
        ip="192.168.6.4",
        rack=0,
        slot=1,
        db_nummer=31,
        sensoradresse=2,
        max_punkte=1000
    ):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.db_nummer = db_nummer
        self.sensoradresse = sensoradresse
        self.zeitwerte = deque(maxlen=max_punkte)
        self.sensorwerte = deque(maxlen=max_punkte)
        self.messen = 200

        self.plc = snap7.client.Client()
        self.data = None
        self.data_bool = None
        self.messung_abgeschlossen = False

    def verbinde_sps(self):
        print("Verbinde mit SPS...")
        self.plc.connect(self.ip, self.rack, self.slot)

        if self.plc.get_connected():
            print("Verbindung erfolgreich")
        else:
            raise Exception("Verbindung zur SPS fehlgeschlagen") 

    def sensor_auslesen(self):
        """
        Liest einen REAL-Wert aus der SPS.
        """
        try:
            daten = self.plc.db_read(
                self.db_nummer,
                self.sensoradresse,
                4
            )

            print("Daten:",daten)
            
            wert = get_real(daten, 0)

            print ("Wert:", wert)
            
            return wert

        except Exception as e:
            print(f"Fehler beim Auslesen: {e}")
            return None

    def messung_starten(self):

        plt.ion()

        fig, ax = plt.subplots()

        linie, = ax.plot([], [], color="blue")

        ax.set_title("Kraftmessung Siemens SPS")
        ax.set_xlabel("Zeit [s]")
        ax.set_ylabel("Kraft")
        ax.grid(True)

        startzeit = time.time()

        try:

            for i in range(self.messen):

                wert = self.sensor_auslesen()

                if wert is not None:

                    aktuelle_zeit = time.time() - startzeit

                    self.zeitwerte.append(aktuelle_zeit)
                    self.sensorwerte.append(wert)

                    linie.set_xdata(self.zeitwerte)
                    linie.set_ydata(self.sensorwerte)

                    ax.relim()
                    ax.autoscale_view()

                    plt.draw()
                    plt.pause(0.05)
                    wert = self.sensor_auslesen()
                    print("Wert:", wert)
                i+=1    
                    

        except KeyboardInterrupt:

            print("Messung beendet")

    def trenne_sps(self):
        self.plc.disconnect()
        self.plc.destroy()
        print("Verbindung zur SPS geschlossen")

    def diagramm_anzeigen(self, zeit_werte, sensor_werte):
        plt.plot(zeit_werte, sensor_werte)
        plt.xlabel("Zeit [s]")
        plt.ylabel("Sensorsignal")
        plt.title("Kistler Messung")
        plt.grid(True)
        plt.show()
        
    def kallibrieren(self):
        self.data_bool = self.plc.db_read(31, 4, 1)
        print(self.data_bool)
        set_bool(self.data_bool, 0, 0, True)
        self.plc.db_write(31, 2, self.data_bool)
        print("Kalibrieren = True")
        time.sleep(1)
        set_bool(self.data_bool, 0, 0, False)
        self.plc.db_write(31, 2, self.data_bool)
        print("Kalibrieren = False")

    def mess_ablauf(self):
        self.verbinde_sps()
        self.kallibrieren()
        wert = None
        wert = self.sensor_auslesen()
        self.messung_starten()
        print (wert)
        self.trenne_sps()
        self.messung_abgeschlossen = True
        
if __name__ == "__main__":

    sensor = sensor(
        ip="192.168.6.4",   # IP-Adresse der SPS
        rack=0,
        slot=1,
        db_nummer=31,
        sensoradresse=0
    )

    sensor.mess_ablauf()
    
