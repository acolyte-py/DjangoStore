from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

from .forms import NewCategoryForm


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})


class NewCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.name = form.cleaned_data['name']
            new_category.save()
        return HttpResponseRedirect('/product-specs/')

