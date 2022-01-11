import datetime, requests, json
from PySide6.QtCore import QAbstractItemModel, QObject, Signal
from PySide6.QtWidgets import *
from PySide6.QtGui import *

cities = ["Seoul,KR", "Tokyo,JP", "LasVegas,US"]


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.city = cities[0]
        self.model = Model()

        self.setWindowTitle("오늘의 날씨")

        layout = QHBoxLayout()
        widget_left = QWidget()
        widget_left.setFixedSize(250, 200)
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        self.label = QLabel("오늘의 날씨")
        self.seoul_button = QPushButton("서울")
        self.tokyo_button = QPushButton("도쿄")
        self.lasvegas_button = QPushButton("라스베가스")

        self.layout_left_weather_1 = QHBoxLayout()
        self.layout_left_weather_2 = QHBoxLayout()
        self.layout_left_weather_3 = QHBoxLayout()
        self.layout_left_weather_4 = QHBoxLayout()
        self.layout_left_weather_5 = QHBoxLayout()
        self.layout_left_weather_6 = QHBoxLayout()
        self.weather_1_title = QLabel("도시")
        self.weather_1_item = QLabel()
        self.weather_2_title = QLabel("날씨")
        self.weather_2_item = QLabel()
        self.weather_3_title = QLabel("최저기온")
        self.weather_3_item = QLabel()
        self.weather_4_title = QLabel("최고기온")
        self.weather_4_item = QLabel()
        self.weather_5_title = QLabel("습도")
        self.weather_5_item = QLabel()
        self.weather_6_title = QLabel("풍속")
        self.weather_6_item = QLabel()

        self.seoul_button.pressed.connect(self.seoul)
        self.tokyo_button.pressed.connect(self.tokyo)
        self.lasvegas_button.pressed.connect(self.lasvegas)
        self.model.dataChanged.connect(self.update_weather)

        widget_left.setLayout(layout_left)
        layout.addWidget(widget_left)
        layout.addLayout(layout_right)

        for i in range(1, 7):
            getattr(self, f"layout_left_weather_{i}").addWidget(
                getattr(self, f"weather_{i}_title")
            )
            getattr(self, f"layout_left_weather_{i}").addWidget(
                getattr(self, f"weather_{i}_item")
            )
            layout_left.addLayout(getattr(self, f"layout_left_weather_{i}"))

        # layout_left_weather_2.addWidget(self.weather_2_title)
        # layout_left_weather_2.addWidget(self.weather_2_item)
        # layout_left.addLayout(layout_left_weather_2)
        # layout_left_weather_3.addWidget(self.weather_3_title)
        # layout_left_weather_3.addWidget(self.weather_3_item)
        # layout_left.addLayout(layout_left_weather_3)
        # layout_left_weather_4.addWidget(self.weather_4_title)
        # layout_left_weather_4.addWidget(self.weather_4_item)
        # layout_left.addLayout(layout_left_weather_4)
        # layout_left_weather_5.addWidget(self.weather_5_title)
        # layout_left_weather_5.addWidget(self.weather_5_item)
        # layout_left.addLayout(layout_left_weather_5)
        # layout_left_weather_6.addWidget(self.weather_6_title)
        # layout_left_weather_6.addWidget(self.weather_6_item)
        # layout_left.addLayout(layout_left_weather_6)

        layout_right.addWidget(self.label)
        layout_right.addWidget(self.seoul_button)
        layout_right.addWidget(self.tokyo_button)
        layout_right.addWidget(self.lasvegas_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_weather(self, weather_data):
        for i in range(6):
            getattr(self, f"weather_{i+1}_item").setText(str(weather_data[i]))

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
