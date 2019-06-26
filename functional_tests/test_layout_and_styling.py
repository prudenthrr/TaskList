from .base import FunctionalTest

class LayoutAndStyleTest(FunctionalTest):

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2, 512,delta=10
        )