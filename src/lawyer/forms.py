from django import forms
from lawyer.models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ("name", "email", "phone_number", "date", "comment")
