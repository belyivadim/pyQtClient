import sys
import datetime
from PyQt6 import uic, QtCore, QtGui, QtWidgets
import requests
from requests.exceptions import HTTPError
import json


class MainWindow(QtWidgets.QMainWindow):
    server_adress = 'http://localhost:5000'
    message_id = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messanger.ui', self)
        self.sendButton1.clicked.connect(self.send_button_clicked)

    def send_button_clicked(self):
        self.send_message()

    def send_message(self):
        user_name = self.userNameLE.text()
        message_text = self.textLE.text()
        time_stamp = str(datetime.datetime.today())
        msg = f'{{"UserName": "{user_name}", "MessageText": "{message_text}", "TimeStamp": "{time_stamp}"}}'
        print('Сообщение отправлено: ' + msg)
        url = self.server_adress + '/api/Messanger'
        data = json.loads(msg)  # string to json
        r = requests.post(url, json=data)

    def get_message(self, id):
        url = self.server_adress + '/api/Messanger/' + str(id)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            return None
        except Exception as err:
            return None
        else:
            text = response.text
            return text

    def timer_event(self):
        msg = self.get_message(self.message_id)
        while msg is not None:
            msg = json.loads(msg)
            user_name = msg['UserName']
            message_text = msg['MessageText']
            time_stamp = msg['TimeStamp']
            msg_text = f'{time_stamp} <{user_name}>: {message_text}'
            print(msg_text)
            self.messagesWidget.insertItem(self.message_id, msg_text)
            self.message_id += 1
            msg = self.get_message(self.message_id)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timer_event)
    timer.start(5000)
    sys.exit(app.exec())
