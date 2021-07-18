
from django import forms
from dashboard.mixins import FormControlMixin 
from dashboard.models import Todo, TodoUser
from django.contrib.auth.forms import PasswordChangeForm

class TodoForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','description','status']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['status'].widget.attrs.update({
                'class': "control outlined control-checkbox checkbox-success"
            })

        
class TodoRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Email *'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Password *'}))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'required': 'true',
        'placeholder': 'Retype Password *'}))

    class Meta:
        model = TodoUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not confirm_password:
            raise forms.ValidationError("You must confirm your password")
        if password != confirm_password:
            raise forms.ValidationError("Your passwords do not match")
        return confirm_password



class TodoLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':  'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Password'}))
    
    

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = TodoUser.objects.filter(username=username, is_active=True).first()
        if user == None or not user.check_password(password):
            raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data

class TodoUserPasswordResetForm(FormControlMixin, forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter email address'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if TodoUser.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("User with this email doesn't exist")

        return email

class TodoUserChangePasswordForm(PasswordChangeForm):
    old_password_flag = True

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'Old Password'}))

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'New Password'}))

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':  'New Password again'}))

    def set_user(self, user):
        self.user = user

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        valpwd = self.cleaned_data.get('new_password1')
        valrpwd = self.cleaned_data.get('new_password2')

        if valpwd != valrpwd:
            raise forms.ValidationError({
                'new_password1': 'Password Not Matched'})
        else:
            pass
        return self.cleaned_data