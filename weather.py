import datetime, requests, json
from PySide6.QtCore import QAbstractItemModel, QObject, Signal
from PySide6.QtWidgets import *
from PySide6.QtGui import *

cities = ["Seoul,KR", "Tokyo,JP", "LasVegas,US"]


class Model(QObject):
    dataChanged = Signal(dict)

    def __init__(self):
        super().__init__()
        self.service_key = "208bc12659b6799741f2f19621c985d9"

    def get_weather_data(self, city):
        def get_vilage_weather_url(city):
            return f"http://api.openweathermap.org/data/2.5/weather?q={city},uk&APPID="

        res = requests.get(get_vilage_weather_url(city) + self.service_key)
        data = json.loads(res.text)
        data_dic = {
            "도시": data["name"],
            "날씨": data["weather"][0]["description"],
            "최저기온": round(data["main"]["temp_min"] - 273, 2),
            "최고기온": round(data["main"]["temp_max"] - 273, 2),
            "습도": data["main"]["humidity"],
            "풍속": data["wind"]["speed"],
        }
        return data_dic

    def update_weather_data(self, city):
        update_data_dic = self.get_weather_data(city)
        self.dataChanged.emit(update_data_dic)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.city = cities[0]
        self.model = Model()

        self.setWindowTitle("오늘의 날씨")

        layout = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        self.label = QLabel("오늘의 날씨")
        self.seoul_button = QPushButton("서울")
        self.tokyo_button = QPushButton("도쿄")
        self.lasvegas_button = QPushButton("라스베가스")

        self.weather_label = QLabel("Click Button!")

        self.seoul_button.pressed.connect(self.seoul)
        self.tokyo_button.pressed.connect(self.tokyo)
        self.lasvegas_button.pressed.connect(self.lasvegas)
        self.model.dataChanged.connect(self.update_weather)

        layout.addLayout(layout_left)
        layout.addLayout(layout_right)
        layout_left.addWidget(self.weather_label)
        layout_right.addWidget(self.label)
        layout_right.addWidget(self.seoul_button)
        layout_right.addWidget(self.tokyo_button)
        layout_right.addWidget(self.lasvegas_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_weather(self, weather_data):
        self.weather_label.setText(str(weather_data))

    def seoul(self):
        self.city = cities[0]
        self.model.update_weather_data(self.city)

    def tokyo(self):
        self.city = cities[1]
        self.model.update_weather_data(self.city)

    def lasvegas(self):
        self.city = cities[2]
        self.model.update_weather_data(self.city)


app = QApplication()
window = MainWindow()
window.show()
app.exec()
