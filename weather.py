from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from model import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cities = ["Seoul,KR", "Tokyo,JP", "LasVegas,US", "London", "Paris,France"]
        self.city = self.cities[0]
        self.model = Model()
        self.setWindowTitle("오늘의 날씨")
        self.setup_widgets()
        self.setup_layout()
        self.setup_handlers()

    def setup_widgets(self):

        self.seoul_button = QPushButton("서울")
        self.tokyo_button = QPushButton("도쿄")
        self.lasvegas_button = QPushButton("라스베가스")
        self.london_button = QPushButton("런던")
        self.paris_button = QPushButton("파리")

        self.layout_left_weather_1 = QHBoxLayout()
        self.layout_left_weather_2 = QHBoxLayout()
        self.layout_left_weather_3 = QHBoxLayout()
        self.layout_left_weather_4 = QHBoxLayout()
        self.layout_left_weather_5 = QHBoxLayout()
        self.layout_left_weather_6 = QHBoxLayout()
        self.weather_1_title = QLabel("도시")
        self.weather_1_item = QLabel()
        self.weather_2_title = QLabel("날씨")
        self.weather_2_icon = QLabel()
        self.weather_2_item = QLabel()
        self.weather_3_title = QLabel("최저기온")
        self.weather_3_item = QLabel()
        self.weather_4_title = QLabel("최고기온")
        self.weather_4_item = QLabel()
        self.weather_5_title = QLabel("습도")
        self.weather_5_item = QLabel()
        self.weather_6_title = QLabel("풍속")
        self.weather_6_item = QLabel()

    def setup_layout(self):

        layout = QHBoxLayout()
        widget_left = QWidget()
        widget_left.setFixedSize(250, 200)
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        widget_left.setLayout(layout_left)
        layout.addWidget(widget_left)
        layout.addLayout(layout_right)

        # for i in range(1, 7):
        #     getattr(self, f"layout_left_weather_{i}").addWidget(
        #         getattr(self, f"weather_{i}_title")
        #     )
        #     getattr(self, f"layout_left_weather_{i}").addWidget(
        #         getattr(self, f"weather_{i}_item")
        #     )
        #     layout_left.addLayout(getattr(self, f"layout_left_weather_{i}"))

        self.layout_left_weather_1.addWidget(self.weather_1_title)
        self.layout_left_weather_1.addWidget(self.weather_1_item)
        layout_left.addLayout(self.layout_left_weather_1)
        self.layout_left_weather_2.addWidget(self.weather_2_title)
        self.weather_2_title.setFixedSize(QSize(30, 20))
        self.layout_left_weather_2.addWidget(self.weather_2_icon)
        self.layout_left_weather_2.addSpacerItem(QSpacerItem(50, 20))
        self.layout_left_weather_2.addWidget(self.weather_2_item)
        self.weather_2_icon.setFixedSize(QSize(20, 20))
        layout_left.addLayout(self.layout_left_weather_2)
        self.layout_left_weather_3.addWidget(self.weather_3_title)
        self.layout_left_weather_3.addWidget(self.weather_3_item)
        layout_left.addLayout(self.layout_left_weather_3)
        self.layout_left_weather_4.addWidget(self.weather_4_title)
        self.layout_left_weather_4.addWidget(self.weather_4_item)
        layout_left.addLayout(self.layout_left_weather_4)
        self.layout_left_weather_5.addWidget(self.weather_5_title)
        self.layout_left_weather_5.addWidget(self.weather_5_item)
        layout_left.addLayout(self.layout_left_weather_5)
        self.layout_left_weather_6.addWidget(self.weather_6_title)
        self.layout_left_weather_6.addWidget(self.weather_6_item)
        layout_left.addLayout(self.layout_left_weather_6)

        layout_right.addWidget(self.seoul_button)
        layout_right.addWidget(self.tokyo_button)
        layout_right.addWidget(self.lasvegas_button)
        layout_right.addWidget(self.london_button)
        layout_right.addWidget(self.paris_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_weather(self, weather_data):
        # for i in range(6):
        #     getattr(self, f"weather_{i+1}_item").setText(str(weather_data[i]))
        def get_weather_icon(weather):
            weather_icon = ""
            icon_cloudy = "./icon/weather-2191838-1846632.webp"
            icon_sunny = "./icon/OOjs_UI_icon_sun-ltr.svg.png"
            icon_rainy = "./icon/ebb8cae74691fb1445849ddaa766d2c6.png"
            icon_mist = "./icon/651098.png"
            if "sky" in weather:
                weather_icon = icon_sunny
            elif "clouds" in weather:
                weather_icon = icon_cloudy
            elif "rain" in weather:
                weather_icon = icon_rainy
            elif "mist" in weather:
                weather_icon = icon_mist

            if weather_icon:
                return QPixmap(weather_icon)

        self.weather_1_item.setText(str(weather_data[0]))
        self.weather_2_icon.setPixmap(get_weather_icon(str(weather_data[1])))
        self.weather_2_icon.setScaledContents(True)
        self.weather_2_item.setText(str(weather_data[1]))
        self.weather_3_item.setText(str(weather_data[2]))
        self.weather_4_item.setText(str(weather_data[3]))
        self.weather_5_item.setText(str(weather_data[4]))
        self.weather_6_item.setText(str(weather_data[5]))

    def setup_handlers(self):
        def seoul():
            self.model.update_weather_data(self.cities[0])

        def tokyo():
            self.model.update_weather_data(self.cities[1])

        def lasvegas():
            self.model.update_weather_data(self.cities[2])

        def london():
            self.model.update_weather_data(self.cities[3])

        def paris():
            self.model.update_weather_data(self.cities[4])

        self.seoul_button.pressed.connect(seoul)
        self.tokyo_button.pressed.connect(tokyo)
        self.lasvegas_button.pressed.connect(lasvegas)
        self.london_button.pressed.connect(london)
        self.paris_button.pressed.connect(paris)
        self.model.dataChanged.connect(self.update_weather)


app = QApplication()
palette = QPalette()
palette.setColor(QPalette.Window, QColor(0, 128, 255))
palette.setColor(QPalette.WindowText, Qt.white)
app.setPalette(palette)

window = MainWindow()
window.show()
app.exec()
