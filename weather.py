import datetime, requests, json
from PySide6.QtWidgets import *

cities = ["Seoul,KR", "Tokyo,JP", "LasVegas,US"]


class Model:
    def __init__(self, city):
        self.city = city
        self.vilage_weather_url = (
            "http://api.openweathermap.org/data/2.5/weather?q={},uk&APPID=".format(
                self.city
            )
        )
        self.service_key = "208bc12659b6799741f2f19621c985d9"

    def get_weather_data(self):
        res = requests.get(self.vilage_weather_url + self.service_key)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.city = cities[0]
        self.model = Model(self.city)
        self.weather = str(self.model.get_weather_data())
        print(self.weather)
        self.setWindowTitle("오늘의 날씨")

        layout = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        self.label = QLabel("오늘의 날씨")
        self.seoul_button = QPushButton("서울")
        self.tokyo_button = QPushButton("도쿄")
        self.lasvegas_button = QPushButton("라스베가스")

        self.seoul_button.pressed.connect(self.seoul)
        self.tokyo_button.pressed.connect(self.tokyo)
        self.lasvegas_button.pressed.connect(self.lasvegas)

        layout.addLayout(layout_left)
        layout.addLayout(layout_right)
        layout_left.addWidget(QLabel(self.weather))
        layout_right.addWidget(self.label)
        layout_right.addWidget(self.seoul_button)
        layout_right.addWidget(self.tokyo_button)
        layout_right.addWidget(self.lasvegas_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def seoul(self):
        self.city = cities[0]
        # self.city가 바꼈음을 emit해줘야함!
        self.model.stringChanged.emit()

    def tokyo(self):
        self.city = cities[1]

    def lasvegas(self):
        self.city = cities[2]


app = QApplication()
window = MainWindow()
window.show()
app.exec()
