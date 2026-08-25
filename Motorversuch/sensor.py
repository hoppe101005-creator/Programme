import snap7
from snap7.util import get_real
import matplotlib.pyplot as plt
from collections import deque
import time


class sensor:

    def __init__(
        self,
        ip="192.168.0.,1",
        rack=0,
        slot=1,
        db_nummer=10,
        startadresse=0,
        max_punkte=1000
    ):

        self.db_nummer = db_nummer
        self.startadresse = startadresse

        self.plc = snap7.client.Client()

        print("Verbinde mit SPS...")
        self.plc.connect("192,168,6,4", 0, 1)

        if self.plc.get_connected():
            print("Verbindung erfolgreich")
        else:
            raise Exception("Verbindung zur SPS fehlgeschlagen")

        self.zeitwerte = deque(maxlen=max_punkte)
        self.sensorwerte = deque(maxlen=max_punkte)

    def sensor_auslesen(self):
        """
        Liest einen REAL-Wert aus der SPS.
        """

        try:
            daten = self.plc.db_read(
                self.db_nummer,
                self.startadresse,
                4
            )

            wert = get_real(daten, 0)

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

            while True:

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

        except KeyboardInterrupt:

            print("Messung beendet")

        finally:

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

if __name__ == "__main__":

    sensor = sensor(
        ip="192.168.6.4",   # IP-Adresse der SPS
        rack=0,
        slot=1,
        db_nummer=31,
        startadresse=0
    )

    sensor.messung_starten()
    
