import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

TEST_EMAIL = 'prudent_hrr@163.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    def test_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        #查看邮箱发送成功的提示
        self.wait_for(lambda: self.assertIn('check your email',self.browser.find_element_by_tag_name('body').text))

        #查看邮箱链接
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL,email.to)
        self.assertEqual(email.subject,SUBJECT)

        #查看邮件链接
        self.assertIn('Use this link to log in',email.body)
        url_search = re.search(r'http://.+/.+$',email.body)
        if not url_search:
            self.fail(f'could not find url in email body:\n{email.body}')
        url = url_search.group()
        self.browser.get(url)

        self.wait_for(lambda : self.browser.find_element_by_link_text('Log out'))
        nvdar = self.browser.find_element_by_css_selector('.navbar').text
        self.assertIn(TEST_EMAIL,nvdar)