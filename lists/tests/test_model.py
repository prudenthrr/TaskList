from unittest import skip

from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item,List


# Create your tests here.


class ListAndItemModelsTest(TestCase):

    def testa_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        firstItem = Item()
        firstItem.text = 'The first (ever) list item'
        firstItem.list = list_
        firstItem.save()

        secondItem = Item()
        secondItem.text = 'The second list item'
        secondItem.list = list_
        secondItem.save()

        saved_lists = List.objects.all()
        self.assertEqual(List.objects.first(), list_)
        self.assertEqual(saved_lists[0], list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        self.assertEqual(saved_items[0].text, 'The first (ever) list item')
        self.assertEqual(saved_items[0].list, list_)
        self.assertEqual(saved_items[1].text, 'The second list item')
        self.assertEqual(saved_items[1].list, list_)

    def test_cannot_save_empty_items(self):
        list_ = List.objects.create()
        item = Item(text='',list=list_)
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    @skip
    def test_duplicate_items_are_saved(self):
        list_ = List.objects.create()
        Item.objects.create(text='bla',list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='bla', list=list_)
            item.save()

    def test_can_save_same_items_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='bla',list=list1)
        Item.objects.create(text='bla',list=list2)


