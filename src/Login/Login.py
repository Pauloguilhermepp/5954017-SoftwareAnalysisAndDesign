import sys
import sqlite3 as sql
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from NewUser.NewUser import NewUser
from BasePipe.BasePipe import BasePipe


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
            [sg.Button("Login"), sg.Text("", key="message")],
            [sg.Button("Add new user", size=(30, 1))],
        ]

        self._window_on = True
        self._window = sg.Window("Login Screen", layout)

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
        elif self._filter():
            self._next()
        elif self._check_new_user():
            self._add_new_user()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED

    def _filter(self):
        if self._login_attempt():
            if self._check_user_and_password():
                self._window["message"].update("Logged with success!")
                return True

            self._window["message"].update("User or password incorrect!")

        return False

    def _next(self):
        print("Logged")

    def _login_attempt(self):
        return self._last_events == "Login"

    def _check_user_and_password(self):
        con = sql.connect("./Data/main_database.db")
        cur = con.cursor()

        statement = "SELECT user_name from users WHERE user_name=? AND user_password=?;"
        query_info = self._last_values["user"], self._last_values["password"]

        try:
            cur.execute(statement, query_info)
        except sql.OperationalError:
            pass

        return cur.fetchone()

    def _check_new_user(self):
        return self._last_events == "Add new user"

    def _add_new_user(self):
        nw = NewUser()
        nw.start()
