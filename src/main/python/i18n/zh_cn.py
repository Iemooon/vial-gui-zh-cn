# SPDX-License-Identifier: GPL-2.0-or-later
"""English -> Simplified Chinese strings for the Vial GUI.

TABLE[context][source] = translation
  * context is the one upstream passes to util.tr() -- "Menu", "MenuFile",
    "MainWindow", "RGBConfigurator" ... -- so the same English word can read
    differently on different screens.
  * the "*" section holds strings that upstream hardcodes into widget calls and
    that therefore have no context of their own.  It is also consulted as a
    fallback for every other context, so a word only needs translating once
    unless it genuinely reads differently per screen.

PATTERNS handle strings upstream builds with str.format(): one rule covers all
128 Tap Dance slots instead of 128 table entries.

Deliberately NOT translated (kept in English on purpose):
  * key names and key descriptions shown by the key picker ("KC_A", "Esc",
    "QK_BOOT: Put the keyboard into bootloader mode ...") -- technical tokens,
    and the 400-odd descriptions are part of the QMK vocabulary;
  * keyboard layout names ("Dvorak", "French (AZERTY)") and theme names
    ("Dracula", "Nord", "Catppuccin Mocha") -- proper nouns;
  * modifier key names shown by Qt for shortcuts ("Ctrl", "Shift", "Alt").
"""

TABLE = {
    # ------------------------------------------------------- generic words --
    # consulted for every context; keep the most common reading of a word here
    "*": {
        "Save": "保存",
        "Revert": "还原",
        "Reset": "重置",
        "OK": "确定",
        "Cancel": "取消",
        "Apply": "应用",
        "Enable": "启用",
        "Unlock": "解锁",
        "Lock": "锁定",
        "Refresh": "刷新",
        "Enable all": "全部启用",
        "Disable all": "全部禁用",
        # NOTE: "Copy" / "Paste" / "Undo" are deliberately absent here.
        # They are also key names (KC_COPY, KC_PSTE, KC_UNDO) shown on the key
        # picker's Media/Special tabs, where they must stay English; the places
        # that want them translated (TextboxWindow, QmkSettings) carry their own
        # context entry below.

        # --- key override / alt repeat key / combos form labels ------------
        # kept at two characters where the concept allows it, and always as a
        # noun phrase rather than a description: these sit in a narrow grid
        # column next to a key field.
        "Last key": "触发键",
        "Alt key": "替代键",
        "Allowed mods": "允许修饰",
        "Enable on layers": "生效层",
        "Trigger": "触发键",
        "Trigger mods": "触发修饰",
        "Negative mods": "取消修饰",
        "Suppressed mods": "屏蔽修饰",
        "Replacement": "替换键",
        "Options": "高级选项",
        "Output key": "输出键",
        "Key 1": "键 1",
        "Key 2": "键 2",
        "Key 3": "键 3",
        "Key 4": "键 4",

        # --- key override option tooltips ----------------------------------
        "Activate when the trigger key is pressed down":
            "按下触发键时激活",
        "Activate when a necessary modifier is pressed down":
            "按下所需修饰键时激活",
        "Activate when a negative modifier is released":
            "松开取消修饰键时激活",
        "Activate on one modifier":
            "按下任一修饰键时激活",
        "Don't deactivate when another key is pressed down":
            "按下其他键时不取消激活",
        "Don't register the trigger key again after the override is deactivated":
            "覆盖失效后不重新注册触发键",
        "Default to this alt key":
            "默认使用此替代键",
        "Bidirectional":
            "双向",
        "Ignore mod handedness":
            "忽略修饰键的左右区分",

        # --- tap dance (the labels, not the TD() template) -----------------
        "On tap": "短按",
        "On hold": "按住",
        "On double tap": "双击",
        "On tap + hold": "短按并按住",
        "Tapping term (ms)": "判定时间（毫秒）",
    },

    # ---------------------------------------------------------------- menus --
    "Menu": {
        "File": "文件",
        "Keyboard layout": "键盘布局",
        "Security": "安全",
        "Theme": "主题",
        "About": "关于",
    },
    "MenuFile": {
        "Load saved layout...": "加载已保存的布局...",
        "Save current layout...": "保存当前布局...",
        "Sideload VIA JSON...": "手动加载 VIA JSON...",
        "Download VIA definitions": "下载 VIA 定义",
        "Load dummy JSON...": "加载示例 JSON...",
        "Exit": "退出",
    },
    "MenuSecurity": {
        "Unlock": "解锁",
        "Lock": "锁定",
        "Reboot to bootloader": "重启进入引导程序",
    },
    "MenuAbout": {
        "About Vial...": "关于 Vial...",
    },
    "MenuTheme": {
        # theme names that are words rather than proper nouns
        "System": "跟随系统",
        "Light": "浅色",
        "Dark": "深色",
    },

    # ----------------------------------------------------------- main window --
    "MainWindow": {
        "Refresh": "刷新",
        'No devices detected. Connect a Vial-compatible device and press "Refresh"<br>'
        'or select "File" → "Download VIA definitions" in order to enable support for VIA keyboards.':
            '未检测到设备。请连接支持 Vial 的设备后按“刷新”，<br>'
            '或选择“文件”→“下载 VIA 定义”，以支持 VIA 键盘。',
        "In order to fully apply the theme you should restart the application.":
            "要完全应用主题，需重启应用。",
        # editor tab labels
        "Keymap": "键位",
        "Layout": "布局",
        "Macros": "宏",
        "Lighting": "灯光",
        "Tap Dance": "一键多用",
        "Combos": "并击",
        "Key Overrides": "按键覆盖",
        "Alt Repeat Key": "替代重复键",
        "QMK Settings": "固件设置",
        "Matrix tester": "矩阵测试",
        "Firmware updater": "固件更新",
    },
    "KeymapEditor": {
        "Layer": "层",
        "Saved keymap belongs to a different keyboard, are you sure you want to continue?":
            "保存的键位属于其他键盘，确定要继续吗？",
    },

    # -------------------------------------------------------------- editors --
    "MacroRecorder": {
        "Stop recording": "停止录制",
        "Save": "保存",
        "Revert": "还原",
        "Append to current": "追加到当前",
        "Replace everything": "替换全部",
        "Record macro": "录制宏",
        "Add action": "添加动作",
        "Tap Enter": "敲击回车",
        "Open Text Editor...": "打开文本编辑器...",
    },
    "TapDance": {},
    "KeyOverride": {
        "Enable all": "全部启用",
        "Disable all": "全部禁用",
    },
    "QmkSettings": {
        "Save": "保存",
        "Undo": "撤销",
        "Reset": "重置",
        "Reset all settings to default values?": "将所有设置重置为默认值？",

        # --- sub-tab names -------------------------------------------------
        # The sub-tab names, and the field titles underneath them, both come from
        # resources/base/qmk_settings.json.  The titles are read at startup by
        # _patch_qmk_settings_fields() in i18n/__init__.py, which walks the JSON
        # and translates each title in place -- upstream builds every row as a
        # bare QLabel(option["title"]) and never calls util.tr() on it.
        "Magic": "魔术键",
        "Grave Escape": "反引号转义",
        "Tap-Hold": "短按/按住",
        "Auto Shift": "自动 Shift",
        "Combo": "并击",
        "One Shot Keys": "按键超时",
        "Mouse keys": "鼠标键",

        # --- Magic ---------------------------------------------------------
        "Swap Caps Lock and Left Control": "交换 Caps 与左 Ctrl",
        "Treat Caps Lock as Control": "Caps 当 Ctrl",
        "Swap Left Alt and GUI": "交换左 Alt 与 GUI",
        "Swap Right Alt and GUI": "交换右 Alt 与 GUI",
        "Disable the GUI keys": "禁用 GUI 键",
        "Swap ` and Escape": "交换 ` 与 Esc",
        "Swap \\ and Backspace": "交换 \\ 与退格",
        "Enable N-key rollover": "启用全键无冲",
        "Swap Left Control and GUI": "交换左 Ctrl 与 GUI",
        "Swap Right Control and GUI": "交换右 Ctrl 与 GUI",

        # --- Grave Escape --------------------------------------------------
        "Always send Escape if Alt is pressed": "按 Alt 时发送 Esc",
        "Always send Escape if Control is pressed": "按 Ctrl 时发送 Esc",
        "Always send Escape if GUI is pressed": "按 GUI 时发送 Esc",
        "Always send Escape if Shift is pressed": "按 Shift 时发送 Esc",

        # --- Tap-Hold ------------------------------------------------------
        "Tapping Term": "判定时间",
        # Permissive Hold and Hold On Other Key Press are easy to mix up, so the
        # distinction is carried by the wording: the first one only skips the
        # tapping term (the other key must be pressed *and released* while the
        # mod-tap is held), the second one fires as soon as another key goes
        # down.  "提前" vs "即" is what keeps them from reading as synonyms --
        # do not fold either back into a vaguer phrase like "宽容按住".
        "Permissive Hold": "提前判定按住",
        "Ignore Mod Tap Interrupt": "忽略修饰键打断",
        "Tapping Force Hold": "强制按住",
        "Retro Tapping": "补发短按",
        "Hold On Other Key Press": "其他键按下即按住",
        "Quick Tap Term": "快速判定时间",
        "Tap Code Delay": "键码延迟",
        "Tap Hold Caps Delay": "大写延迟",
        "Tapping Toggle": "短按切层",
        # Chordal Hold is not about pressing several keys together: it tightens
        # same-hand dual-function keys, which only fire their hold action after
        # the full tapping term has elapsed and another key is tapped.  "同手"
        # names the scope, "判定" ties it back to the tapping term -- the word
        # "和弦" comes from the chorded-timing implementation and reads as
        # "press these simultaneously", which is the opposite of the point.
        "Chordal Hold": "同手判定",
        # Flow Tap: a mod-tap/layer-tap pressed within a short window after the
        # previous key reports its tap action immediately and never enters the
        # hold path.  "跟随" keeps it on the same footing as its neighbours,
        # which all state the condition under which a tap or hold is decided;
        # "流式" (from "flow of taps") read as an input-method candidate list
        # and said nothing about the trigger.
        "Flow Tap": "短按跟随",

        # --- Auto Shift ----------------------------------------------------
        "Enable for modifiers": "修饰键也启用",
        "Timeout": "超时时间",
        "Do not Auto Shift special keys": "特殊键不自动 Shift",
        "Do not Auto Shift numeric keys": "数字键不自动 Shift",
        "Do not Auto Shift alpha characters": "字母不自动 Shift",
        "Enable keyrepeat": "启用按键重复",
        "Disable keyrepeat when timeout is exceeded": "超时后停止重复",

        # --- Combo ---------------------------------------------------------
        "Time out period for combos": "并击超时时间",

        # --- One Shot Keys -------------------------------------------------
        "Tapping this number of times holds the key until tapped once again":
            "连按此次数后转为按住，直到再次短按",
        "Time (in ms) before the one shot key is released":
            "按键自动释放前的等待时间（毫秒）",

        # --- Mouse keys ----------------------------------------------------
        "Delay between pressing a movement key and cursor movement":
            "按下到光标开始移动的延迟",
        "Time between cursor movements in milliseconds": "光标移动间隔（毫秒）",
        "Step size": "步长",
        "Maximum cursor speed at which acceleration stops": "加速上限速度",
        "Time until maximum cursor speed is reached": "达到上限速度所需时间",
        "Delay between pressing a wheel key and wheel movement":
            "按下到滚轮开始移动的延迟",
        "Time between wheel movements": "滚轮移动间隔（毫秒）",
        "Maximum number of scroll steps per scroll action": "单次滚动最大步数",
        "Time until maximum scroll speed is reached": "达到上限滚动速度所需时间",
    },

    "MatrixTest": {
        "Unlock the keyboard before testing:": "测试前请先解锁键盘：",
        "Unlock": "解锁",
        "Reset": "重置",
    },
    "Flasher": {
        "Select file...": "选择文件...",
        "Flash": "刷写",
        "Restore current layout after flashing": "刷写后恢复当前布局",
    },
    "Unlocker": {
        "In order to proceed, the keyboard must be set into unlocked mode.\n"
        "You should only perform this operation on computers that you trust.":
            "要继续操作，键盘必须进入解锁模式。\n请仅在您信任的电脑上执行此操作。",
        "To exit this mode, you will need to replug the keyboard\n"
        "or select Security->Lock from the menu.":
            "要退出此模式，需要重新插拔键盘，\n或在菜单中选择“安全”→“锁定”。",
        "Press and hold the following keys until the progress bar below fills up:":
            "按住以下按键，直到下方进度条填满：",
    },
    "RGBConfigurator": {
        "Underglow Effect": "底光效果",
        "Underglow Brightness": "底光亮度",
        "Underglow Color": "底光颜色",
        "Backlight Brightness": "背光亮度",
        "Backlight Breathing": "背光呼吸",
        "RGB Effect": "RGB 效果",
        "RGB Color": "RGB 颜色",
        "RGB Brightness": "RGB 亮度",
        "RGB Speed": "RGB 速度",
        "Save": "保存",
        # light effect names
        "All Off": "全部关闭",
        "Solid Color": "纯色",
        "Breathing 1": "呼吸 1",
        "Breathing 2": "呼吸 2",
        "Breathing 3": "呼吸 3",
        "Breathing 4": "呼吸 4",
        "Rainbow Mood 1": "彩虹律动 1",
        "Rainbow Mood 2": "彩虹律动 2",
        "Rainbow Mood 3": "彩虹律动 3",
        "Rainbow Swirl 1": "彩虹漩涡 1",
        "Rainbow Swirl 2": "彩虹漩涡 2",
        "Rainbow Swirl 3": "彩虹漩涡 3",
        "Rainbow Swirl 4": "彩虹漩涡 4",
        "Rainbow Swirl 5": "彩虹漩涡 5",
        "Rainbow Swirl 6": "彩虹漩涡 6",
        "Snake 1": "蛇形 1",
        "Snake 2": "蛇形 2",
        "Snake 3": "蛇形 3",
        "Snake 4": "蛇形 4",
        "Snake 5": "蛇形 5",
        "Snake 6": "蛇形 6",
        "Knight 1": "骑士 1",
        "Knight 2": "骑士 2",
        "Knight 3": "骑士 3",
        "Christmas": "圣诞",
        "Gradient 1": "渐变 1",
        "Gradient 2": "渐变 2",
        "Gradient 3": "渐变 3",
        "Gradient 4": "渐变 4",
        "Gradient 5": "渐变 5",
        "Gradient 6": "渐变 6",
        "Gradient 7": "渐变 7",
        "Gradient 8": "渐变 8",
        "Gradient 9": "渐变 9",
        "Gradient 10": "渐变 10",
        "RGB Test": "RGB 测试",
        "Alternating": "交替",
    },
    "TabbedKeycodes": {
        "Basic": "基本",
        "Backlight": "背光",
        "App, Media and Mouse": "应用、媒体和鼠标",
        "Layers": "层",
        "User": "用户",
        "Macro": "宏",
        "Tap Dance": "一键多用",
        "Quantum": "高级",
        # "ISO/JIS" and "MIDI" stay as-is: QMK terminology
    },

    # -------------------------------------------------------------- dialogs --
    "TextboxWindow": {
        "Apply": "应用",
        "Cancel": "取消",
        "Copy": "复制",
        "Paste": "粘贴",
        "Undo": "撤销",
    },
    "AnyKeycodeDialog": {
        "Enter an arbitrary keycode": "输入任意键码",
        "Enter an expression": "输入表达式",
        "Invalid input": "输入无效",
        "Invalid input: {}": "输入无效：{}",
        "Computed value: 0x{:X}": "计算结果：0x{:X}",
    },
}


# Strings upstream assembles with str.format(); (regex, replacement) pairs.
PATTERNS = [
    # tap_dance.py builds one of these per Tap Dance slot
    (r"^Use <code>TD\((\d+)\)</code> to set up this action in the keymap\.$",
     r"在键位表中使用 <code>TD(\1)</code> 调用此动作。"),
    # macro recorder status line
    (r"^Memory used by macros: (\d+)/(\d+)$", r"宏占用内存：\1/\2"),
    # "About <manufacturer> <product>..." (menu entry) and the dialog title
    (r"^About (.+)\.\.\.$", r"关于 \1..."),
    (r"^About (.+)$", r"关于 \1"),
]
