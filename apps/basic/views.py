from django.shortcuts import render
from django.views import View

class IndexView(View):
    template_name='index.html'

    def get(self, request, *args, **kwargs):
        # formset = modelformset_factory(MyUser, fields={'first_name', 'last_name', 'email', 'password', 'phone'})
        return render(request, self.template_name)
