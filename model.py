from PySide6.QtCore import QAbstractItemModel, QObject, Signal
import requests, json


class Model(QObject):
    dataChanged = Signal(list)

    def __init__(self):
        super().__init__()
        self.service_key = "208bc12659b6799741f2f19621c985d9"

    def get_weather_data(self, city):
        def get_vilage_weather_url(city):
            return f"http://api.openweathermap.org/data/2.5/weather?q={city},uk&APPID="

        res = requests.get(get_vilage_weather_url(city) + self.service_key)
        data = json.loads(res.text)
        data_list = [
            data["name"],
            data["weather"][0]["description"],
            round(data["main"]["temp_min"] - 273, 2),
            round(data["main"]["temp_max"] - 273, 2),
            data["main"]["humidity"],
            data["wind"]["speed"],
        ]
        return data_list

    def update_weather_data(self, city):
        update_data_list = self.get_weather_data(city)
        self.dataChanged.emit(update_data_list)
