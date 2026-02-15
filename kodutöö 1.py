def number_rooma_numbriks(number):
    #Kontroll, et arv oleks sobivas vahemikus
    if number < 1 or number > 1000:
        return ("Palun sisesta arv vahemikus 1-1000.")
    #Nimekirjad arvudest ja sümbolitest
    arvud = [
        1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1
    ]

    rooma_numbrid = [
        "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"
    ]

    rooma_number = ""

    #Läbib kõik väärtused suurimast väiksemani
    for i in range(len(arvud)):
        #Kui väärtus mahub arvu sisse
        while number >= arvud[i]:
            #Lisame sobiva rooma sümboli
            rooma_number += rooma_numbrid[i]
            #Lahutame väärtuse arvust
            number -= arvud[i]
    return rooma_number

#Küsib kasutajalt arvu
user_input = int(input("Sisesta täisarv 1-1000:"))
#Teisandab ja väljastab tulemuse
result = number_rooma_numbriks(user_input)
print("Rooma number:", result)
