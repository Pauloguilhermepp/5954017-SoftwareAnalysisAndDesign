import sys
import pickle
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from BasePipe.BasePipe import BasePipe


class ModelWindow(BasePipe):
    def __init__(self):
        self._model = None
        self._window = None
        self._window_on = False
        self._new_window = True
        self._last_events = None
        self._last_values = None
        self._last_chosen_columns = []
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
            [
                sg.Text("New Data File", size=(15, 0)),
                sg.Input(key="new__data_file", size=(20, 0)),
                sg.Button("Add", size=(12, 0)),
                sg.Button("Load", size=(12, 0))
            ],
            [
                sg.Text("New Model File", size=(15, 0)),
                sg.Input(key="new__model_file", size=(20, 0)),
                sg.Button("Add", size=(12, 0)),
                sg.Button("Load", size=(12, 0))
            ],
            [sg.Button("Create Graph", size=(18, 0)), sg.Button("Evaluate Model", size=(18, 0))],
            [table],
        ]

        self._window_on = True
        self._window = sg.Window("Model Window", layout)

    def _load_data(self):
        if hasattr(self, "_df"):
            return

        try:
            self._df = pd.read_sql_query("SELECT * from data", self._con)
        except pd.io.sql.DatabaseError:
            self._df = pd.DataFrame([])
    
    def _load_model(self, model_path):
        self._model = pickle.load(open(model_path, 'rb'))

    def _load_file_from_attempt(self):
        return self._last_events == "Load"

    def _load_file_from_path(self):
        path = self._last_values["new_file"]
        self._df = pd.read_csv(path)

        self._window_on = False
        self._last_chosen_columns = []

    def _add_file_attempt(self):
        return self._last_events == "Add"

    def _add_file_from_path(self):
        self._load_file_from_path()
        self._save_file()

    def _create_graph_attempt(self):
        return self._last_events == "Create Graph"

    def _create_graph(self):
        header = list(self._df.head())
        column1_name = header[self._last_chosen_columns[-1]]
        column2_name = header[self._last_chosen_columns[-2]]

        column1 = self._df[column1_name]
        column2 = self._df[column2_name]

        plt.scatter(column1, column2)
        plt.xlabel(column1_name)
        plt.ylabel(column2_name)
        plt.title(f"Graph of {column2_name} per {column1_name}")
        plt.grid()
        plt.show()

    def _save_file(self):
        self._df.to_sql(name="data", con=self._con)

    def _load_table(self):
        headings = list(self._df.head())
        values = self._df.values.tolist()

        table = sg.Table(
            values=values,
            headings=headings,
            auto_size_columns=True,
            display_row_numbers=False,
            justification="center",
            key="-TABLE-",
            selected_row_colors="red on yellow",
            enable_events=True,
            expand_x=True,
            expand_y=True,
            enable_click_events=True,
        )

        return table

    def _window_screen(self):
        while self._window_on:
            self._window_read()
            self._window_check_events()

        self._window.close()

    def _window_read(self):
        self._last_events, self._last_values = self._window.read()

    def _check_for_update_columns(self):
        return "+CLICKED+" in self._last_events

    def _update_columns(self):
        self._last_chosen_columns.append(self._last_events[2][1])

    def _window_check_events(self):
        if self._close():
            self._window_on = False
            self._new_window = False
        elif self._load_file_from_attempt():
            self._load_file_from_path()
        elif self._add_file_attempt():
            self._add_file_from_path()
        elif self._create_graph_attempt():
            self._create_graph()
        elif self._check_for_update_columns():
            self._update_columns()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED
