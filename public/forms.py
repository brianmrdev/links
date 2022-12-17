from django.forms import ModelForm
from bookmark.models import Link

class AddLinkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddLinkForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Titulo"
        self.fields['name'].widget.attrs = {'class': 'form-control'}
        self.fields['url'].label = "URL"
        self.fields['url'].widget.attrs = {'class': 'form-control'}
        self.fields['description'].label = "Descripción"
        self.fields['description'].widget.attrs = {'class': 'form-control'}
        self.fields['category'].label = "Categoria"
        self.fields['category'].widget.attrs = {'class': 'form-select select2'}
        self.fields['is_private'].label = "Privado"
        self.fields['is_private'].widget.attrs = {'class': 'form-check-input'}

    class Meta:
        model = Link
        fields = ['category', 'name', 'url', 'description', 'is_private']