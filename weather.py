from functools import partial

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from model import *


class PairItem:
    """layout_left에 들어가는 layout 3개 모아놓은 class"""

    def __init__(self, title, use_icon=False):
        self.setup_widgets(title)
        self.setup_layout(use_icon)

    def setup_widgets(self, title):

        self.title_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()
        self.title_widget = QLabel(title)
        self.icon_widget = QLabel()
        self.icon_widget.setFixedSize(QSize(20, 20))
        self.content_widget = QLabel()

    def setup_layout(self, use_icon):
        if use_icon:
            # self.title_widget.setFixedSize(QSize(40, 20))
            self.title_layout.addWidget(self.title_widget)
            self.title_layout.addWidget(self.icon_widget)
        else:
            self.title_layout.addWidget(self.title_widget)
        self.content_layout.addWidget(self.content_widget)

    def change_content(self, content):
        self.content_widget.setText(content)

    def update_icon(self, icon_path):
        if icon_path:
            self.icon_widget.setPixmap(QPixmap(icon_path))
        else:
            self.icon_widget.setPixmap(QPixmap())
        self.icon_widget.setScaledContents(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.city_buttons = {
            "Seoul,KR": QPushButton("서울"),
            "Tokyo,JP": QPushButton("도쿄"),
            "LasVegas,US": QPushButton("라스베가스"),
            "LA,US": QPushButton("엘에이"),
            "London": QPushButton("런던"),
            "Paris,France": QPushButton("파리"),
        }
        for city, city_button in self.city_buttons.items():
            city_button.autoDefault()
        self.model = Model()
        self.setWindowTitle("오늘의 날씨")
        self.setup_widgets()
        self.setup_layout()
        self.setup_handlers()

    def setup_widgets(self):

        self.pairitem_city = PairItem("도시")
        self.pairitem_weather = PairItem("날씨", use_icon=True)
        self.pairitem_min_temp = PairItem("최저기온")
        self.pairitem_max_temp = PairItem("최고기온")
        self.pairitem_humidity = PairItem("습도")
        self.pairitem_wind = PairItem("풍속")

    def setup_layout(self):

        layout = QHBoxLayout()
        widget_left = QWidget()
        widget_left.setFixedSize(200, 200)
        layout_left = QGridLayout()
        layout_right = QVBoxLayout()

        widget_left.setLayout(layout_left)
        layout.addWidget(widget_left)
        layout.addLayout(layout_right)

        layout_left.addLayout(self.pairitem_city.title_layout, 0, 0)
        layout_left.addLayout(self.pairitem_city.content_layout, 0, 1)
        layout_left.addLayout(self.pairitem_weather.title_layout, 1, 0)
        layout_left.addLayout(self.pairitem_weather.content_layout, 1, 1)
        layout_left.addLayout(self.pairitem_min_temp.title_layout, 2, 0)
        layout_left.addLayout(self.pairitem_min_temp.content_layout, 2, 1)
        layout_left.addLayout(self.pairitem_max_temp.title_layout, 3, 0)
        layout_left.addLayout(self.pairitem_max_temp.content_layout, 3, 1)
        layout_left.addLayout(self.pairitem_humidity.title_layout, 4, 0)
        layout_left.addLayout(self.pairitem_humidity.content_layout, 4, 1)
        layout_left.addLayout(self.pairitem_wind.title_layout, 5, 0)
        layout_left.addLayout(self.pairitem_wind.content_layout, 5, 1)

        for city, city_button in self.city_buttons.items():
            layout_right.addWidget(city_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def update_weather(self, weather_data):
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

            return weather_icon

        self.pairitem_weather.update_icon(get_weather_icon(str(weather_data[1])))
        self.pairitem_city.change_content(str(weather_data[0]))
        self.pairitem_weather.change_content(str(weather_data[1]))
        self.pairitem_min_temp.change_content(str(weather_data[2]))
        self.pairitem_max_temp.change_content(str(weather_data[3]))
        self.pairitem_humidity.change_content(str(weather_data[4]))
        self.pairitem_wind.change_content(str(weather_data[5]))

    def setup_handlers(self):

        for city, city_button in self.city_buttons.items():
            city_button.pressed.connect(partial(self.model.update_weather_data, city))

        self.model.dataChanged.connect(self.update_weather)


app = QApplication()
palette = QPalette()
palette.setColor(QPalette.Window, QColor(0, 128, 255))
palette.setColor(QPalette.WindowText, Qt.white)
app.setPalette(palette)

window = MainWindow()
window.show()
app.exec()
