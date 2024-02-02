import sys
import requests
from util.JsonExtraction import JsonExtraction
from util.Config import Config


class GifUtil:
    jsonExt = JsonExtraction()
    config = Config()

    def download_gif_from_url(self, site, is_first_run):
        url = self.jsonExt.extract_with_failure(site, "url", "websites")
        image_name = self.jsonExt.extract_with_failure(site, "image_name", "websites")
        skip_if_failed = self.jsonExt.extract(site, "skip_if_failed", True, "websites", is_first_run)

        r = requests.get(url)
        if r.ok:
            with open(self.config.location + "/" + image_name + ".gif", 'wb') as outfile:
                outfile.write(r.content)
        else:
            if is_first_run:
                print(r)
            if not skip_if_failed:
                sys.exit()
