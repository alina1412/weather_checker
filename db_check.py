from http.client import HTTPSConnection
import json

Last_input = ""


def getTemperature(city):
    c = HTTPSConnection("api.openweathermap.org")
    # city = 'Moscow' # input()
    c.request('GET', f'/data/2.5/weather?q={city}&units=metric&appid=cb37668bb0f9f472913ecc40fcb08884')
    res = c.getresponse()
    data = res.read()
    data = json.loads(data)
    # print(data)
    if data and "main" in data:
        return data["main"]["temp"]
    else:
        # print("unfortunately, no such city found")
        return None
    # return None


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        s = s.replace(" ", "")
        s = s.replace("-", "")
        return s.isalpha()


def users_input(request):
    global Last_input
    city = request.form.get("p-name", type=str)
    # Nizhny+Novgorod
    Last_input = city
    if isEnglish(city):
        print("Eng")
        city = city.replace("-", " ")
        city = "+".join(city.split(" "))
        return city


def cpost(request, db):
    global Last_input
    city = users_input(request)
    if not city:
        return False

    t_in_city = getTemperature(city)
    if t_in_city:
        weather = round(getTemperature(city), 1)
         
        query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
        db.insert(query, (Last_input, weather))
        return True
    return False