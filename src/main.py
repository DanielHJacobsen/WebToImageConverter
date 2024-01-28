import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import os
import time

from src.util.Config import Config
from src.util.IntroUtil import IntroPrint
from src.handlers.CaptionHandler import CaptionHandler
from src.handlers.NavigationHandler import NavigationHandler
from src.handlers.LoginHandler import LoginHandler
from src.util.JsonExtraction import JsonExtraction
from src.util.FileUtil import FileUtil
from src.util.GifUtil import GifUtil


class Main:
    is_first_run = True
    captionHandler = CaptionHandler()
    navigationHandler = NavigationHandler()
    gifUtil = GifUtil()
    loginHandler = LoginHandler()
    jsonExt = JsonExtraction()
    config = Config()
    fileUtil = FileUtil()

    def start(self):
        IntroPrint().print_ascii_art()

        config_file = FileUtil.load_config_file()

        self.config.setup_configuration_util(config_file)

        self.delete_old_files()

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.fullscreen_window()
        driver.maximize_window()

        self.start_screenshot_collection_and_slideshow(config_file, driver)

    def start_screenshot_collection_and_slideshow(self, config, driver):
        self.collect_screenshots(config, driver)
        self.run_slide_show(config, driver)
        self.is_first_run = False
        self.start_screenshot_collection_and_slideshow(config, driver)

    def run_slide_show(self, config, driver):
        for interation in range(self.config.refresh_interval):
            self.loop_slide_show(config, driver, interation)

    def loop_slide_show(self, config, driver, interation):
        for site in config["websites"]:
            if not self.is_screenshot_iteration(interation, site):
                continue

            image_name_with_format = site["image_name"] + self.get_file_format(site)
            try:
                path = self.config.location + "/" + image_name_with_format
                file_exits = os.path.exists(path)

                if file_exits:
                    self.handle_existing_image(driver, path, site)
                else:
                    self.handle_missing_image(path, site)

            except NoSuchWindowException as e:
                print(e.msg)
                print("Was the program terminated manually? - If so, don't worry about this log.")
                sys.exit()

    def is_screenshot_iteration(self, interation, site):
        show_for_every_x_iteration = self.jsonExt.extract(site,
                                                          "show_for_every_x_interation",
                                                          1,
                                                          "websites",
                                                          self.is_first_run)
        return ((interation + 1) % show_for_every_x_iteration) == 0

    def handle_existing_image(self, driver, path, site):
        driver.get(path)
        self.timeout_on_screenshot(site)

    def timeout_on_screenshot(self, site):
        # noinspection PyBroadException
        try:
            time.sleep(self.get_time_on_slide(site))
        except:
            print("Was the program terminated manually? - If so, don't worry about this log.")
            sys.exit()

    def get_time_on_slide(self, site):
        time_for_slide_override = self.jsonExt.extract(
            site,
            "time_for_slide_override",
            0,
            "websites",
            self.is_first_run
        )
        if not time_for_slide_override == 0:
            time_on_slide = time_for_slide_override
        else:
            time_on_slide = self.config.time_per_slide
        return time_on_slide

    def handle_missing_image(self, path, site):
        print('There was found no file with the path "' + path + '"')
        skip_if_failed = self.jsonExt.extract(site, "skip_if_failed", True, "websites", self.is_first_run)
        if skip_if_failed:
            print('The website was configured as "skip_if_failed" and '
                  'the website will therefore be skipped.')
        else:
            print('The website was configured as not "skip_if_failed" and '
                  'the failure shall therefore cause termination of the program.')
            sys.exit()

    def collect_screenshots(self, config, driver):
        websites = self.jsonExt.extract_with_failure(config, "websites", "config")
        for site in websites:
            self.collect_snapshot(driver, site)

    def collect_snapshot(self, driver, site):
        skip_if_failed = self.jsonExt.extract(site, "skip_if_failed", True, "websites", self.is_first_run)
        # noinspection PyBroadException
        try:
            image_name = self.jsonExt.extract_with_failure(site, "image_name", "websites")
            image_name_with_format = image_name + self.get_file_format(site)
            site_url = self.jsonExt.extract_with_failure(site, "url", image_name)
            driver.get(site_url)
            image_path = self.config.location + "/" + image_name_with_format

            self.loginHandler.login(driver=driver,
                                    site=site,
                                    image_name=image_name,
                                    is_with_log=self.is_first_run)

            if site_url.endswith(".png") or site_url.endswith(".gif"):
                self.gifUtil.download_gif_from_url(site=site, is_first_run=self.is_first_run)

            else:
                self.navigationHandler.navigate(driver=driver,
                                                site=site,
                                                image_name=image_name,
                                                image_path=image_path,
                                                is_with_log=self.is_first_run)

                self.captionHandler.add_caption(site=site,
                                                image_path=image_path,
                                                is_with_log=self.is_first_run)

        except:
            print('The website "' + image_name + '" failed due to an undefined error.')
            if skip_if_failed:
                print('The website will therefore be skipped.')
            else:
                print('The website was configured as not "skip_if_failed" and '
                      'the failure shall therefore cause termination of the program.')
                sys.exit()

    def get_file_format(self, site):
        url = self.jsonExt.extract_with_failure(site, "url", "websites")
        if url.endswith(".gif"):
            file_format = ".gif"
        else:
            file_format = ".png"
        return file_format

    def delete_old_files(self):
        location = self.config.location

        for filename in os.listdir(location):
            if (os.path.isfile(os.path.join(location, filename)) and
                    (filename.endswith(".png") or filename.endswith(".gif"))):

                os.remove(os.path.join(location, filename))


if __name__ == "__main__":
    Main().start()
