from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from django.template.loader import render_to_string

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() #
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        #self.assertTrue(response.content.startswith(b'<html>')) 
        #self.assertIn(b'<title>To-Do lists</title>', response.content) 
        #self.assertTrue(response.content.endswith(b'</html>')) 
        # django r当请求一张页面时，Django把请求的metadata数据包装成一个HttpRequest对象，
        #然后Django加载合适的view方法,把这个HttpRequest 对象作为第一个参数传给view方法。
        #任何view方法都应该返回一个HttpResponse对象。
    

    #def test_home_page_can_save_a_POST_request(self):     
    #    request = HttpRequest()
    #    request.method = 'POST'
    #    request.POST['item_text'] = 'A new list item'

     #   response = home_page(request)

        # The render_to_string shortcut takes one required argument – template_name, 
        #which should be the name of the template to load and render (or a list of 
        # template names, in which case Django will use the first template in the list 
        # that exists) – and two optional arguments:

      #  self.assertEqual(Item.objects.count(), 1) 
      #  new_item = Item.objects.first()   
       # self.assertEqual(new_item.text, 'A new list item')

        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/')

        #self.assertIn('A new list item', response.content.decode())
        #expected_html = render_to_string(
        #    'home.html',
        #    {'new_item_text':  'A new list item'}
        #)
        #self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)



    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


from lists.models import Item

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
