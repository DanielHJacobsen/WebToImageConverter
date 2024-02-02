from util.JsonExtraction import JsonExtraction


class Config(object):

    timeout = 5
    location = ""
    refresh_interval = 5
    time_per_slide = 5

    jsonExt = JsonExtraction()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        # noinspection PyUnresolvedReferences
        return cls.instance

    def setup_configuration_util(self, config_file):
        location = self.jsonExt.extract_with_failure(config_file, "image_directory", "config_file")
        timeout = self.jsonExt.extract(config_file, "allowed_timeout", 5, "config_file", True)
        refresh_interval = self.jsonExt.extract(config_file, "refresh_interval", 5, "refresh_interval", True)
        time_per_slide = self.jsonExt.extract(config_file, "time_per_slide", 5, "time_per_slide", True)

        self.location = location
        self.timeout = timeout
        self.time_per_slide = time_per_slide
        self.refresh_interval = refresh_interval

