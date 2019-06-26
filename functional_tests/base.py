import time
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from unittest import skip
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os


MAX_WAIT = 10
class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        #super().setUp()
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://'+staging_server

    def tearDown(self):
        super().tearDown()
        self.browser.quit()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_for_row_in_list_table(self,row_text):
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # # self.assertTrue(any(row.text=='Buy peacock feathers' for row in rows),"did not appear")
        # self.assertIn(row_text, [row.text for row in rows], "did not appear")
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows], "did not appear")
                return
            except(AssertionError, WebDriverException) as e:
                if time.time()-start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def input_itmes(self,text):
        inputbox = self.get_item_input_box()
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def wait_for(self,fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except(AssertionError, WebDriverException) as e:
                if time.time()-start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

