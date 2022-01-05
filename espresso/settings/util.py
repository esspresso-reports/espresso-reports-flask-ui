def convert_settings(settings):
    settings_dict = {}
    for setting_key in settings:
        splitted_setting_key = setting_key.split('.')
        _settings = settings_dict

        for key in splitted_setting_key[:-1]:
            if key not in _settings.keys():
                _settings[key] = {}
            _settings = _settings[key]

        _settings[splitted_setting_key[-1]] = settings[setting_key]

    return settings_dict
