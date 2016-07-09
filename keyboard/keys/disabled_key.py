from base_key import BaseKey


class DisabledKey(BaseKey):
    def __init__(self, *args, **kwargs):
        super(DisabledKey, self).__init__(*args, **kwargs)
        self.setDisabled(True)
        self.setMinimumWidth(50)
