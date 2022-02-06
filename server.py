from flask import Flask

import file

server = Flask(__name__)


@server.route("/")
def mainPage():
    return '<font size="7">IOT實驗 - 期末專題報告</font>'


@server.route("/light")
def light():
    if file.read_file('web_light_state.txt') == 'ON':
        return '<font size="7">檯燈狀態：ON</font>'
    else:
        return '<font size="7">檯燈狀態：OFF</font>'


@server.route("/light_on")
def light_ON():
    file.write_file('web_light_state.txt', 'ON')
    print('Light ON')
    return '<h3>檯燈：ON!</h3>'


@server.route("/light_off")
def light_OFF():
    file.write_file('web_light_state.txt', 'OFF')
    print('Light OFF')
    return '<h3>檯燈：OFF!</h3>'


if __name__ == '__main__':
    server.run(host="192.168.43.158", port=8080)
