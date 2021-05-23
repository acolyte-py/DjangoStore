from django.shortcuts import render
from django.views import View


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})
