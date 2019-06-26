from html import escape
from django.test import TestCase
from lists.models import Item,List
from lists.forms import ItemForm

# Create your tests here.
class HomePageTest(TestCase):
    '''测试URL是否映射到对应打视图函数上'''
    # def test_root_url_to_home_page_views(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)

    def test_user_home_page(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_home_page_uses_itemform(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'],ItemForm)

    def test_saving_and_retrive_items(self):
        list_ = List.objects.create()
        first_item = Item()
        first_item.text = 'The first item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = list_
        second_item.save()

        saved_all_items = Item.objects.all()
        self.assertEqual(saved_all_items.count(),2)
        self.assertEqual(saved_all_items[0].text,'The first item')
        self.assertEqual(saved_all_items[1].text,'The second item')

    def test_can_save_a_post(self):
        self.client.post('/lists/new', data={'text':'A new list item'})

        self.assertEqual(Item.objects.count(), 1)   #Item.objects.count()是Item.objects.all().count()的简写形式
        new_item = Item.objects.first()  #Item.objects.all()[0]
        self.assertEqual(new_item.text,'A new list item')

        # self.assertIn('A new list item',response.content.decode())
        # self.assertTemplateUsed(response,'home.html')

    def test_only_save_item_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)

    # def test_redirects_after_post(self):
    #     response = self.client.post('/lists/new',data={'item_text':'A new list item'})
    #     self.assertEqual(response.status_code,302)
    #     self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        reponse = self.client.get(f'/lists/{list_.id}/')
        #reponse = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(reponse,'list.html')

    def test_display_only_item_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1',list=correct_list)
        Item.objects.create(text='itemey 2',list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        reponse = self.client.get(f'/lists/{correct_list.id}/')
        self.assertContains(reponse,'itemey 1')
        self.assertContains(reponse,'itemey 2')
        self.assertNotContains(reponse,'other list item 1')
        self.assertNotContains(reponse, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'],correct_list)

    def test_save_a_post_to_an_existing_list(self):
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/', data={'text': 'a new item'})
        self.assertEqual(Item.objects.count(),1)
        self.assertEqual(List.objects.count(),1)
        self.assertEqual(Item.objects.first().list, correct_list)
        self.assertRedirects(response,f'/lists/{correct_list.id}/' )

    def test_validation_errors_end_up_on_lists_page(self):
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/', data={'text': ''})
        error = escape("You cannot have an empty list item!")
        # self.assertEqual(response.status_code,200)
        # self.assertTemplateUsed(response,'list.html')
        self.assertContains(response, error)



class NewListTest(TestCase):

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new',data={'text':'A new list item'})
        new_list = List.objects.all()[0]
        self.assertRedirects(response,f'/lists/{new_list.id}/')

    # def test_validation_errors_are_send_back_homepage(self):
    #     response = self.client.post('/lists/new',data={'text':''})
    #     self.assertEqual(response.status_code,200)
    #     self.assertTemplateUsed(response,'home.html')
    #     expected_error =  "You cannot have an empty list item!"
    #     self.assertContains(response,expected_error)

    def test_invaild_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(Item.objects.count(),0)
        self.assertEqual(List.objects.count(),0)


    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new',data={'text':''})
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')


