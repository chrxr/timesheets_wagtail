from django import forms
from .models import WorkDay
import datetime

class WorkDayForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = ['project', 'date', 'hours']
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y'),
        }
