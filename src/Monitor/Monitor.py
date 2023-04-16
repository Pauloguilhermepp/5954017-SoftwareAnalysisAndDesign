import sys
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from BasePipe.BasePipe import BasePipe

class Monitor(BasePipe):
    def __init__(self):
        self._window = None
        self._window_on = False
        self._last_events = None
        self._last_values = None
        self._path = None

    def start(self):
        self._window_config()
        self._window_screen()

    def _window_config(self):
        sg.theme("DarkTeal11")

        layout = [
            [
                sg.Text("Email address", size=(25, 0)),
                sg.Input(key="email_address", size=(30, 0))
            ],
            [
                sg.Text("Model Path", size=(25, 0)),
                sg.Input(key="model_path", size=(30, 0))
            ],
            [
                sg.Text("Url address", size=(25, 0)),
                sg.Input(key="url_address", size=(30, 0))
            ],
            [
                sg.Text("Timer (hours)", size=(25, 0)),
                sg.Input(key="timer", size=(10, 0)),
                sg.Button("Create Monitor", size=(15, 0))
            ]
        ]

        self._window_on = True
        self._window = sg.Window("Monitor Window", layout)

    def _create_monitor_attempt(self):
        return self._last_events == "Create Monitor"

    def _create_monitor(self):
        pass

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
        elif self._create_monitor_attempt():
            self._create_monitor()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED
