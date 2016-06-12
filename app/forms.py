from django import forms
from .models import WorkDay
import datetime

class WorkDayForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = ['project', 'date', 'days']
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y', attrs={'class': "date"}),
            'project': forms.Select(attrs={'class': "project"}),
        }
