from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import DesignRequest

class DesignRequestAdminForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        design_image = cleaned_data.get("design_image")
        comment = cleaned_data.get("comment")

        if status == "completed" and not design_image:
            raise ValidationError("Для статуса 'Выполнено' необходимо прикрепить изображение.")

        if status == "in_progress" and not comment:
            raise ValidationError("Для статуса 'Принято в работу' необходимо добавить комментарий.")

        return cleaned_data

@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    form = DesignRequestAdminForm
    readonly_fields = ('title', 'description', 'user', 'created_at', 'category', 'image')



    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)

        if obj and obj.status in ["in_progress", "completed"]:
            readonly_fields.extend(["status", "design_image", "comment"])
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('main/admin_design_request.js',)

    def save_model(self, request, obj, form, change):
        if change and obj.status in ["in_progress", "completed"]:
            if 'status' in form.changed_data:
                raise ValidationError("Нельзя изменить статус после того, как заявка принята в работу или завершена.")

        super().save_model(request, obj, form, change)