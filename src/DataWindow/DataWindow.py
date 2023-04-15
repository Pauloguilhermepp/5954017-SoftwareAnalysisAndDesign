import sys
import pandas as pd
import sqlite3 as sql
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from BasePipe.BasePipe import BasePipe

class DataWindow(BasePipe):
    def __init__(self):
        self._window = None
        self._window_on = False
        self._new_window = True
        self._last_events = None
        self._last_values = None
        self._con = sql.connect("./Data/main_database.db")
        self._load_data()

    def start(self):
        while self._new_window:
            self._load_data()
            self._window_config()
            self._window_screen()
        self._con.close()

    def _window_config(self):
        sg.theme("DarkTeal11")
        sg.set_options(font=("Arial Bold", 12))

        table = self._load_table()
        layout = [
            [sg.Text("New File", size=(8, 0)),
             sg.Input(key="new_file", size=(20, 0)),
             sg.Button("Add", size=(3, 0))], [table]
        ]

        self._window_on = True
        self._window = sg.Window("Data Window", layout)

    def _load_data(self):
        if  hasattr(self, "_df"):
            return
    
        try:
            self._df = pd.read_sql_query("SELECT * from data", self._con)
        except pd.io.sql.DatabaseError:
            self._df = pd.DataFrame([])
    
    def _load_file_from_attempt(self):
        return self._last_events == "Add"

    def _load_file_from_path(self):
        path = self._last_values["new_file"]
        self._df = pd.read_csv(path)
        self._window_on = False

    def _load_table(self):
        headings = list(self._df.head())
        values = self._df.values.tolist()

        table = sg.Table(values=values, headings=headings,
        auto_size_columns=True,
        display_row_numbers=False,
        justification='center', key='-TABLE-',
        selected_row_colors='red on yellow',
        enable_events=True,
        expand_x=True,
        expand_y=True,
        enable_click_events=True)

        return table

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
            self._new_window = False
        elif self._load_file_from_attempt():
            self._load_file_from_path()
        elif '+CLICKED+' in self._last_events:
            sg.popup("You clicked row:{} Column: {}".format(self._last_events[2][0], self._last_events[2][1]))

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED
