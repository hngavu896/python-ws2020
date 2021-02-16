# Alle benötige Bibliothek importieren. Ich nutze Tkinter um die Benutzerschnittstelle meines Apps umzusetzen;
# requests um die API abzurufen; pandas um mit DataFrame und Tabelle umzugehen; und letztendlich, matlablib zu ploten
from tkinter import *
from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt

# API Adresse - Zahlen aus Gesundheitsämter der Länder und RKI. Deswegen in den letzten Fälle ab 2021, es umfasst in
# einem Tag Statistics aus 2 Quellen. Das Diagramm kann deswegen nicht 100% korrekt.
url = "https://api.public.fusionbase.io/cases/filter?kreis_name={}&start_date={}"

# Eine Funktion, um API abzurufen. Es wird wieder in 3 Funktionen: "Search", "Save", "Show Graphic" verwendet
def callAPI():
    city = city_text.get()
    date = date_text.get()
    # GET-Methode, um die Eingabe von Nutzer zu rufen
    data = requests.get(url.format(city, date))
    return data

# callAPI-Funktion erst aktivieren, dereb Response wird als .json-Datei umwandelt. Man verweist die Position der
# benötigten Informationen in der Dictionary, die danach der Text von Label ersetzt
def searchCity():
    response = callAPI()
    if response:
        json = response.json()
        location_lbl['text'] = json[0]['location_label']
        case_lbl['text'] = 'Infizierte: {}'.format(json[0]['cases']) + '\nDifferenz zum Vortag: {}'.format(json[0]['relative_case_changes'])
        case_dens_lbl['text'] = 'Anzahl pro 100,000 Einwohner: {}'.format(json[0]['cases_per_100k'])
        death_lbl['text'] = 'Tod: {}'.format(json[0]['deaths']) + '\nDifferenz zum Vortag: {}'.format(json[0]['relative_death_changes'])
        return json
    else:
        # Fehlermeldung über Messagebox von Tkinter
        messagebox.showerror('Error', 'Information not found')
    
# callAPI aktivieren. Json-Datei wird mit Pandas zum Dataframe umwandelt, danach als .xlsx-Datei gespeichert.
# Data wird auch aufgeräumt bevor Speichern
def save():
    response = callAPI()
    if response:
        json = response.json()
        city = json[0]['location_label']
        df = pd.DataFrame(json)
        df.drop(['fb_id', 'fb_datetime'], axis=1, inplace=True)
        df.to_excel("Covid-Statistic in {}.xlsx".format(city))
        messagebox.showinfo('Complete', 'File have successfully saved')
    else:
        messagebox.showerror('Error', 'There have been error occurred')

# callAPI aktivieren. Durch diese Funktion wird ein Diagramm aus Anzahl der Infizierten täglich angezeigt.
# Weil die Zeit-Formate aus Json-Datei zu lang ist, wird nur Datum daraus extrahiert. Wir schon von Anfang erwähnt, das
# Diagramm ist nicht 100% korrekt, aber sieht man die Tendenz.
def graph():
    response = callAPI()
    if response:
        json = response.json()
        city = json[0]['location_label']
        df = pd.DataFrame(json)
        df['publication_datetime'] = pd.to_datetime(df['publication_datetime'])
        date = df['publication_datetime'].dt.date
        # Using Matlaplib to plot with 3 data: date, case, case per 100k
        cases = df['cases']
        plt.plot(date, cases)
        plt.xlabel('Datum')
        plt.ylabel('Anzahl der infizierten Personen')
        plt.title('Covid Statistic in {}'.format(city))
        plt.show()
    else:
        messagebox.showerror('Error', 'There have been error occurred')

# Gestaltung von Benutzerschnittstelle
app = Tk()
app.title('Real-Time Corona Statistic in Germany')
app.geometry('500x600')

myLabel = Label(app, text='Aktuelle Corona-Lage', font=('bold', 20)).pack()
location_lbl = Label(app, text='Location', font=('bold', 16))
location_lbl.pack()
case_lbl = Label(app, text='Anzahl von Infizierte')
case_lbl.pack()
case_dens_lbl = Label(app, text='Infizierte/100k Einwohner')
case_dens_lbl.pack()
death_lbl = Label(app, text='Anzahl von Toden')
death_lbl.pack()

#Frame für Steuerung
frame = LabelFrame(app, text="Control Panel")
frame.place(height=210, width=500, rely=0.65, relx=0)

city_input_lbl = Label(frame, text = 'Landkreis: ', pady=4).pack()
city_text = StringVar()
city_input = Entry(frame, textvariable=city_text, width=200)
city_input.pack()
city_input.insert(0, "Hamburg")
date_input_lbl = Label(frame, text = 'Seit wann: ', pady=5).pack()
date_text = StringVar()
date_input = Entry(frame, textvariable=date_text, width=200)
date_input.pack()
date_input.insert(0, "2020-02-03")

button1 = Button(frame, text="Stat aktualisieren", command = searchCity, width=18, pady=3)
button1.pack()
button2 = Button(frame, text="Stats speichern", command = save, width = 18, pady=3)
button2.pack()
button3 = Button(frame, text="Grafik zeigen", command = graph, width = 18, pady=3)
button3.pack()

app.mainloop()