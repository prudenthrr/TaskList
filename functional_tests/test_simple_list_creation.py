from .base import FunctionalTest
from selenium import webdriver


class NewVistorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do',self.browser.title)
        head_txt = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', head_txt)

        self.input_itmes('Buy peacock feathers')
        self.wait_for_row_in_list_table(row_text='1: Buy peacock feathers')

        self.input_itmes('Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table(row_text='2: Use peacock feathers to make a fly')

        self.wait_for_row_in_list_table(row_text='1: Buy peacock feathers')

        #self.fail("finish")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        self.input_itmes('Buy peacock feathers')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        elis_current_url = self.browser.current_url
        self.assertRegex(elis_current_url,'/lists/.+')
        self.browser.quit()

        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        self.input_itmes('Buy milk')
        self.wait_for_row_in_list_table('1: Buy milk')

        fransic_current_url = self.browser.current_url
        self.assertRegex(fransic_current_url,'/lists/.+')
        self.assertNotEqual(fransic_current_url,elis_current_url)

