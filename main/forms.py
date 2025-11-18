from django import forms
from .models import ProjectLink

class ProjectLinkAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectLink
        fields = '__all__'
        widgets = {
            'style': forms.RadioSelect,
        }
        
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=200, help_text='Your telegram/discord/email/etc')
