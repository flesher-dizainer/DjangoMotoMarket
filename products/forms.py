from django import forms

from products.models import Product, ProductReview


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
    images = MultipleFileField(label='Фотографии', required=False)

    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at', 'quantity', 'reserved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['author', 'text', 'rating']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'rating': forms.Select(choices=[
                (5, 'Отлично (5 звезд)'),
                (4, 'Хорошо (4 звезды)'),
                (3, 'Удовлетворительно (3 звезды)'),
                (2, 'Плохо (2 звезды)'),
                (1, 'Ужасно (1 звезда)'),
            ]),
            'text': forms.Textarea(attrs={'rows': 3}),
        }
