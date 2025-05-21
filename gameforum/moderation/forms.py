from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('report_type', 'description')  # исправлено
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите причину жалобы'}),
        }
