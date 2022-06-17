import mysql.connector
import serial

from PyQt5 import QtWidgets

from listener import Listener
from serial_ports import serial_ports
from typing import Union
from design import design


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port: Union[serial.Serial, None] = None
        self.listener = None
        self.init_elements()
        self.temperature = ""
        self.humidity = ""
        self.getTemperature1.clicked.connect(self.click)
        self.startAir.clicked.connect(self.AirStart)
        self.StopAir.clicked.connect(self.AirStop)
        self.saveData.clicked.connect(self.DataBase)
        self.conditioner = "Stopped"

    def click(self):
        data = str(self.port.readline())
        print(data)
        self.temperature = data[34:36]
        self.humidity = data[56:58]
        self.dispTemp.setText(self.temperature + " \N{DEGREE SIGN}C")
        self.dispHum.setText(self.humidity + "  %")
        self.dispTemp_2.setText(self.temperature + " \N{DEGREE SIGN}C")
        self.dispHum_2.setText(self.humidity + "  %")

    def DataBase(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                database="db_kursova",
                user="root",
                password="xxxx"
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor()

                sql = "INSERT INTO room (temperature, humidity, airConditioning) VALUES (%s, %s, %s)"
                print(sql)
                val = (self.temperature, self.humidity, self.conditioner)
                cursor.execute(sql, val)

                connection.commit()
                cursor.close()
            connection.close()
        except mysql.connector.Error:
            print("Error while connection to database")

    def AirStart(self):
        message = 11
        self.conditioner = "is working"
        self.label_14.setText("Conditioner " + self.conditioner)
        if self.port:
            self.port.write(chr(message).encode('utf-8'))

    def AirStop(self):
        message = 12
        self.conditioner = "stopped"
        self.label_14.setText("Conditioner " + self.conditioner)
        if self.port:
            self.port.write(chr(message).encode('utf-8'))

    def init_elements(self):
        self.comComboBox.addItems(serial_ports())
        self.port = serial.Serial(self.comComboBox.currentText(),
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE,
                                  bytesize=serial.EIGHTBITS,
                                  timeout=2)

    def listen_port(self):
        self.listener = Listener(self.port, self.receive_message)
        self.listener.start()

    def receive_message(self, message):
        print(message.decode("utf-8"))

    def send_message(self, message):
        if self.port:
            self.port.write(str(message).encode("utf-8"))