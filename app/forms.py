from django import forms
from .models import WorkDay, Project, Contributor
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.db.models import Q
import datetime

class WorkDayForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = ['project', 'date', 'days']
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y', attrs={'class': "date-field"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        # Get a list of projects that the current user has contributed to
        contributed_projects = Contributor.objects.filter(contributor=self.user).values_list('project__pk', flat=True)

        super(WorkDayForm, self).__init__(*args, **kwargs)
        # Only allow the user to log time against projects they either own or are contributors on
        self.fields['project']=forms.ModelChoiceField(queryset=Project.objects.filter(Q(owner=self.user) | Q(id__in=contributed_projects)),
                                                       widget=forms.Select(attrs={'class': "project-field"},)
                                                      )
class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['projectName', 'time_units']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(AddProjectForm, self).__init__(*args, **kwargs)
        # Exclude current user in list of contributors (current user will be the owner.)
        self.fields['contributors']=forms.ModelMultipleChoiceField(queryset=User.objects.exclude(pk=self.user.pk))

class EditProjectForm(AddProjectForm):
    def __init__(self, *args, **kwargs):
        self.contributors = kwargs.pop('contributors', None)
        # The list of selected contributors is passed from Views to the form.
        # We then use a list comprehension to set the initial values
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.fields['contributors'].initial = [c.pk for c in self.contributors]

class CreateAccountForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
