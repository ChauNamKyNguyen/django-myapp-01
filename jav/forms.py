from django import forms

# Django applications
from django.contrib.auth.models import User

# My models
from jav.models import Actress, Movie
from jav.models import UserProfile


class ActressForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the actress name.")
    view = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    like = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)    
    
    # An incline class to provide additional information on the form
    class Meta:
        # Provide an association between the MovieForm and an model
        model = Actress
        fields = ('name', 'image')
        
class MovieForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Title")
    url = forms.URLField(max_length=200, help_text="URL")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    like = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    date = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the MovieForm and an model
        model = Movie
        
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we not want to include them ...
        # Here, we are hiding the foreign key.
        # we can either exclude the actress field from the form,
        exclude = ('actress',)
        # or specify the fields to include (i.e. not include the actress field)
        # fields = ('title', 'url', 'views')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        
        # If url is not empty and doesn't start with 'http://', prepend  'http://'
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data    

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add class 'special' into input tag
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'special'})
                
    class Meta:
        model = User
        fields = ('username', 'email', 'password')        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')