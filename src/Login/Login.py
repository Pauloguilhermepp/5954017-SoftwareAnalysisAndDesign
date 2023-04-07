import sys

sys.path.append("./")
from BasePipe.BasePipe import BasePipe
from PySimpleGUI import PySimpleGUI as sg


class Login(BasePipe):
    def __init__(self):
        self._window = None
        self._window_on = False
        self._last_events = None
        self._last_values = None

    def start(self):
        self._window_config()
        self._window_screen()

    def _window_config(self):
        sg.theme("DarkAmber")
        layout = [
            [sg.Text("User", size=(10, 0)), sg.Input(key="user", size=(20, 0))],
            [sg.Text("Password", size=(10, 0)), sg.Input(key="password", size=(20, 0))],
            [sg.Button("Login")],
        ]

        self._window_on = True
        self._window = sg.Window("Login Screen", layout)

    def _window_screen(self):
        while self._window_on:
            self._window_read()
            self._window_check_events()

    def _window_read(self):
        self._last_events, self._last_values = self._window.read()

    def _window_check_events(self):
        if self._close():
            self._window_on = False
        elif self._login_attempt():
            if self._check_user_and_password():
                print("Logged")

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED

    def _login_attempt(self):
        return self._last_events == "Login"

    def _check_user_and_password(self):
        return (
            self._last_values["user"] == "name"
            and self._last_values["password"] == "123"
        )
