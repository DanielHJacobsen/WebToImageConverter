class Config(object):

    timeout = 5
    location = ""
    refresh_interval = 5
    time_per_slide = 5

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
