import tkinter as tk
from tkinter import ttk
import requests
import time
from PIL import Image, ImageTk

def update_time():
    current_time = time.strftime("%I:%M:%S %p")
    time_label.config(text=current_time)
    time_label.after(1000, update_time)

def data_get():
    city = city_name.get()
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=cd7ab898af24adf218ac5d0f21f01514").json()
    forecast_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=cd7ab898af24adf218ac5d0f21f01514").json()

    w_label1.config(text=weather_data["weather"][0]["main"])
    wb_label1.config(text=weather_data["weather"][0]["description"])
    temp_label1.config(text=str(int(weather_data["main"]["temp"] - 273.15)))
    pres_label1.config(text=weather_data["main"]["pressure"])
    wind_label1.config(text=str(int(weather_data["wind"]["speed"] * 1.6)))
    hum_label1.config(text=weather_data["main"]["humidity"])

    min_temp_label1.config(text=str(int(weather_data["main"]["temp_min"] - 273.15)) + "°C")
    max_temp_label1.config(text=str(int(weather_data["main"]["temp_max"] - 273.15)) + "°C")

    sunrise_time = time.strftime("%I:%M:%S %p", time.gmtime(weather_data["sys"]["sunrise"] + weather_data["timezone"]))
    sunset_time = time.strftime("%I:%M:%S %p", time.gmtime(weather_data["sys"]["sunset"] + weather_data["timezone"]))
    rise_label1.config(text=sunrise_time)
    set_label1.config(text=sunset_time)

    forecast_frame.place(x=15, y=15)
    for i in range(5):
        forecast_time = time.strftime("%I:%M %p", time.gmtime(forecast_data["list"][i]["dt"] + weather_data["timezone"]))
        forecast_temp = str(int(forecast_data["list"][i]["main"]["temp"] - 273.15))
        forecast_desc = forecast_data["list"][i]["weather"][0]["description"]

        forecast_labels[i][0].config(text=forecast_time)
        forecast_labels[i][1].config(text=forecast_temp + "°C")
        forecast_labels[i][2].config(text=forecast_desc)

    current_hour = time.localtime().tm_hour
    if 5 <= current_hour < 12:
        time_of_day = "morning"
    elif 12 <= current_hour < 18:
        time_of_day = "noon"
    else:
        time_of_day = "night"

    weather_main = weather_data["weather"][0]["main"]
    if weather_main == "Clear":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_clear.jpg"))
    elif weather_main == "Clouds":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_clouds.jpg"))
    elif weather_main == "Rain":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_rain.jpg"))
    elif weather_main == "Snow":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_snow.jpg"))
    elif weather_main == "Thunder":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_thunder.jpg"))
    elif weather_main == "Fog":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_fog.jpg"))
    elif weather_main == "Mist":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_mist.jpg"))
    elif weather_main == "Smoke":
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_smoke.jpg"))
    else:
        bg_image = ImageTk.PhotoImage(Image.open(f"{time_of_day}_default.jpg"))

    bg_label.config(image=bg_image)
    bg_label.image = bg_image

win = tk.Tk()
win.title("Weather Forecast")
win.geometry("1200x850")

bg_image = ImageTk.PhotoImage(Image.open("bg.jpg"))
bg_label = tk.Label(win, image=bg_image)
bg_label.place(x=0, y=0, relheight=1, relwidth=1)

def create_image_label(image_path, x, y, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(win, image=photo, bg="green")
    label.image = photo
    label.place(x=x, y=y, width=width, height=height)

forecast_frame = tk.Frame(win, bg='lightblue')
forecast_labels = []
for i in range(5):
    time_label = tk.Label(forecast_frame, text="", font=("Time New Roman", 14))
    temp_label = tk.Label(forecast_frame, text="", font=("Time New Roman", 14))
    desc_label = tk.Label(forecast_frame, text="", font=("Time New Roman", 14))
    time_label.grid(row=i, column=0, padx=5, pady=5)
    temp_label.grid(row=i, column=1, padx=5, pady=5)
    desc_label.grid(row=i, column=2, padx=5, pady=5)
    forecast_labels.append([time_label, temp_label, desc_label])

create_image_label("Weather_Icon.png.jpg", 340, 50, 100, 50)
name_label = tk.Label(win, text="Weather App", font=("Time New Roman", 30, "bold"))
name_label.place(x=465, y=50, height=50, width=430)

time_label = tk.Label(win, text="", font=("Time New Roman", 20))
time_label.place(x=1050, y=10, height=40, width=150)
update_time()

min_temp_label = tk.Label(win, text="Min Temp (°C)", font=("Time New Roman", 10))
min_temp_label.place(x=1000, y=300, height=30, width=100)
min_temp_label1 = tk.Label(win, text="", font=("Time New Roman", 10))
min_temp_label1.place(x=1120, y=300, height=30, width=40)

max_temp_label = tk.Label(win, text="Max Temp (°C)", font=("Time New Roman", 10))
max_temp_label.place(x=1000, y=340, height=30, width=100)
max_temp_label1 = tk.Label(win, text="", font=("Time New Roman", 10))
max_temp_label1.place(x=1120, y=340, height=30, width=40)

city_name = tk.StringVar()
list_name = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
             "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
             "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
             "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
             "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
             "National Capital Territory of Delhi", "Puducherry"]
com = ttk.Combobox(win, values=list_name, font=("Time New Roman", 20, "bold"), textvariable=city_name)
com.place(x=340, y=120, height=50, width=450)

create_image_label("Climate_Icon.png.jpg", 340, 210, 50, 50)
w_label = tk.Label(win, text="Weather Climate", font=("Time New Roman", 20))
w_label.place(x=400, y=210, height=50, width=210)
w_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
w_label1.place(x=625, y=210, height=50, width=210)

create_image_label("Descrip_Icon.png.jpg", 340, 280, 50, 50)
wb_label = tk.Label(win, text="Weather Description", font=("Time New Roman", 17))
wb_label.place(x=400, y=280, height=50, width=210)
wb_label1 = tk.Label(win, text="", font=("Time New Roman", 17))
wb_label1.place(x=625, y=280, height=50, width=210)


create_image_label("Temp_Icon.png.jpg", 340, 350, 50, 50)
temp_label = tk.Label(win, text="Temperature (°C)", font=("Time New Roman", 20))
temp_label.place(x=400, y=350, height=50, width=210)
temp_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
temp_label1.place(x=625, y=350, height=50, width=210)

create_image_label("Press_Icon.png.jpg", 340, 420, 50, 50)
pres_label = tk.Label(win, text="Pressure (mb)", font=("Time New Roman", 20))
pres_label.place(x=400, y=420, height=50, width=210)
pres_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
pres_label1.place(x=625, y=420, height=50, width=210)


create_image_label("Wind_Icon.png.jpg", 340, 490, 50, 50)
wind_label = tk.Label(win, text="Wind (km/h)", font=("Time New Roman", 20))
wind_label.place(x=400, y=490, height=50, width=210)
wind_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
wind_label1.place(x=625, y=490, height=50, width=210)

create_image_label("Humid_Icon.png.jpg", 340, 560, 50, 50)
hum_label = tk.Label(win, text="Humidity (%)", font=("Time New Roman", 20))
hum_label.place(x=400, y=560, height=50, width=210)
hum_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
hum_label1.place(x=625, y=560, height=50, width=210)

create_image_label("Rise_Icon.png.jpg", 340, 630, 50, 50)
rise_label = tk.Label(win, text="Sunrise", font=("Time New Roman", 20))
rise_label.place(x=400, y=630, height=50, width=210)
rise_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
rise_label1.place(x=625, y=630, height=50, width=210)

create_image_label("Set_Icon.png.jpg", 340, 700, 50, 50)
set_label = tk.Label(win, text="Sunset", font=("Time New Roman", 20))
set_label.place(x=400, y=700, height=50, width=210)
set_label1 = tk.Label(win, text="", font=("Time New Roman", 20))
set_label1.place(x=625, y=700, height=50, width=210)

done_button = tk.Button(win, text="Done", font=("Time New Roman", 20, "bold"), command=data_get)
done_button.place(y=120, height=50, width=100, x=800)

win.mainloop()
