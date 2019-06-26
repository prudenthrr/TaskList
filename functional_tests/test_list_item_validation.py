from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_items(self):
        self.browser.get(self.live_server_url)
        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element_by_css_selector('.has-error').text,
        #         "You cannot have an empty list item!"
        #     ))

        self.input_itmes('Buy peacock feathers')
        self.wait_for_row_in_list_table(row_text='1: Buy peacock feathers')

        self.input_itmes(text='')
        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element_by_css_selector('.has-error').text,
        #         "You cannot have an empty list item!"
        #     ))
