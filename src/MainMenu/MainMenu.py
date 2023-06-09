import sys
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from BasePipe.BasePipe import BasePipe
from Monitor.Monitor import Monitor
from DevWindow.DevWindow import DevWindow
from DataWindow.DataWindow import DataWindow
from ModelWindow.ModelWindow import ModelWindow

class MainMenu(BasePipe):
    def __init__(self):
        self._window = None
        self._window_on = False
        self._last_events = None
        self._last_values = None

    def start(self):
        self._window_config()
        self._window_screen()

    def _window_config(self):
        sg.theme("DarkTeal11")
        layout = [
            [
                sg.Button("Data", size=(20, 5)),
                sg.Button("Model", size=(20, 5)),
                sg.Button("Development", size=(20, 5)),
                sg.Button("Monitor", size=(20, 5)),
            ],
        ]

        self._window_on = True
        self._window = sg.Window("Main Menu", layout, size=(720, 100))

    def _window_screen(self):
        while self._window_on:
            self._window_read()
            self._window_check_events()

        self._window.close()

    def _window_read(self):
        self._last_events, self._last_values = self._window.read()

    def _window_check_events(self):
        if self._close():
            self._window_on = False
        elif self._check_button("Data"):
            self._load_data()
        elif self._check_button("Model"):
            self._load_model()
        elif self._check_button("Development"):
            self._load_development()
        elif self._check_button("Monitor"):
            self._load_monitor()

    def _check_button(self, button):
        return self._last_events == button

    def _load_data(self):
        dw = DataWindow()
        dw.start()

    def _load_model(self):
        model_win = ModelWindow()
        model_win.start()

    def _load_development(self):
        dev_win = DevWindow()
        dev_win.start()

    def _load_monitor(self):
        mon = Monitor()
        mon.start()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED
