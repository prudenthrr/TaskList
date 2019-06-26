from django.test import TestCase
#from lists.forms import ItemForm
from lists.forms import ExistingListItemForm
from lists.models import Item,List

class ItemFormTest(TestCase):

    # def test_form_renders_item_text_input(self):
    #     form = ItemForm()
    #     self.fail(form.as_p())

    def test_form_validation_for_blank_items(self):
        list1 = List.objects.create()
        form = ExistingListItemForm(for_list=list1,data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],["You cannot have an empty list item!"])

    def test_duplicate_items_to_a_list_display_erroe(self):
        list1 = List.objects.create()
        form1 = ExistingListItemForm(for_list=list1,data={'text':'bla'})
        form1.save()
        form2 = ExistingListItemForm(for_list=list1,data={'text':'bla'})
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors['text'], ['You have already got this in your list!'])

    def test_can_save_items_to_different_list(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='bla', list=list1)
        form2 = ExistingListItemForm(for_list=list2, data={'text': 'bla'})
        self.assertTrue(form2.is_valid())
