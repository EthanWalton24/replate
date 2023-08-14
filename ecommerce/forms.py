from django import forms
from ecommerce.models import *
from crispy_forms.layout import Layout, Field, Submit
from crispy_forms.helper import FormHelper



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('email', placeholder='Email'),
            Field('password', placeholder='Password'),
            Submit('submit-login', 'Login', css_class='btn btn-dark rounded-0 border-0', style='width: 100%;')
        )
        self.helper.form_show_labels = False



class RegisterForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', placeholder='Name'),
            Field('email', placeholder='Email'),
            Field('password', placeholder='Password'),
            Submit('submit-register', 'Register', css_class='btn btn-dark rounded-0 border-0', style='width: 100%;')
        )
        self.helper.form_show_labels = False



class ProductForm(forms.Form):
    size = forms.ChoiceField(choices=(('M','M   (17.7"/12.6")'),('L','L   (26.6"/18.9")'),('XL','XL   (35.4"/25.2")')))

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('size', placeholder='Size'),
            Submit('submit-cart', 'Add to Cart', css_class='btn btn-dark rounded-0', style='width: calc(100%); font-size: 11px;'),
        )
        self.helper.form_show_labels = False




class ContactForm(forms.ModelForm):
  class Meta:
    model = ContactRequest
    fields = ["name", "email", "purpose", "subject", "message"]

  def __init__(self, *args, **kwargs):
    super(ContactForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
        Field('name', placeholder='Name'),
        Field('email', placeholder='Email'),
        Field('purpose', default='Choose a Purpose'),
        Field('subject', placeholder='Subject'),
        Field('message', placeholder='Message', style='height: 100px; max-width: 450px'),
        Submit('submit-contact', 'Submit', css_class='btn btn-dark rounded-0')
    )
    self.helper.form_show_labels = False


class ContactHistoryForm(forms.Form):
  name = forms.CharField(max_length=200)
  email = forms.CharField(max_length=200)

  def __init__(self, *args, **kwargs):
    super(ContactHistoryForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
        Field('name', placeholder='Name'),
        Field('email', placeholder='Email'),
        Submit('submit-contact-history', 'Submit', css_class='btn btn-dark rounded-0')
    )
    self.helper.form_show_labels = False