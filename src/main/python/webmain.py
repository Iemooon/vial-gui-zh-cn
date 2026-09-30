# SPDX-License-Identifier: GPL-2.0-or-later
import os

import traceback

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

import sys
import json

from main_window import MainWindow


# http://timlehr.com/python-exception-hooks-with-qt-message-box/
from util import init_logger

window = None

def show_exception_box(log_msg):
    if QtWidgets.QApplication.instance() is not None:
        global errorbox

        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(log_msg)
        errorbox.setModal(True)
        errorbox.show()


class UncaughtHook(QtCore.QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            log_msg = '\n'.join([''.join(traceback.format_tb(exc_traceback)),
                                 '{0}: {1}'.format(exc_type.__name__, exc_value)])

            # trigger message box show
            self._exception_caught.emit(log_msg)
        sys._excepthook(exc_type, exc_value, exc_traceback)


def web_get_resource(name):
    return "/usr/local/" + name


# The web build starts in the light palette.  Upstream's default comes from
# main_window.get_theme() -> QSettings("Vial","Vial").value("theme", "Dark"),
# and a browser cannot keep that setting across a reload, so "Dark" is what
# everyone gets today.  Desktop builds are untouched; override per load with
# ?theme=dark|system|light.
DEFAULT_THEME = "Light"


def _theme_names():
    """("System", "Light", "Dark", ...) -- the same list the desktop menu shows."""
    import themes
    return [name for name, _ in [("System", None)] + themes.themes]


def apply_theme(app, name):
    """Switch the palette without the desktop build's restart warning.

    Upstream hides the whole Theme menu under Emscripten (main_window.py:221),
    but the palettes in themes.py are pure Python and apply just fine here.
    Names are matched case-insensitively so a URL can say ?theme=light.
    """
    import themes

    wanted = str(name or "").strip().lower()
    match = next((n for n in _theme_names() if n.lower() == wanted), None)
    if match is None:
        return False
    name = match
    if name == "System":
        # Theme.set_theme() deliberately does nothing for "System", which would
        # leave the previous palette painted on the screen.
        themes.Theme.theme = name
        app.setStyle("Fusion")
        app.setPalette(app.style().standardPalette())
    else:
        themes.Theme.set_theme(name)
    return True


def add_theme_menu(app, window, current=None):
    """Put the Theme menu back on the menu bar (web build only)."""
    # Qt5 keeps both of these in QtWidgets; QActionGroup only moved to QtGui in Qt6.
    from PyQt5.QtWidgets import QAction, QActionGroup

    from util import tr

    menu = window.menuBar().addMenu(tr("Menu", "Theme"))
    group = QActionGroup(window)
    wanted = str(current or window.get_theme() or "System").lower()
    for name in _theme_names():
        act = QAction(tr("MenuTheme", name), window)
        act.setCheckable(True)
        act.setChecked(name.lower() == wanted)
        act.triggered.connect(lambda checked, n=name: _choose_theme(app, window, n))
        group.addAction(act)
        menu.addAction(act)
    return menu


def _choose_theme(app, window, name):
    apply_theme(app, name)
    try:
        window.settings.setValue("theme", name)
    except Exception:
        pass


def main(app, theme=None):
    font = app.font()
    font.setPointSize(10)
    app.setFont(font)

    app.get_resource = web_get_resource
    with open(app.get_resource("build_settings.json"), "r") as inf:
        app.build_settings = json.loads(inf.read())
    qt_exception_hook = UncaughtHook()

    # Simplified-Chinese interface (see src/main/python/i18n/)
    import i18n
    i18n.install(app)

    # Not sure of the best way to do this.
    global window
    window = MainWindow(app)

    # Theme: MainWindow has already painted upstream's default (Dark, read from
    # QSettings which a browser cannot persist), so apply ours after it is
    # built and before it is shown.  ?theme= from the page wins over the
    # default; the menu is there for the current session only.
    chosen = theme or DEFAULT_THEME
    add_theme_menu(app, window, current=chosen)
    apply_theme(app, chosen)

    window.show()

    app.processEvents()
