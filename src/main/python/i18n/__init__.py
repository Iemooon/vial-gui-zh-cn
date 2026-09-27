# SPDX-License-Identifier: GPL-2.0-or-later
"""Simplified-Chinese localisation for Vial GUI -- an additive layer.

Why it is built this way
------------------------
Upstream already routes most user-visible text through ``util.tr``, which is a
plain alias of ``QCoreApplication.translate`` (src/main/python/util.py:17).
Installing one QTranslator therefore reaches every one of those call sites --
including the strings that only exist at runtime (tab labels, keymap names,
theme names, editor names), which no amount of static source rewriting could
cover.

A small number of strings are hardcoded straight into widget calls instead of
being wrapped in ``tr()``.  Those are picked up by the hooks installed below.

No upstream source is rewritten, so ``git merge upstream/main`` stays clean.
Removing this translation means deleting this directory and the two
``i18n.install()`` calls in main.py / webmain.py.

Strings that still need translating
-----------------------------------
Start the GUI with ``VIAL_ZH_COLLECT=<path>`` set; every string Qt asks about
and every string the hooks see is appended to that file, one JSON object per
line, with ``"translated": false`` when the table has no entry for it yet.
"""
import io
import json
import os
import re

from PyQt5.QtCore import QCoreApplication, QTranslator

from . import zh_cn

# (compiled regex, replacement) for strings upstream assembles with str.format()
_PATTERNS = [(re.compile(pattern), repl) for pattern, repl in zh_cn.PATTERNS]

# Context used for strings that upstream hardcodes instead of wrapping in tr().
HOOK_CONTEXT = "*"

_COLLECT_PATH = os.environ.get("VIAL_ZH_COLLECT")
_seen = set()
_translator = None
_hooks_installed = False
_any_context = None


def _any_context_table():
    """English -> Chinese across *every* context, for strings that reach us with
    no context of their own.

    Strings hardcoded into widget calls arrive as HOOK_CONTEXT ("*"), but their
    entry may well live in a section named after the screen that owns it: the
    RGB effect names sit in "RGBConfigurator", the QMK setting titles in
    "QmkSettings".  Only strings that read the same in every context are offered
    here, so this can never pick the wrong reading for a screen-specific word.
    """
    global _any_context
    if _any_context is None:
        seen = {}
        for ctx, section in zh_cn.TABLE.items():
            if ctx == HOOK_CONTEXT:
                continue
            for en, cn in section.items():
                if en in seen and seen[en] != cn:
                    seen[en] = None          # ambiguous: only its own context may use it
                else:
                    seen.setdefault(en, cn)
        _any_context = {en: cn for en, cn in seen.items() if cn}
    return _any_context


def _caller():
    """file:line of the first frame outside this package -- collect mode only."""
    import sys
    try:
        here = os.path.dirname(os.path.abspath(__file__))
        frame = sys._getframe(2)
        while frame is not None:
            if os.path.dirname(os.path.abspath(frame.f_code.co_filename)) != here:
                return "%s:%d" % (os.path.basename(frame.f_code.co_filename), frame.f_lineno)
            frame = frame.f_back
    except Exception:
        pass
    return ""


def _collect(context, source, translated, via, caller=""):
    if not _COLLECT_PATH:
        return
    key = (via, context, source)
    if key in _seen:
        return
    _seen.add(key)
    try:
        with io.open(_COLLECT_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"context": context, "source": source,
                                "translated": bool(translated), "via": via,
                                "caller": caller},
                               ensure_ascii=False) + "\n")
    except Exception:
        pass


def _lookup(context, source):
    """Return the Chinese text, or None when nothing is known about it."""
    section = zh_cn.TABLE.get(context or "")
    if section:
        hit = section.get(source)
        if hit is not None:
            return hit
    if context != HOOK_CONTEXT:
        hit = zh_cn.TABLE.get(HOOK_CONTEXT, {}).get(source)
        if hit is not None:
            return hit
    else:
        hit = _any_context_table().get(source)
        if hit is not None:
            return hit
    # Strings that upstream builds with str.format() (e.g. one entry per Tap
    # Dance slot) are matched as patterns instead of being enumerated in the
    # table; \1 style backreferences work as usual.
    for rx, template in _PATTERNS:
        if rx.match(source):
            return rx.sub(template, source)
    return None


class ZhTranslator(QTranslator):
    """Feeds the zh-CN table into *every* QCoreApplication.translate() call."""

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        if not sourceText:
            return None
        hit = _lookup(context or "", sourceText)
        _collect(context or "", sourceText, hit is not None, "qt")
        # Returning None is what tells Qt "no translation here" -- it then keeps
        # looking and finally falls back to the source string.  Returning "" does
        # NOT mean that: PyQt hands Qt an *empty but non-null* QString, which
        # counts as a hit and stops the search, so every string missing from the
        # table would come back blank instead of English (that is exactly how the
        # editor tab labels went empty on 2026-09-27).
        return hit


def _tr(text):
    if not isinstance(text, str) or not text:
        return text
    if _COLLECT_PATH:
        # collect mode deliberately leaves behaviour untouched: the hooks only
        # report what they see, the table gets filled in afterwards
        _collect(HOOK_CONTEXT, text, _lookup(HOOK_CONTEXT, text) is not None,
                 "widget", _caller())
        return text
    return QCoreApplication.translate(HOOK_CONTEXT, text)


def _wrap_setter(cls, name, index=0):
    """Translate the positional string argument of ``cls.name``."""
    orig = getattr(cls, name)

    def wrapped(self, *args, **kwargs):
        if len(args) > index and isinstance(args[index], str):
            args = list(args)
            args[index] = _tr(args[index])
        return orig(self, *args, **kwargs)

    setattr(cls, name, wrapped)


def _wrap_init(cls, index=0):
    orig = cls.__init__

    def wrapped(self, *args, **kwargs):
        if len(args) > index and isinstance(args[index], str):
            args = list(args)
            args[index] = _tr(args[index])
        return orig(self, *args, **kwargs)

    setattr(cls, "__init__", wrapped)


def _patch_tabbed_keycodes():
    """Keep the selected keycode tab across rebuilds.

    FilteredTabbedKeycodes.recreate_keycode_buttons() remembers the current tab
    by comparing the *displayed* title against the untranslated ``tab.label``:

        prev_tab = self.tabText(self.currentIndex())
        ...
        if tab.label == prev_tab: self.setCurrentIndex(...)

    Once titles are translated that comparison can never be true again, so every
    rebuild (changing the keycode filter, opening the tray) jumps back to the
    first tab.  The wrapper restores the same intent using widget identity, which
    is translation-proof, and leaves upstream untouched.
    """
    from tabbed_keycodes import FilteredTabbedKeycodes

    if getattr(FilteredTabbedKeycodes, "_i18n_wrapped", False):
        return
    orig = FilteredTabbedKeycodes.recreate_keycode_buttons

    def recreate_keycode_buttons(self):
        index = self.currentIndex()
        current = self.widget(index) if index >= 0 else None
        orig(self)
        if current is None:
            return
        for i in range(self.count()):
            if self.widget(i) is current:
                self.setCurrentIndex(i)
                return

    recreate_keycode_buttons._i18n_original = orig
    FilteredTabbedKeycodes.recreate_keycode_buttons = recreate_keycode_buttons
    FilteredTabbedKeycodes._i18n_wrapped = True


def _patch_qmk_settings_tabs():
    """Translate the QMK settings sub-tab names, and only those.

    That screen builds its rows in Python as ``QLabel(option["title"])`` and
    ``QPushButton(tr("QmkSettings", "Save"))``, so the *field titles* never pass
    through ``util.tr`` and no widget hook sees them -- which is just as well,
    because those stay English by request.  The sub-tab names come from the very
    same JSON, though, and are added through ``QTabWidget.addTab``, which *is*
    hooked; without this filter the global hook would happily translate the
    labels next to them as well.

    So the tab names get translated at the source, with the table still holding
    them under the "QmkSettings" context.  Upstream file untouched.
    """
    from editor.qmk_settings import QmkSettings

    if getattr(QmkSettings, "_i18n_wrapped", False):
        return
    orig = QmkSettings.populate_tab

    def populate_tab(self, tab, container):
        options = orig(self, tab, container)
        index = self.tabs_widget.indexOf(container.parentWidget())
        name = _lookup("QmkSettings", tab["name"])
        if index >= 0 and name and self.tabs_widget.tabText(index) == tab["name"]:
            self.tabs_widget.setTabText(index, name)
        return options

    populate_tab._i18n_original = orig
    QmkSettings.populate_tab = populate_tab
    QmkSettings._i18n_wrapped = True


def _patch_qmk_settings_fields():
    """Translate the QMK settings *field titles*.

    They live in resources/base/qmk_settings.json and are shown as bare
    ``QLabel(option["title"])`` -- no ``util.tr()`` call anywhere on that path,
    so neither the translator nor the widget hooks can reach them.  The only
    place they can be caught is the JSON itself, read once at startup by
    ``QmkSettings.initialize()``; this wrapper translates each title as it is
    loaded, which also keeps the qsid tables keyed by the same strings.

    The setting *values* are untouched: spinboxes and checkboxes read the
    numeric part, and the free-text values under an integer field are numbers.

    Wrapping the classmethod means upstream file stays untouched.
    """
    from editor.qmk_settings import QmkSettings

    if getattr(QmkSettings, "_i18n_fields_wrapped", False):
        return
    orig = QmkSettings.initialize.__func__

    def initialize(cls, appctx):
        orig(cls, appctx)
        hits = 0
        for tab in cls.settings_defs.get("tabs", []):
            name = _lookup("QmkSettings", tab.get("name", ""))
            if name:
                tab["name"] = name
            for field in tab.get("fields", []):
                title = field.get("title")
                if not title:
                    continue
                zh = _lookup("QmkSettings", title)
                if zh:
                    field["title"] = zh
                    hits += 1
        _collect("QmkSettings", "<fields>", bool(hits), "json")

    initialize._i18n_original = orig
    QmkSettings.initialize = classmethod(initialize)
    QmkSettings._i18n_fields_wrapped = True


def _localize_standard_buttons(box):
    for btn in box.buttons():
        text = btn.text()
        if text:
            btn.setText(_tr(text))


def _install_hooks():
    from PyQt5.QtWidgets import (QAbstractButton, QAction, QComboBox, QDialogButtonBox,
                                 QGroupBox, QLabel, QLineEdit, QListWidgetItem, QMenu,
                                 QMessageBox, QStatusBar, QTabWidget, QTableWidgetItem,
                                 QTreeWidgetItem, QWidget)

    # --- plain widgets -------------------------------------------------
    _wrap_init(QLabel)
    _wrap_setter(QLabel, "setText")
    _wrap_init(QAbstractButton)          # QPushButton/QCheckBox/QRadioButton/QToolButton
    _wrap_setter(QAbstractButton, "setText")
    _wrap_init(QGroupBox)
    _wrap_setter(QGroupBox, "setTitle")
    _wrap_setter(QWidget, "setWindowTitle")
    _wrap_setter(QWidget, "setToolTip")
    _wrap_setter(QWidget, "setWhatsThis")
    _wrap_setter(QLineEdit, "setPlaceholderText")
    _wrap_setter(QStatusBar, "showMessage")

    # --- menus / actions -----------------------------------------------
    _wrap_init(QAction)
    _wrap_setter(QAction, "setText")
    _wrap_init(QMenu)
    _wrap_setter(QMenu, "setTitle")
    _wrap_setter(QWidget, "addAction")   # QWidget.addAction(QAction) and addAction(str)
    _wrap_setter(QMenu, "addAction")

    # --- containers ----------------------------------------------------
    _wrap_setter(QTabWidget, "addTab", 1)
    _wrap_setter(QTabWidget, "insertTab", 2)
    _wrap_setter(QTabWidget, "setTabText", 1)
    _wrap_setter(QComboBox, "addItem", 0)
    _wrap_setter(QComboBox, "insertItem", 1)
    _wrap_setter(QComboBox, "setItemText", 1)

    # --- item widgets ---------------------------------------------------
    _wrap_init(QListWidgetItem)
    _wrap_setter(QListWidgetItem, "setText")
    _wrap_init(QTableWidgetItem)
    _wrap_setter(QTableWidgetItem, "setText")
    _wrap_init(QTreeWidgetItem)
    _wrap_setter(QTreeWidgetItem, "setText", 1)

    # --- dialogs --------------------------------------------------------
    _wrap_setter(QMessageBox, "setText")
    _wrap_setter(QMessageBox, "setInformativeText")
    _wrap_setter(QMessageBox, "setDetailedText")
    for name in ("about", "information", "warning", "critical", "question"):
        orig = getattr(QMessageBox, name)

        def make(orig=orig):
            def f(parent, title, text, *a, **k):
                return orig(parent, _tr(title), _tr(text), *a, **k)
            return f

        setattr(QMessageBox, name, staticmethod(make()))

    orig_dbb_init = QDialogButtonBox.__init__

    def dbb_init(self, *a, **k):
        orig_dbb_init(self, *a, **k)
        _localize_standard_buttons(self)

    QDialogButtonBox.__init__ = dbb_init
    orig_dbb_set = QDialogButtonBox.setStandardButtons

    def dbb_set(self, *a, **k):
        orig_dbb_set(self, *a, **k)
        _localize_standard_buttons(self)

    QDialogButtonBox.setStandardButtons = dbb_set

    # not a hook: repairs a piece of logic that reading translated text broke
    try:
        _patch_tabbed_keycodes()
    except Exception:
        pass
    try:
        _patch_qmk_settings_tabs()
    except Exception:
        pass
    try:
        _patch_qmk_settings_fields()
    except Exception:
        pass


def install(app=None):
    """Install the translator and the widget hooks. Idempotent."""
    global _translator, _hooks_installed
    if app is None:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
    if app is None:
        raise RuntimeError("i18n.install() must run after QApplication exists")
    if _translator is None:
        # keep a reference: Qt does not own the object and Python would GC it
        _translator = ZhTranslator()
        app.installTranslator(_translator)
    if not _hooks_installed:
        _install_hooks()
        _hooks_installed = True
    return _translator
