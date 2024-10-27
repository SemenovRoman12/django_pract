from django import forms
from .models import DesignRequest, Category

class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'comment', 'design_image']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('comment')
        design_image = cleaned_data.get('design_image')

        if status == 'in_progress' and not comment:
            self.add_error('comment', 'Для принятия заявки в работу необходимо указать комментарий.')

        if status == 'completed' and not design_image:
            self.add_error('design_image', 'Для завершения заявки необходимо загрузить изображение дизайна.')
