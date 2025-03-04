from django import forms
from .models import user_det,user_login,Expert_det,Language_selection,AssessmentQuestion

class user_details(forms.ModelForm):
    class Meta:
        model=user_det
        fields=['name','contact']
        widgets ={
            'name':forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'contact': forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
        }

class login_data(forms.ModelForm):
    class Meta:
        model=user_login
        fields=['email','password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control rounded-2 py-1'}),
        }
class logindata(forms.ModelForm):
    class Meta:
        model=user_login
        fields=['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-2 py-1'}),
            }
class loginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control rounded-2 py-4', 'placeholder': 'Enter Your Email'}))
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-2 py-4', 'placeholder': 'Enter Your Password'})
    )

class Expert_login(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=Expert_det.OPTIONS,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Expert_det
        fields = ['name', 'gender','age', 'experience', 'language', 'contact_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'gender':forms.Select(attrs={'class':'form-control rounded-2 py-1'}),
            'age': forms.NumberInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'language': forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'experience': forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control rounded-2 py-1'}),
        }
class lang_selectionForm(forms.ModelForm):
    class Meta:
        model= Language_selection
        fields=['language']
class Question_from(forms.ModelForm):
    class Meta:
        model= AssessmentQuestion
        fields=['language','question_text','difficulty','options1','options2','options3','correct_answer']
class Difficulty_form(forms.ModelForm):
    class Meta:
        model =Language_selection
        fields=['difficulty']
class QuizForm(forms.Form):
    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)
        if question:
            self.fields['answer'] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    (question.options1, question.options1),
                    (question.options2, question.options2),
                    (question.options3, question.options3),
                ],
                widget=forms.RadioSelect,
                required=True
            )
