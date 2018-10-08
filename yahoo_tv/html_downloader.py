"""
html.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

LOGGER = logging.getLogger(__name__)


class Html:
    def __init__(self, chromedriver_path: str = None):
        self.__chromedriver_path = chromedriver_path
        self.__page_source = ""

    def get(self, url: str):
        options = Options()
        options.headless = True
        options.add_argument("--log-level=3")

        try:
            if self.__chromedriver_path is None:
                driver = webdriver.Chrome(options=options)
            else:
                driver = webdriver.Chrome(
                    self.__chromedriver_path, chrome_options=options)
        except:
            print("ChromeDownloderのパスを正しく設定してください。(--chrome, -c)")
            return

        driver.set_page_load_timeout(30)

        try:
            driver.get(url)
            LOGGER.debug("The HTML file download have been completed. ")
        except:
            LOGGER.error("It failed to download the HTML file...")

        self.__page_source = driver.page_source.encode(
            "utf-8", "ignore").decode("utf-8")

        driver.close()
        driver.quit()

    @property
    def page_source(self):
        return self.__page_source
