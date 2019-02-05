from django.test import TestCase
from django.urls import URLPattern, URLResolver, resolvers, reverse, resolve
from django.conf import settings
from pyVerein.urls import urlpatterns
import re
from django.http import HttpResponseRedirect

# Credit: Douglas @ https://stackoverflow.com/a/35760156/9652454
def get_urls(urlpatterns, parent=''):
    patterns = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            if not str(pattern.pattern).startswith('admin'):
                patterns += get_urls(pattern.url_patterns, parent + str(pattern.pattern))
        elif isinstance(pattern, URLPattern):
            patterns.append(parent + str(pattern.pattern))
    
    return patterns

class AppTestMethods(TestCase):
    def test_login_required(self):
        "Test if urls redirect to login_url if no user is logged in and login is required"
        parameter_map = {
            'int': '0',
            'str': 'a',
            'slug': 'building-your-1st-django-site',
            'uuid': '075194d3-6885-417e-a8a8-6c931e272f00'
        }
        login_not_required_urls = [
            reverse('account:login'),
        ]
        urls = get_urls(urlpatterns)
        regex = re.compile(r'\<(?P<type>int|str|slug|uuid)\:[a-zA-Z0-9\-\_]*\>')
        login_url = reverse('account:login')
        for url in urls:
            for match in regex.finditer(url):
                url = regex.sub(parameter_map[match.group('type')], url, count=1)
            
            url = '/' + url if not url.startswith('/') else url
            response = self.client.get(url)
            
            if type(response) is HttpResponseRedirect:
                response_url = response.url
            else:
                response_url = url
            if url in login_not_required_urls:
                try:
                    self.assertEqual(response.status_code, 200)
                except AssertionError as e:
                    res = resolve(url)
                    e.args = (e.args[0] + '\n Url %s:%s is enforcing login!' % (res.namespace, res.url_name),)
                    raise 
            else:
                try:
                    if '?' in response_url:
                        redirect_url = login_url + response_url[response_url.find('?'):]
                    else:
                        redirect_url = login_url
                    self.assertRedirects(response, redirect_url)
                except AssertionError as e:
                    res = resolve(url)
                    e.args = (e.args[0] + '\n Url %s:%s is not enforcing login!' % (res.namespace, res.url_name),)
                    raise 