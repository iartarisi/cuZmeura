from django.test import TestCase
from pristav.ads.models import Impression

class ServeTests(TestCase):
    fixtures = ['mydata.json']

    def _test_serve_default_publisher(self, puburl):
        """
        Test for default publisher.
        """
        response = self.client.get('/serve/' + puburl)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ad_url'], u'http://ceata.org/')
        self.assertEqual(response.context['ad_name'], u'Ceata')
        self.assertEqual(response.context['ad_img_url'],
                         u'http://localhost:8000/media/ads/ceata_.png')

    def test_serve_default_publisher(self):
        self._test_serve_default_publisher('')
        
    def test_serve_pristav_publisher(self):
        self._test_serve_default_publisher('pristav')

    def test_serve_notexists_publisher(self):
        response = self.client.get('/serve/notfound')
        self.assertEqual(response.status_code, 404)

    def test_serve_size_match_regex(self):
        response = self.client.get('/serve/pristav/')
        self.assertEqual(response.context['ad_size'], '125x125')
        
        response = self.client.get('/serve/pristav/125x125')
        self.assertEqual(response.context['ad_size'], '125x125')

    def test_serve_size_not_found(self):
        response = self.client.get('/serve/pristav/0x0')
        self.assertEqual(response.status_code, 404)

    def test_serve_size_mismatch_regex(self):
        invalid_url = ['/serve/x125',
                        '/serve/x125',
                        '/serve/x12y',
                        '/serve/125x',
                        '/serve/12yx',
                        '/serve/125x1y',
                        '/serve/12yx125',
                        '/serve/y']
        for res in invalid_url:
            response = self.client.get(res)
            self.assertEqual(response.status_code, 404)

    def test_serve_correct_referer_netloc(self):
        response = self.client.get('/serve/pristav/125x125',
                                   HTTP_REFERER='http://pristav.ceata.org/xmpl')
        impre = Impression.objects.all()[0]
        self.assertEqual(impre.referer, 'http://pristav.ceata.org/xmpl')
        self.assertEqual(impre.referer_netloc, 'http://pristav.ceata.org')
        # clean up
        Impression.objects.all()[0].delete()
