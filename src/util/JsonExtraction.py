import sys


class JsonExtraction:

    @staticmethod
    def extract(json_object, key, default_value, object_reference, is_with_log):
        is_scroll_to_selector = default_value
        try:
            is_scroll_to_selector = json_object[key]
        except KeyError:
            if is_with_log:
                print('There is no ' + key + '-property for the "' + object_reference + '"-object.')
                print('Using default value of: ', default_value)
        return is_scroll_to_selector

    @staticmethod
    def extract_with_failure(json_object, key, object_reference):
        try:
            return json_object[key]
        except KeyError:
            print('The required key of ' + key + ' is missing for the "' + object_reference + '"-object.')
            sys.exit()
