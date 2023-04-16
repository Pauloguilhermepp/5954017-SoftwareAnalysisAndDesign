import os
import sys
from PySimpleGUI import PySimpleGUI as sg

sys.path.append("./")
from BasePipe.BasePipe import BasePipe


class DevWindow(BasePipe):
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
                sg.Text("Project Path", size=(15, 0)),
                sg.Input(key="project_path", size=(30, 0)),
                sg.Button("Load", size=(5, 0)),
            ],
            [
                sg.Text("Project Organization", size=(25, 0)),
                sg.Button("Fast Organization", size=(15, 0)),
            ],
            [sg.Text("", key="project_organization_msg")],
            [sg.Text("Test Coverage", size=(15, 0))],
            [sg.Text("", key="test_coverage_msg")],
        ]

        self._window_on = True
        self._window = sg.Window("Development Window", layout)

    def _load_project_from_attempt(self):
        return self._last_events == "Load"

    def _load_project_from_path(self):
        self._path = self._last_values["project_path"]

        sg.set_options(font=("Arial Bold", 6))
        self._evaluate_project_organization()
        self._evaluate_test_coverage()

    def _evaluate_project_organization(self):
        command = f"pylint {self._path}"
        output = os.popen(f"{command}").read()
        self._window["project_organization_msg"].update(f"{output}")

    def _evaluate_test_coverage(self):
        command = f"pytest --cov=myproj {self._path}"
        output = os.popen(f"{command}").read()
        self._window["test_coverage_msg"].update(f"{output}")

    def _fast_organization_attempt(self):
        return self._last_events == "Fast Organization"

    def _fast_organization(self):
        command = f"black {self._path}"
        os.popen(f"{command}").read()
        self._window["project_organization_msg"].update("Project Organization Updated")

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
        elif self._load_project_from_attempt():
            self._load_project_from_path()
        elif self._fast_organization_attempt():
            self._fast_organization()

    def _close(self):
        return self._last_events == sg.WINDOW_CLOSED
