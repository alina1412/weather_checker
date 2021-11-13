from http.client import HTTPSConnection
from json import loads

Last_input = ""


def getTemperature(city):
    c = HTTPSConnection("api.openweathermap.org")
    c.request('GET', f'/data/2.5/weather?q={city}&units=metric&appid=cb37668bb0f9f472913ecc40fcb08884')
    res = c.getresponse()
    data = res.read()
    data = loads(data)
    # print(data)
    if data and "main" in data:
        return data["main"]["temp"]
    else:
        # print("not found")
        return None


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
    Last_input = city
    if isEnglish(city):
        # print("Eng")
        city = city.replace("-", " ")
        city = "+".join(city.split(" "))
        # Nizhny+Novgorod
        return city


def check_posted_request(request, db):
    global Last_input
    city = users_input(request)
    # print("city--", city)
    if not city:
        return False

    t_in_city = getTemperature(city)
    if t_in_city:
        weather = round(getTemperature(city), 1)
        query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
        db.run_query(query, (Last_input, weather))
        return True
    return False
