import requests
import tkinter


def get_JSON(code_postal): #à un code postal donné retourné le JSON associé
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?zip="+str(code_postal)+",fr&APPID=f856c4048fc25d7f6fd4e7843d31376b&lang=fr")
    json = r.json()
    return json


def convert_Kelvin_to_Celsius(temp): #convertit les températures de K° vers C°
    return round(temp - 273.15, 1)


def get_weather_data(code_postal):
    r = get_JSON(code_postal)
    list_of_weathers = r['weather']
    list_of_weatehers_in_french = []
    for i in list_of_weathers:
        list_of_weatehers_in_french.append(i['description'])
    temperature = convert_Kelvin_to_Celsius(r['main']['temp'])
    pression = r['main']['pressure']
    humidité = r['main']['humidity']
    vitesse_vent = int(3.6*r['wind']['speed']) #convertit les m/s en km/h
    ville = r['name']
    return ville, list_of_weatehers_in_french, temperature, pression, humidité, vitesse_vent


def mise_en_forme_data(meteo_tuple):
    string_weather = "\nLe temps est "+str(meteo_tuple[1][0])
    if len(meteo_tuple[1])>1:
        for i in range(1, len(meteo_tuple[1])):
            string_weather +=" et "+str(meteo_tuple[1][i])
    return "Météo à "+str(meteo_tuple[0])+string_weather+"\nLa température est de "+str(meteo_tuple[2])+" degrés " \
            "Celsius"+"\nLa pressions atmosphérique est de "+str(meteo_tuple[3])+" Pascal"+ \
           "\nLe taux d'humidité est de "+str(meteo_tuple[4])+" %"+"\nLa vitesse du vent est de "+ \
           str(meteo_tuple[5])+" km/h "


def click():
    entered_text = entrée.get()
    output.delete(0.0, tkinter.END)
    try:
        meteo_raw = get_weather_data(int(entered_text))
        texte_a_afficher = mise_en_forme_data(meteo_raw)
    except:
        texte_a_afficher = "Code postal non valide"
    output.insert(tkinter.END, texte_a_afficher)


window = tkinter.Tk()
window.title("Application météo")
label = tkinter.Label(window, text="Entrez le code postal de votre ville.", bg="white")
label.grid(row=0, column=0)
entrée = tkinter.Entry(window, width=20, bg="white")
entrée.grid(row=1, column=0)
buttonName = tkinter.Button(window, text="Ok",  width=6, command=click)
buttonName.grid(row=1, column=1)
output = tkinter.Text(window, width=65, height=10, wrap='word', background='white')
output.grid(row=5, column=0, columnspan=3)
window.mainloop()
