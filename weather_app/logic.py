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

    def load(self):
        return self.request.form.get("p-name", type=str)

    def load_user_input(self):
        """turns name of the city
        'Nizhny Novgorod' -> 'Nizhny+Novgorod'
        'yoshkar-ola -> 'yoshkar+ola'"""
        city = self.load()
        self.last_input = city
        if self.is_english(city):
            changed_city = city.strip()
            changed_city = changed_city.replace("-", " ")
            changed_city = "+".join(changed_city.split(" "))
            return (city, changed_city)
        return ("", "")


def save_city_request(db, city, temperature) -> None:
    """save new data to db"""
    query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
    db.run_query(query, (city, temperature))


def processed_request(request, db) -> tuple[str, bool]:
    input_decoder = InputDecoder(request)
    city, changed_city = input_decoder.load_user_input()
    last_input = input_decoder.last_input
    if not city:
        return (last_input, False)
    temperature = WeatherFromApi().get_temperature(changed_city)
    if temperature is None:
        return (last_input, False)
    temperature = round(temperature, 1)
    save_city_request(db, city, temperature)
    return (last_input, True)
