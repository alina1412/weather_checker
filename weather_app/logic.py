from weather_app.api_request import WeatherFromApi


class InputDecoder:
    def __init__(self, request) -> None:
        self.last_input = ""
        self.request = request

    def is_english(self, phrase):
        """checks if only letters, spaces, dashes"""
        try:
            phrase.encode(encoding="utf-8").decode("ascii")
        except UnicodeDecodeError:
            return False
        else:
            phrase = phrase.replace(" ", "")
            phrase = phrase.replace("-", "")
            return phrase.isalpha()

    def load_user_input(self):
        """turns name of the city
        'Nizhny Novgorod' -> 'Nizhny+Novgorod'
        'yoshkar-ola -> 'yoshkar+ola '"""
        city = self.request.form.get("p-name", type=str)
        self.last_input = city
        if self.is_english(city):
            city = city.replace("-", " ")
            city = "+".join(city.split(" "))
            return city
        return ""


def save_city_request(db, city, temperature) -> None:
    """save new data to db"""
    query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
    db.run_query(query, (city, temperature))


def processed_request(request, db) -> tuple[str, bool]:
    input_decoder = InputDecoder(request)
    last_input = input_decoder.last_input
    city = input_decoder.load_user_input()
    if not city:
        return (last_input, False)
    temperature = WeatherFromApi().get_temperature(city)
    if temperature is None:
        return (last_input, False)
    temperature = round(temperature, 1)
    save_city_request(db, city, temperature)
    return (last_input, True)


def parse_args(request):
    get_found_s = request.args.get("found", type=str)
    if not get_found_s:
        answer = 1
    elif get_found_s.startswith("False"):
        answer = 0
    else:
        answer = 1
    return answer
