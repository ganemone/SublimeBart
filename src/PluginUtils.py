import sublime
SETTINGS_FILE = "SublimeBart.sublime-settings"


def get_pref(key):
    return get_settings().get(key)


def get_settings():
    return sublime.load_settings(SETTINGS_FILE)


def set_settings(key, val):
    user_settings = get_settings()
    user_settings.set(key, val)
    sublime.save_settings(SETTINGS_FILE)
