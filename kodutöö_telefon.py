import tkinter as tk
import math

#Loome akna
aken = tk.Tk()
aken.title("Kettaga Telefon")
aken.geometry("500x650")

#Joonistamise ala (canvas)
canvas = tk.Canvas(aken, width=400, height=400, bg="white")
canvas.pack(pady=30)

#Ketta keskpunkt
kesk_x = 200
kesk_y = 200

#Aukude ja ringi mõõdud
aukude_raadius = 120
augu_suurus = 20

#Numbrite järjekord kettal
numbrid = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

#Nurkade arvutamiseks vajalikud väärtused
algusnurk = 30
lopunurk = 290
samm = (lopunurk - algusnurk) / 9

#Salvestame aukude asukohad
augud = []

#Pööramise muutujad
lohistamine = False        # kas hiirt hoitakse all
eelmine_nurk = 0           # eelmine hiire nurk
praegune_nurk = 0          # kui palju ketas on pööratud
max_poorang = 270          # maksimaalne pööramine

#Valitud numbri loogika
valitud_auk = None
valitud_augu_max_poorang = 0
stopper_kraad = 300        # metallist stopperi nurk
aktiivne_number = None     # hetkel valitud number
number_valmis = False      # kas number jõudis stopperini

#Sisestatud telefoninumber
sisestatud_number = ""

#Funktsioon kontrollib kas punkt on mõne augu sees
def punkt_augus(px, py, aukude_keskpunktid, raadius):
    for ax, ay in aukude_keskpunktid:
        kaugus = ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
        if kaugus <= raadius - 2:
            return True
    return False

#Lisab numbri telefoninumbrile (ainult siis kui pöörati lõpuni)
def lisa_number():
    global sisestatud_number, aktiivne_number, number_valmis

    if aktiivne_number is not None and number_valmis:
        sisestatud_number += str(aktiivne_number)
        telefoni_ekraan.config(text=f"Telefoninumber: {sisestatud_number}")

    aktiivne_number = None
    number_valmis = False

#Joonistab kogu ketta
def joonista_ketas(nurga_nihe=0):
    global augud
    canvas.delete("all")
    augud = []

    #Välimine hall ketas
    canvas.create_oval(50, 50, 350, 350, fill="grey")

    #Sisemine roheline ring
    canvas.create_oval(120, 120, 280, 280, fill="dark green", outline="black", width=2)

    #Metallist stopper (nooleke)
    stopper_nurk = math.radians(stopper_kraad)

    tipu_raadius = 138
    tx = kesk_x + tipu_raadius * math.cos(stopper_nurk)
    ty = kesk_y - tipu_raadius * math.sin(stopper_nurk)

    #Suund keskpunkti poole
    dx = kesk_x - tx
    dy = kesk_y - ty
    pikkus = math.sqrt(dx**2 + dy**2)

    ux = dx / pikkus
    uy = dy / pikkus

    #Risti suund (noole laiuse jaoks)
    px = -uy
    py = ux

    noole_pikkus = 24
    noole_laius = 10

    #Noole tagumine osa
    bx = tx - ux * noole_pikkus
    by = ty - uy * noole_pikkus

    x1 = bx + px * noole_laius
    y1 = by + py * noole_laius

    x2 = bx - px * noole_laius
    y2 = by - py * noole_laius

    #Joonistame noole
    canvas.create_polygon(tx, ty, x1, y1, x2, y2, fill="silver", outline="black")

    #Arvutame aukude asukohad
    aukude_keskpunktid = []

    for i, number in enumerate(numbrid):
        kraad_auk = algusnurk + i * samm + nurga_nihe
        nurk_auk = math.radians(kraad_auk)

        x_auk = kesk_x + aukude_raadius * math.cos(nurk_auk)
        y_auk = kesk_y - aukude_raadius * math.sin(nurk_auk)

        augud.append((number, x_auk, y_auk))
        aukude_keskpunktid.append((x_auk, y_auk))

        #Joonistame augu
        canvas.create_oval(
            x_auk - augu_suurus, y_auk - augu_suurus,
            x_auk + augu_suurus, y_auk + augu_suurus,
            fill="white", outline="#999999", width=2
        )

    #Joonistame numbrid ainult siis kui need on augu all
    for i, number in enumerate(numbrid):
        kraad_number = algusnurk + i * samm
        nurk_number = math.radians(kraad_number)

        x_number = kesk_x + aukude_raadius * math.cos(nurk_number)
        y_number = kesk_y - aukude_raadius * math.sin(nurk_number)

        if punkt_augus(x_number, y_number, aukude_keskpunktid, augu_suurus):
            canvas.create_text(
                x_number, y_number,
                text=str(number),
                font=("Arial", 16, "bold"),
                fill="black"
            )

#Kuvab valitud numbri
valitud_number = tk.Label(aken, text="Valitud number: ", font=("Arial", 14))
valitud_number.pack()

#Kuvab kogu telefoninumbri
telefoni_ekraan = tk.Label(aken, text="Telefoninumber: ", font=("Arial", 16, "bold"))
telefoni_ekraan.pack(pady=10)

#Hiire vajutus
def hiir_alla(event):
    global lohistamine, eelmine_nurk, valitud_auk, valitud_augu_max_poorang
    global aktiivne_number, number_valmis

    hiir_x = event.x
    hiir_y = event.y

    valitud_auk = None
    lohistamine = False
    number_valmis = False
    aktiivne_number = None

    #Kontrollime kas klikiti auku
    for i, (number, x, y) in enumerate(augud):
        kaugus = ((hiir_x - x) ** 2 + (hiir_y - y) ** 2) ** 0.5

        if kaugus <= augu_suurus:
            valitud_auk = i
            aktiivne_number = number

            #Arvutame kui palju saab seda auku pöörata kuni stopperini
            augu_algne_kraad = algusnurk + i * samm
            valitud_augu_max_poorang = stopper_kraad - augu_algne_kraad

            if valitud_augu_max_poorang < 0:
                valitud_augu_max_poorang += 360

            if valitud_augu_max_poorang > max_poorang:
                valitud_augu_max_poorang = max_poorang

            valitud_number.config(text=f"Valitud number: {number}")

            dx = event.x - kesk_x
            dy = kesk_y - event.y
            eelmine_nurk = math.degrees(math.atan2(dy, dx))

            lohistamine = True
            break

#Hiire liikumine pööravas asendis
def hiir_liigub(event):
    global eelmine_nurk, praegune_nurk, number_valmis

    if not lohistamine or valitud_auk is None:
        return

    dx = event.x - kesk_x
    dy = kesk_y - event.y

    uus_nurk = math.degrees(math.atan2(dy, dx))
    muutus = uus_nurk - eelmine_nurk

    #Parandame nurga hüppe
    if muutus > 180:
        muutus -= 360
    elif muutus < -180:
        muutus += 360

    #Lubame ainult ühes suunas pööramist
    if muutus > 0:
        praegune_nurk += muutus

        #Kui jõuab stopperini, siis number valmis
        if praegune_nurk >= valitud_augu_max_poorang:
            praegune_nurk = valitud_augu_max_poorang
            number_valmis = True

        joonista_ketas(praegune_nurk)

    eelmine_nurk = uus_nurk

#Ketas liigub tagasi
def tagasi_animatsioon():
    global praegune_nurk, valitud_auk

    if praegune_nurk > 0.5:
        praegune_nurk *= 0.9
        joonista_ketas(praegune_nurk)
        aken.after(16, tagasi_animatsioon)
    else:
        praegune_nurk = 0
        joonista_ketas(0)
        lisa_number()
        valitud_auk = None

#Hiire vabastamine
def hiir_yla(event):
    global lohistamine
    lohistamine = False
    tagasi_animatsioon()

#Kustutab viimase numbri
def kustuta_viimane():
    global sisestatud_number
    sisestatud_number = sisestatud_number[:-1]
    telefoni_ekraan.config(text=f"Telefoninumber: {sisestatud_number}")

#Nullib kogu numbri
def nulli_kogu_number():
    global sisestatud_number
    sisestatud_number = ""
    telefoni_ekraan.config(text="Telefoninumber: ")

#Helistamise nupp
def helista():
    if sisestatud_number != "":
        telefoni_ekraan.config(text=f"Helistan: {sisestatud_number}")
    else:
        telefoni_ekraan.config(text="Telefoninumber puudub")

#Nupud
nuppude_raam = tk.Frame(aken)
nuppude_raam.pack(pady=10)

tk.Button(nuppude_raam, text="Kustuta viimane", command=kustuta_viimane).pack(side="left", padx=5)
tk.Button(nuppude_raam, text="Nulli number", command=nulli_kogu_number).pack(side="left", padx=5)
tk.Button(nuppude_raam, text="Helista", command=helista).pack(side="left", padx=5)

#Hiire sündmused
canvas.bind("<Button-1>", hiir_alla)
canvas.bind("<B1-Motion>", hiir_liigub)
canvas.bind("<ButtonRelease-1>", hiir_yla)

#Esmane joonistus
joonista_ketas(0)

aken.mainloop()