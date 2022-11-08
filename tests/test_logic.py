import pytest
import mock

from weather_app.config.config import Settings
from weather_app.db_editor import DatabaseEditor
from weather_app.logic import InputDecoder, processed_request


def test_home_page_with_fixture(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "input_query, found",
    [
        ("moscow", True),
        ("", False),
        ("berlin", True),
    ],
)
def test_processed_request_function(input_query, found):
    db = DatabaseEditor()
    city = input_query

    assert Settings().openweather_api_key is not None

    with mock.patch("weather_app.logic.InputDecoder.load", return_value=city):
        last_input, isfound = processed_request(input_query, db)
        assert last_input == city
        assert isfound == found


@pytest.mark.parametrize(
    "input_query, city_after",
    [
        ("moscow", "moscow"),
        ("Nizhny Novgorod", "Nizhny+Novgorod"),
        ("yoshkar-ola ", "yoshkar+ola"),
    ],
)
def test_parsing(input_query, city_after):
    input_decoder = InputDecoder("")
    with mock.patch("weather_app.logic.InputDecoder.load", return_value=input_query):
        city, changed_city = input_decoder.load_user_input()
        assert input_query == city
        assert city_after == changed_city
