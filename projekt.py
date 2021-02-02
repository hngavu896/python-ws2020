from tkinter import *
from tkinter import messagebox
import requests
import csv

api_key = "198165aa40452785f9fce208b7a6369d"
url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

def getWeather(city):
    data = requests.get(url.format(city, api_key))
    if data:
        json = data.json()
        # It should return a tupple, which is format like this: (City, Country, temp_c, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_k = json['main']['temp']
        temp_c = '{:.2}'.format(temp_k - 273.15)
        weather = json['weather'][0]['main']
        desc = json['weather'][0]['description']
        result = (city, country, temp_c, weather, desc)
        return result
    else:
        return None

def searchWeather():
    city = city_text.get()
    weather = getWeather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        temp_lbl['text'] = weather[2]
        weather_lbl['text'] = weather[3]
        desc_lbl['text'] = weather[4]
    else:
        messagebox.showerror('Error', 'City {}'.format(city) + ' not found')

def saveWeather():
    city = city_text.get()
    data = getWeather(city)
    if data:
        f = open("test.csv", "w", newline="")
        writer = csv.writer(f)
        writer.writerow(data)
        f.close()
        messagebox.showinfo('', 'Successfully saved!')
    else:
        messagebox.showerror('Error', 'Data not found')

root = Tk()
root.title('This is the Python final Project')
root.geometry('700x350')

city_text = StringVar()
city_entry = Entry(root, textvariable=city_text)
city_entry.pack()

searchButton = Button(root, text="Search", width=14, command=searchWeather)
searchButton.pack()

location_lbl = Label(root, text='Location', font=('bold', 20))
location_lbl.pack()
image = Label(root, bitmap='')
image.pack()
temp_lbl = Label(root, text='Temparature')
temp_lbl.pack()
weather_lbl = Label(root, text='Weather')
weather_lbl.pack()
desc_lbl = Label(root, text='Description')
desc_lbl.pack()

saveButton = Button(root, text="Save", width=14, command=saveWeather)
saveButton.pack()

root.mainloop()