import pygame
from Epos import epos
import sys
import time

pygame.init()
epos = epos()

# Fenster
WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motorversuch")

font = pygame.font.Font(None, 40)

# Zustände
screen_state = 1

# Daten
auswahl1 = ""
auswahl2 = ""
auswahl3 = ""

antwort0 = None
antwort1 = ""
antwort2 = ""
antwort3 = ""

eingabetext = ""
active = False

sensor_werte = []
zeit_werte = []

startzeit = time.time()

# Eingabefeld
input_box = pygame.Rect(
    WIDTH//2-200,
    300, 
    400, 
    50
)

# Buttons
buttons_jn = [
    pygame.Rect(100, 150, 250, 60),
    pygame.Rect(100, 250, 250, 60)
]


buttons = [
    pygame.Rect(100, 150, 250, 60),
    pygame.Rect(100, 250, 250, 60),
    pygame.Rect(100, 350, 250, 60),
    pygame.Rect(100, 450, 250, 60)
]

motoren = [
    "ACT", 
    "DeltaLine", 
    "Faulhaber", 
    "Maxon"
]

positionen = [
    "Offen",
    "Wechsel",
    "Gespannt",
    "Geschlossen"
]

ja_nein = [
    "Ja",
    "Nein"
]
running = True

while running:
    if epos.controler1.fault == 1:
        sys.exit()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # -------------------
        # Mausklicks
        # -------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Bildschirm 0
            if screen_state == 0:
                for i, button in enumerate(buttons_jn):
                    if button.collidepoint(event.pos):
                        auswahl0 = motoren[i]
                        if auswahl1 == "Ja":
                            screen_state = 2

            # Bildschirm 1
            if screen_state == 1:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        auswahl1 = motoren[i]
                        print(motoren[i])
                        screen_state = 2

            # Bildschirm 2
            elif screen_state == 2:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        auswahl2 = positionen[i]
                        print(positionen[i])
                        screen_state = 3
                        
            # Bildschirm 7
            elif screen_state == 7:
                for i, button in enumerate(buttons_jn):
                    if button.collidepoint(event.pos):
                        auswahl3 = ja_nein[i]
                        print(ja_nein[i])
                        if auswahl3 == "Ja":
                            screen_state = 6
                        else:
                            screen_state = 8
            

            # Fragen
            elif screen_state in [3, 4, 5]:
                active = input_box.collidepoint(event.pos)

            # Ergebnis
            elif screen_state == 6:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        epos.programmablauf(auswahl1, auswahl2, positionen[i], antwort1, antwort2, antwort3)
                        print ("Programmablauf gestartet")

        # -------------------
        # Tastatur
        # -------------------
        if event.type == pygame.KEYDOWN and active:

            if event.key == pygame.K_BACKSPACE:
                eingabetext = eingabetext[:-1]

            elif event.key == pygame.K_RETURN:
                
                if eingabetext.strip() !="" and int(eingabetext) > 0:
                    if screen_state == 3:
                        antwort1 = int(eingabetext)
                        eingabetext = ""
                        screen_state = 4

                    elif screen_state == 4:
                        antwort2 = int(eingabetext)
                        eingabetext = ""
                        screen_state = 5

                    elif screen_state == 5:
                        antwort3 = int(eingabetext)
                        eingabetext = ""
                        screen_state = 6

            else:
                # Nur Zahlen zulassen
                if event.unicode.isdigit():
                    eingabetext += event.unicode

    # -------------------
    # Zeichnen
    # -------------------
    screen.fill((0, 61, 106))

    #
    # Bildschirm 0
    #
    if screen_state == 0:
        titel = font.render(
                    "Wurde die EPOS von der Spannungsversorgung getrennt?", True, (255, 255, 255)
                )
        screen.blit(titel, (100, 50))
        
        for i, button in enumerate(buttons_jn):
            pygame.draw.rect(screen, (0, 158, 224), button)
        
            txt = font.render(
                ja_nein[i],
                True,
                (255, 255, 255)
            )
        
            screen.blit(
                txt,
                (button.x + 20, button.y + 15)
            )
    
    #
    # Bildschirm 1
    #
    elif screen_state == 1:

        titel = font.render(
            "Welcher Motor soll angesteuert werden?", True, (255, 255, 255)
        )
        screen.blit(titel, (100, 50))

        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, (0, 158, 224), button)

            txt = font.render(
                motoren[i],
                True,
                (255, 255, 255)
            )

            screen.blit(
                txt,
                (button.x + 20, button.y + 15)
            )

    #
    # Bildschirm 2
    #
    elif screen_state == 2:

        titel = font.render(
            "In welcher Lage befindet sich das NSE?",
            True,
            (255, 255, 255)
        )

        screen.blit(titel, (250, 50))

        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, (0, 158, 224), button)

            txt = font.render(
                positionen[i],
                True,
                (255, 255, 255)
            )

            screen.blit(
                txt,
                (button.x + 20, button.y + 15)
            )

    #
    # Frage 1
    #
    elif screen_state == 3:

        frage = font.render(
            "Geben Sie eine Motordrehzahl ein:",
            True,
            (255, 255, 255)
        )

        frage_mittig = frage.get_rect(center = (WIDTH //2,200))
        screen.blit(frage, frage_mittig)

    #
    # Frage 2
    #
    elif screen_state == 4:

        frage = font.render(
            "Geben Sie eine Beschleunigung ein:",
            True,
            (255, 255, 255)
        )
        frage_mittig = frage.get_rect(center = (WIDTH //2,200))
        screen.blit(frage, frage_mittig)

    #
    # Frage 3
    #
    elif screen_state == 5:

        frage = font.render(
            "Geben Sie eine Verzögerung ein:",
            True,
            (255, 255, 255)
        )

        frage_mittig = frage.get_rect(center = (WIDTH //2,200))
        screen.blit(frage, frage_mittig)
        sensor_werte.clear()
        zeit_werte.clear()
        startzeit = time.time()

    #
    # Eingabefeld zeichnen
    #
    if screen_state in [3, 4, 5]:

        color = (188, 207, 0) if active else (227, 227, 227)

        pygame.draw.rect(
            screen,
            color,
            input_box,
            2
        )

        txt_surface = font.render(
            eingabetext,
            True,
            (255, 255, 255)
        )

        screen.blit(
            txt_surface,
            (input_box.x + 10, input_box.y + 10)
        )

    #
    # Ergebnis
    #
    elif screen_state == 6:

        titel = font.render(
            "Um das NSE auf die Position zu bewegen, bitte Button drücken",
            True,
            (255, 255, 255)
        )

        screen.blit(titel, (100, 50))
        
        # Infobox
        info_box = pygame.Rect(550,130,370,300)
        pygame.draw.rect(screen, (0, 158, 224), info_box)
        pygame.draw.rect(screen, (188, 207, 0), info_box, 2)
        
                        
        info1 = font.render(
            f"Motor: {auswahl1}",
            True,
            (255, 255, 255)
        )
        
        info2 = font.render(
            f"Startposition: {auswahl2}",
            True,
            (255, 255, 255)
        )
        
        info3 = font.render(
            f"Drehzahl: {antwort1}",
            True,
            (255, 255, 255)
        )
        
        info4 = font.render(
            f"Beschl.: {antwort2}",
            True,
            (255, 255, 255)
        )
        
        info5 = font.render(
            f"Verzög.: {antwort3}",
            True,
            (255, 255, 255)
        )
                
        screen.blit(info1, (570, 150))
        screen.blit(info2, (570, 190))
        screen.blit(info3, (570, 230))
        screen.blit(info4, (570, 270))
        screen.blit(info5, (570, 310))
        
        if epos.kistler.messung_abgeschlossen:
                    epos.kistler.max_spannkraft.append(round(max(epos.kistler.sensorwerte),2))
                    info7 = font.render(
                        f"Max. Spannkraft: {epos.kistler.max_spannkraft [-1]}kN",
                        True,
                        (255, 255, 255)
                    )
                 
                    screen.blit(info7, (570, 390))
        
        if epos.kistler.messung_abgeschlossen:
            durchschnitt_Spannkraft = sum(epos.kistler.max_spannkraft)/len(epos.kistler.max_spannkraft)
            info6 = font.render(
                f"Durchschnitt: {durchschnitt_Spannkraft}",
                True,
                (255, 255, 255)
            )
                       
            screen.blit(info6, (570, 350))
                            

        for i, button in enumerate(buttons):

            pygame.draw.rect(
                screen,
                (0, 158, 224),
                button
            )

            txt = font.render(
                positionen[i],
                True,
                (255, 255, 255)
            )

            screen.blit(
                txt,
                (button.x + 20,
                 button.y + 15)
            )
            
    elif screen_state == 7:
        titel = font.render(
                    "Möchten sie weiter mit dem NSE verfahren?", True, (255, 255, 255)
                )
        screen.blit(titel, (100, 50))
        
        for i, button in enumerate(buttons_jn):
            pygame.draw.rect(screen, (0, 158, 224), button)
        
            txt = font.render(
                ja_nein[i],
                True,
                (255, 255, 255)
            )
        
            screen.blit(
                txt,
                (button.x + 20, button.y + 15)
            )
                    
    elif screen_state == 8:
            titel = font.render(
                        "Das Wars!", True, (255, 255, 255)
                    )
            screen.blit(titel, (100, 50))  
                         
    pygame.display.flip()

pygame.quit()
