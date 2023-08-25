from django import forms
from .models import UploadedContent


class UploadContentForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = UploadedContent
        fields = ('image', 'video')

    def __init__(self, *args, **kwargs):
        super(UploadContentForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'upload-field'})
