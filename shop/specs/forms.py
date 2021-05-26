from django import forms

from mainapp.models import Category


class NewCategoryForm(forms.Form):

    class Meta:
        model = Category
        fields = '__all__'
