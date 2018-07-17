from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# My models
from jav.models import Actress

class ActressMethodTest(TestCase):
    
    def test_ensure_view_and_like_are_positive(self):
        """
        ensure_view_and_like_are_positive should results True for actresses where view and like are zero or positive
        """
        act = Actress(name='test',view=-1, like=-1)
        act.save()
        self.assertEqual((act.view == 0 and act.like == 0), True)
        
    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add an actress an appropriate slug line is created
        i.e. "Random Actress String" -> "random-actress-string"
        """
        act = Actress(name="Random Actress String")
        act.save()
        self.assertEqual((act.slug == "random-actress-string"), True)   

def add_cat(name, view, like, image):
    a = Actress.objects.get_or_create(name=name)[0]
    a.view = view
    a.like = like
    a.image = image
    a.save()
    return a        
        
class IndexViewTests(TestCase):
    
    def test_index_view_with_no_categories(self):
        """
        If no actress exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing !!!")
        self.assertQuerysetEqual(response.context['actresses'], []) 

    def test_index_view_with_categories(self):
        """
        If actresses exist, an appropriate message should be displayed.
        """
        image_path = "/mnt/g/Work/062_Django/002_Jav/jav_with_django/media/actress_images/ai-uehara.jpg"
        test_image = SimpleUploadedFile(name='slide-1.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        
        add_cat('test',1,1,test_image)
        add_cat('temp',1,1,test_image)
        add_cat('tmp',1,1,test_image)
        add_cat('tmp test temp',1,1,test_image)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
        # Check item exists
        self.assertContains(response, "tmp test temp")
        
        # Check total return objects
        num_acts =len(response.context['actresses'])
        self.assertEqual(num_acts , 4)        