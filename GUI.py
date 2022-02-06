import serial
import tkinter as tk
from tkinter.font import Font

from time import strftime
from datetime import date

from threading import Thread

from lineTool import lineNotify

import file


class APP:
    # 初始化設定。
    def __init__(self):
        # 設置GUI介面權限
        self.window = tk.Tk()
        # 設置GUI介面標題
        self.window.title('IOT系統實驗')

        # 螢幕寬度
        self.screen_width = self.window.winfo_screenwidth()
        # 螢幕高度
        self.screen_height = self.window.winfo_screenheight()

        # 設置視窗置中
        screen_x = str(int((self.screen_width - 800) / 2))
        screen_y = str(int((self.screen_height - 600) / 2))

        # 設置GUI介面視窗大小為800x600
        self.window.geometry('800x600' + '+' + screen_x + '+' + screen_y)
        # 固定GUI介面視窗大小(不可調整)
        self.window.resizable(False, False)
        # 設置GUI介面視窗背景為白色
        self.window.configure(background='white')

        # Line Notify通知權杖。
        self.line_token = 'YUzttetMNYFQrNaVSdHNZI2RwcTjBzjDxlgJRsHTGwK'

        # 初始化Arduino UNO serial通訊連接。
        # self.init_serial()

        # 宣告按鈕圖示。
        self.on = tk.PhotoImage(file="on.png")
        self.off = tk.PhotoImage(file="off.png")

        # 設置各按鈕初始狀態。
        self.Light_state = False
        self.Fan_state = False
        self.Charge_state = False

        # 設置元件擺放。
        self.set_element()

        # 每1000毫秒(1秒)，更新時間設定。
        self.delay_clock = 1000
        self.update_clock()

        # 網頁控制檯燈開關。
        file.write_file('web_light_state.txt', 'OFF')
        self.web_light_last_state = False
        self.delay_light = 100
        self.update_light()

        # 溫度設置。
        self.degree = 0
        # 背景讀取溫度。
        # self.threading_read_temp()

        # 每1000毫秒(1秒)，更新溫度設定。
        # self.delay_temp = 1000
        # self.Fan_last_state = False
        # self.update_temp()

        self.Charge_last_state = False
        self.Charge_start_time = "18:40:00"
        self.Charge_end_time = "18:40:20"

        self.delay_Charge = 1000
        self.update_Charge()

        # 顯示GUI介面。
        self.window.mainloop()

    # 設置元件位置。
    def set_element(self):
        self.title_label = tk.Label(self.window, text='期末專題 - 智慧家居實作', bg="white", fg="black", font=Font(size=24), )
        self.title_label.place(x=200, y=10, width=400, height=40)

        self.Light_label = tk.Label(self.window, text='檯燈', bg="white", fg="black", font=Font(size=24))
        self.Light_label.place(x=255, y=150, width=100, height=40)

        self.Light_button = tk.Button(self.window, image=self.off, bg="white", bd=0, command=self.Light_Switch)
        self.Light_button.place(x=425, y=150, width=100, height=40)

        self.Fan_label = tk.Label(self.window, text='風扇', bg="white", fg="black", font=Font(size=24))
        self.Fan_label.place(x=255, y=220, width=100, height=40)

        self.Fan_button = tk.Button(self.window, image=self.off, bg="white", bd=0, command=self.Fan_Switch)
        self.Fan_button.place(x=425, y=220, width=100, height=40)

        self.Charge_label = tk.Label(self.window, text='充電器', bg="white", fg="black", font=Font(size=24))
        self.Charge_label.place(x=255, y=290, width=100, height=40)

        self.Charge_button = tk.Button(self.window, image=self.off, bg="white", bd=0, command=self.Charge_Switch)
        self.Charge_button.place(x=425, y=290, width=100, height=40)

    # 初始化Arduino Serial連接。
    def init_serial(self):
        self.COM_PORT = 'COM3'
        self.BAUD_RATES = 9600
        self.ser = serial.Serial(self.COM_PORT, self.BAUD_RATES)

    # 檯燈按鈕。
    def Light_Switch(self):
        if self.Light_state:
            self.Light_button.config(image=self.off)
            self.Light_state = False

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n檯燈：OFF'
            lineNotify(self.line_token, self.message)

            self.ser.write(b'off\n')
        else:
            self.Light_button.config(image=self.on)
            self.Light_state = True

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n檯燈：ON'
            lineNotify(self.line_token, self.message)

            self.ser.write(b'on\n')

    # 風扇按鈕。
    def Fan_Switch(self):
        if self.Fan_state:
            self.Fan_button.config(image=self.off)
            self.Fan_state = False

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n風扇：OFF'
            lineNotify(self.line_token, self.message)

            # self.ser.write(b'on\n')
        else:
            self.Fan_button.config(image=self.on)
            self.Fan_state = True

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n風扇：ON'
            lineNotify(self.line_token, self.message)

            # self.ser.write(b'off\n')

    # 充電器按鈕。
    def Charge_Switch(self):
        if self.Charge_state:
            self.Charge_button.config(image=self.off)
            self.Charge_state = False

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n充電器：OFF'
            lineNotify(self.line_token, self.message)

            # self.ser.write(b'on\n')
        else:
            self.Charge_button.config(image=self.on)
            self.Charge_state = True

            self.message = '\n當前時間：' + self.now_time + '\n觸發事件：按鈕\n充電器：ON'
            lineNotify(self.line_token, self.message)

            # self.ser.write(b'off\n')

    # 顯示當前時間。
    def update_clock(self):
        week_day_dict = {0: '(一)', 1: '(二)', 2: '(三)', 3: '(四)',
                         4: '(五)', 5: '(六)', 6: '(日)', }

        # 讀取當前日期
        now_date, day = strftime("%Y-%m-%d"), date.today().weekday()

        # 設置當前日期
        now_date_info = tk.Label(text=now_date + ' ' + week_day_dict[day], bg="white", fg="black", font=Font(size=24))
        now_date_info.place(x=150, y=80, width=250, height=40)

        # 讀取當前時間。
        self.now_time = strftime("%H:%M:%S")

        # 設置當前時間。
        now_time_info = tk.Label(text=self.now_time, bg="white", fg="black", font=Font(size=24))
        now_time_info.place(x=480, y=80, width=150, height=40)

        self.window.after(self.delay_clock, self.update_clock)

    # 更新網頁響應
    def update_light(self):
        if file.read_file('web_light_state.txt') == 'ON':
            # 若按鈕上個狀態為OFF，執行以下區塊。
            if not self.web_light_last_state:
                self.Light_button.config(image=self.on)
                self.Light_state = True

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：網頁\n檯燈：ON'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'on\n')

            self.web_light_last_state = True
        else:
            # 若按鈕上個狀態為ON，執行以下區塊。
            if self.web_light_last_state:
                self.Light_button.config(image=self.off)
                self.Light_state = False

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：網頁\n檯燈：OFF'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'off\n')

            self.web_light_last_state = False

        self.window.after(self.delay_light, self.update_light)

    # 顯示當前溫度。
    def update_temp(self):
        self.temp = str(self.degree).replace('\r\n', '') + '°C'
        self.temp_label = tk.Label(self.window, text=self.temp, bg="white", fg="black", font=Font(size=24))
        self.temp_label.place(x=550, y=220, width=100, height=40)

        if float(str(self.degree).replace('\r\n', '')) >= 30:
            # 若按鈕上個狀態為OFF，執行以下區塊。
            if not self.Fan_last_state:
                self.Fan_button.config(image=self.on)
                self.Fan_state = True

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：溫度\n風扇：ON'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'on\n')

            self.Fan_last_state = True
        else:
            # 若按鈕上個狀態為ON，執行以下區塊。
            if self.Fan_last_state:
                self.Fan_button.config(image=self.off)
                self.Fan_state = False

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：溫度\n風扇：OFF'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'off\n')

            self.Fan_last_state = False

        self.window.after(self.delay_temp, self.update_temp)

    # 讀取LM35感測溫度。
    def read_temp(self):
        while True:
            while self.ser.in_waiting:
                print(self.ser.readline())
                self.degree = self.ser.readline().decode()

    # 背景讀取LM35感測溫度。
    def threading_read_temp(self):
        # 將face_train添加至子執行緒中
        process = Thread(target=self.read_temp)
        # 子執行緒執行face_train
        process.start()

    # 檢測充電時間。
    def update_Charge(self):
        if self.Charge_start_time < self.now_time < self.Charge_end_time:
            # 若按鈕上個狀態為OFF，執行以下區塊。
            if not self.Charge_last_state:
                self.Charge_button.config(image=self.on)
                self.Charge_state = True

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：時間\n充電器：ON'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'on\n')

            self.Charge_last_state = True
        else:
            # 若按鈕上個狀態為ON，執行以下區塊。
            if self.Charge_last_state:
                self.Charge_button.config(image=self.off)
                self.Charge_state = False

                self.message = '\n當前時間：' + self.now_time + '\n觸發事件：時間\n充電器：OFF'
                lineNotify(self.line_token, self.message)

                self.ser.write(b'off\n')

            self.Charge_last_state = False

        self.window.after(self.delay_Charge, self.update_Charge)


if __name__ == '__main__':
    APP()
