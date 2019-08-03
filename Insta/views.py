from django.views.generic import TemplateView

# create my own view heritaize template view
class HelloWorld(TemplateView):
    template_name = 'test.html'
