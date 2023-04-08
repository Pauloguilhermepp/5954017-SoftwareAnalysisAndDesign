import sys
import time
import sqlite3 as sql

sys.path.append("./")
from BasePipe.BasePipe import BasePipe
from PySimpleGUI import PySimpleGUI as sg


class NewUser(BasePipe):
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
            [sg.Text("Name", size=(10, 0)), sg.Input(key="name", size=(20, 0))],
            [sg.Text("Password", size=(10, 0)), sg.Input(key="password", size=(20, 0))],
            [sg.Button("Create"), sg.Text("", key="message")]
        ]

        self._window_on = True
        self._window = sg.Window("New User Screen", layout)

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
            self._add_new_user()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED

    def _filter(self):
        if self._create_new_user_attempt():
            if self._check_user_name():
                self._window["message"].update("New user created!")
                return True

            self._window["message"].update("Error while creating new user!")

        return False

    def _create_new_user_attempt(self):
        return self._last_events == "Create"

    def _check_user_name(self):
        con = sql.connect("./Data/main_database.db")
        cur = con.cursor()

        statement = "SELECT user_name from users WHERE user_name=?;"
        query_info = (self._last_values["name"],)
        
        try:
            cur.execute(statement, query_info)
        except sql.OperationalError:
            pass

        return not cur.fetchone()
    
    def _add_new_user(self):
        conn = sql.connect("./Data/main_database.db") 
        cur = conn.cursor()

        statement = """
                    CREATE TABLE IF NOT EXISTS users
                    ([user_name] TEXT PRIMARY KEY, [user_password] TEXT)
                    """
        try:
            cur.execute(statement)
        except sql.OperationalError:
            pass

        statement = """
                    INSERT INTO users (user_name, user_password) 
                    VALUES
                    (?, ?)
                    """
        query_info = self._last_values["name"], self._last_values["password"]
        
        try:
            cur.execute(statement, query_info)
        except sql.OperationalError:
            pass
                            
        conn.commit()
