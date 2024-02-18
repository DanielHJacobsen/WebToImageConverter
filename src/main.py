import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
import os
import time
from threading import Thread

from util.Config import Config
from util.IntroUtil import IntroPrint
from util.JsonExtraction import JsonExtraction
from util.FileUtil import FileUtil
from util.GifUtil import GifUtil
from handlers.CaptionHandler import CaptionHandler
from handlers.NavigationHandler import NavigationHandler
from handlers.LoginHandler import LoginHandler


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

        driver_collector = self.create_driver()
        driver_slideshow = self.create_driver()

        self.start_screenshot_collection_and_slideshow(config_file, driver_collector, driver_slideshow)

    @staticmethod
    def create_driver():
        driver = webdriver.Chrome()
        driver.fullscreen_window()
        driver.maximize_window()
        return driver

    def start_screenshot_collection_and_slideshow(self, config, driver_collector, driver_slideshow):
        thread_collector = Thread(target=self.loop_collection, args=(config, driver_collector))
        thread_collector.start()

        self.show_loading_screen(driver_slideshow)

        thread_slideshow = Thread(target=self.loop_slide_show, args=(config, driver_slideshow))
        thread_slideshow.start()

    def show_loading_screen(self, driver_slideshow):
        path_to_loading = os.getcwd().replace("src", "") + "resources\\Loading.gif"
        driver_slideshow.get(path_to_loading)

        number_of_attempts = range(5)
        for attempt in number_of_attempts:
            if self.is_empty(self.config.location):
                print("Attempt number: " + str(attempt) + " failed to find any files in configuration directory "
                                                          "of image storage location: " + path_to_loading)
                # 9 seconds matches the duration of the "loading" GIF.
                time.sleep(9)
            else:
                break

    @staticmethod
    def is_empty(path):
        if os.path.exists(path) and not os.path.isfile(path):

            if not os.listdir(path):
                return True
            else:
                return False
        else:
            print("It was not possible to find the directory of the configured image storage location: " + path)
            return False

    def loop_collection(self, config, driver_collector):
        self.collect_screenshots(config, driver_collector)
        self.is_first_run = False
        path_to_loading = os.getcwd().replace("src", "") + "resources\\CollectorOnHold.png"
        driver_collector.get(path_to_loading)
        time.sleep(60)
        self.loop_collection(config, driver_collector)

    def loop_slide_show(self, config, driver):
        for site in config["websites"]:

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
        self.loop_slide_show(config, driver)

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

            if site_url.endswith(".png") or site_url.endswith(".gif") or site_url.endswith(".jpeg"):
                self.gifUtil.download_gif_from_url(site=site, is_first_run=self.is_first_run)

            else:
                self.loginHandler.login(driver=driver,
                                        site=site,
                                        image_name=image_name,
                                        is_with_log=self.is_first_run)

                self.navigationHandler.navigate(driver=driver,
                                                site=site,
                                                image_name=image_name,
                                                image_path=image_path,
                                                is_with_log=self.is_first_run)

                self.captionHandler.add_caption(site=site,
                                                image_path=image_path,
                                                is_with_log=self.is_first_run)

        except NoSuchWindowException:
            print('The website "' + image_name + '" failed due to an NoSuchWindowException.'
                  'This is likely cause by manually closing the browser window while the program is still running.')
            sys.exit()

        except Exception as e:
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
        elif url.endswith(".png"):
            file_format = ".png"
        elif url.endswith(".jpeg"):
            file_format = ".jpeg"
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
