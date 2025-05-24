# Weather API App

import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Search", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("HyWeather")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: Verdana;
            }
            QLabel#city_label{
                font-size: 50px; 
                font-weight: bold;
            }
            QLineEdit#city_input{
                font-size: 35px;
                font-weight: bold;
                padding: 15px;
                background-color: #AAAAAA;
                color: #000000;
            }
            QPushButton#get_weather_button{
                font-size: 35px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 50px;
            }
            QLabel#emoji_label{
                font-size: 50px;
            }
            QLabel#description_label{
                font-size: 35px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "ab5bb4a7c615ff8d58b06c161ba61a47"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API Key !")
                case 403:
                    self.display_error("Forbidden\nAccess Denied")
                case 404:
                    self.display_error("Not found\nCity not found !")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later !")
                case 502:
                    self.display_error("Bad gateway\nInvalid server response")
                case 503:
                    self.display_error("Service unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway timeout\nNo server response")
                case _:
                    self.display_error(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.01f}℃\n{temperature_f:.01f}℉")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())