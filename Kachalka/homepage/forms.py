from typing import Any
from django import forms
from .models import Records, Statistic, User

class RecordsForm(forms.ModelForm):

    class Meta:
        model = Records
        fields = ('exercise', 'record', 'date')

class StatisticForm(forms.ModelForm):

    class Meta:
        model = Statistic
        fields = '__all__'

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'