from django.views.generic import TemplateView


# Create your views here.
class EventPageView(TemplateView):
    template_name = 'event/event.html'
