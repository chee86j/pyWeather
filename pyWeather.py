import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=imperial&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "city": data["name"],
            "country": data["sys"]["country"]
        }
        return weather_data, None
    else:
        error_message = data.get("message", "Unknown error")
        return None, error_message

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.display_units = "imperial"  # Default Imperial

    def init_ui(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # City input
        city_layout = QHBoxLayout()
        city_label = QLabel("Enter city name:")
        self.city_edit = QLineEdit()
        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_edit)

        # Weather display
        self.weather_display = QTextEdit()
        self.weather_display.setReadOnly(True)

        # Buttons
        button_layout = QHBoxLayout()
        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.get_weather_clicked)
        self.unit_button = QPushButton("Switch Units")
        self.unit_button.clicked.connect(self.switch_units)
        button_layout.addWidget(self.get_weather_button)
        button_layout.addWidget(self.unit_button)

        # Add layouts to main layout
        layout.addLayout(city_layout)
        layout.addWidget(self.weather_display)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def switch_units(self):
        if self.display_units == "imperial":
            self.display_units = "metric"
            self.unit_button.setText("Switch to Imperial")
        else:
            self.display_units = "imperial"
            self.unit_button.setText("Switch to Metric")

        # Fetch weather data again to update the display
        self.get_weather_clicked()

    def get_weather_clicked(self):
        city_name = self.city_edit.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Warning", "Please enter a city name.")
            return

        api_key = os.getenv("API_KEY")
        if not api_key:
            QMessageBox.warning(self, "Error", "API key was not found. Ensure API_KEY is in .env file")
            return

        weather, error_message = get_weather(city_name, api_key)

        if weather:
            self.display_weather(weather)
        else:
            QMessageBox.warning(self, "Error", f"Failed to fetch weather data. Error: {error_message}")

    def display_weather(self, weather):
        if self.display_units == "imperial":
            temperature_unit = "°F"
            temperature = weather["temperature"]
        else:
            temperature_unit = "°C"
            temperature = (weather["temperature"] - 32) * 5/9

        message = f"Weather in {weather['city']}, {weather['country']}:\n"
        message += f"Temperature: {temperature:.2f}{temperature_unit}\n"
        message += f"Humidity: {weather['humidity']}%\n"
        message += f"Description: {weather['description']}"
        self.weather_display.setText(message)

def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
