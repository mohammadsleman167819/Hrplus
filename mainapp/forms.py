from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Course,Company,Job_Post,Employee
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=50, help_text='Unique Name',widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(label="Email", max_length=50, help_text='Unique Email',widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    role = forms.ChoiceField(choices=[('','Choose..'),('Employee', 'Employee'),('Company', 'Company')], label="Role",widget=forms.Select(attrs={'class': 'form-select'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
  
    class Meta:
        model = CustomUser
        fields = ("username", "email","role","password1","password2")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email","role")

from django import forms
from datetime import date


class EmployeeInfoForm(forms.Form):
    firstname = forms.CharField(label="First Name", max_length=100, help_text='Employee First Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label="Last Name", max_length=100, help_text='Employee Last Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateOfBirth = forms.DateField(label="Date Of Birth", help_text='Employee Date of Birth',
                                  widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date" , 'class': 'form-control'}),
                                    input_formats=["%Y-%m-%d"])
    gender = forms.ChoiceField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], label="Gender",widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=50, help_text='Employee City',widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone", max_length=20,min_length=10, help_text='Employee Phone',widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(label="Education", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    experience = forms.CharField(label="Experience", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    awards = forms.CharField(label="Awards", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    hobbies = forms.CharField(label="Hobbies", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    skills = forms.CharField(label="Skills", max_length=1000,widget=forms.Textarea(attrs={'class': 'form-control'}))
    references = forms.CharField(label="References", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    other = forms.CharField(label="Other", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data

    def clean_dateOfBirth(self):       
        data = self.cleaned_data["dateOfBirth"]
        birthyear = data.year
        today = date.today()
        age = today.year - birthyear
        if (today.month, today.day) < (data.month, data.day):
            age -= 1 
        if data > today:
            raise ValidationError('Date of birth cannot be in the future.')
        minimum_age = 16 
        maximum_age = 120  
        if age < minimum_age:
            raise ValidationError(f'You must be at least {minimum_age} years old to register.')
        if age > maximum_age:
            raise ValidationError(f'{age} years old is not a valid value.')

        return data


class CompanyInfoForm(forms.Form):
    name  = forms.CharField(label = "Comapany Name", max_length = 100,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    city = forms.CharField(label="City", max_length=50,
                           widget = forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone", max_length=20,min_length=10,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    

    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data

    
class Job_PostCreateForm(forms.Form):
    
    job_title = forms.CharField(label="Job Title",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    jobDescription = forms.CharField(label="Job Description", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    workhours = forms.CharField(label="Work Hours", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    contact = forms.CharField(label="Contact",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.CharField(label="Salary", max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    

class CourseCreateForm(forms.Form):
    
    courseTitle = forms.CharField(label="Course Title",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    description  = forms.CharField(label="Course Description", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    link = forms.CharField(label="Course Link", max_length=100,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 

    
from .models import Job_Post

class TrainModelForm(forms.Form):
    number_of_clusters = forms.IntegerField(label="number_of_clusters",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=2
                                            )
    word2vec_vector_size = forms.IntegerField(label="word2vec vector size",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=100
                                            )
    word2vec_window_size = forms.IntegerField(label="word2vec window size",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'}),
                                            min_value=5
                                            )
    word2vec_word_min_count = forms.IntegerField(label="word2vec word_min_count",help_text="Put 0 for auto compute",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'}),
                                            min_value=0
                                            )
    start_date = forms.DateField(label="Use Data Starting From:",help_text="Default to use all data",widget = forms.DateInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(TrainModelForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = self.get_min_added_date()
        self.fields['word2vec_window_size'].initial = 12
        self.fields['word2vec_vector_size'].initial = 2500
        self.fields['word2vec_word_min_count'].initial = 0
    def get_min_added_date(self):
        min_date = Job_Post.objects.filter(added_date__isnull=False).order_by('added_date').first()
        if min_date:
            return min_date.added_date
        else:
            # Handle case where no Job_Posts exist (optional)
            return date.today()

class test_n_clusters_form(forms.Form):
    
    start_number = forms.IntegerField(label="Min n.of.clusters",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=2
                                            )

    end_number = forms.IntegerField(label="Max n.of.clusters",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=2
                                            )
    
    step = forms.IntegerField(label="Step between tests",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'}),
                                            min_value=1
                                            )
    word2vec_vector_size = forms.IntegerField(label="word2vec vector size",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=100
                                            )
    word2vec_window_size = forms.IntegerField(label="word2vec window size",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'}),
                                            min_value=5
                                            )
    word2vec_word_min_count = forms.IntegerField(label="word2vec word_min_count",help_text="Put 0 for auto compute",required=True,
                                            widget = forms.NumberInput(attrs={'class': 'form-control'})
                                            ,min_value=0
                                            )
    start_date = forms.DateField(label="Use Data Starting From:",help_text="Default to use all data",widget = forms.DateInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(test_n_clusters_form, self).__init__(*args, **kwargs)
        self.fields['start_date'].initial = self.get_min_added_date()
        self.fields['word2vec_window_size'].initial = 12
        self.fields['word2vec_vector_size'].initial = 2500
        self.fields['word2vec_word_min_count'].initial = 0
    
    def get_min_added_date(self):
        min_date = Job_Post.objects.filter(added_date__isnull=False).order_by('added_date').first()
        if min_date:
            return min_date.added_date
        else:
            return date.today()
    def clean_end_number(self):
        data1 = self.cleaned_data['end_number']
        data2 = self.cleaned_data['start_number']
        if data1<data2:
            raise ValidationError('Max number of clusters must be smaller or equal to Min number')
        return data1

class CourseForm(forms.ModelForm):
    
    courseTitle = forms.CharField(label="Course Title",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    description  = forms.CharField(label="Course Description", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    link = forms.CharField(label="Course Link", max_length=100,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
   

    class Meta:
        model = Course
        fields = ('courseTitle', 'description', 'link')

class CompanyForm(forms.ModelForm):
    
    name  = forms.CharField(label = "Comapany Name", max_length = 100,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    city = forms.CharField(label="City", max_length=50,
                           widget = forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone", max_length=20,min_length=10,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    

    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data
   

    class Meta:
        model = Company
        fields = ('name','city','phone')


class Job_PostForm(forms.ModelForm):

    job_title = forms.CharField(label="Job Title",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'})) 
    jobDescription = forms.CharField(label="Job Description", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    workhours = forms.CharField(label="Work Hours", max_length=1000,
                            widget = forms.Textarea(attrs={'class': 'form-control'}))
    contact = forms.CharField(label="Contact",max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))
    salary = forms.CharField(label="Salary", max_length=50,
                            widget = forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Job_Post
        fields = ('job_title', 'jobDescription', 'workhours', 'contact','city','salary')

class EmployeeForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name", max_length=100, help_text='Employee First Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label="Last Name", max_length=100, help_text='Employee Last Name',widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateOfBirth = forms.DateField(label="Date Of Birth", help_text='Employee Date of Birth',
                                  widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date" , 'class': 'form-control'}),
                                    input_formats=["%Y-%m-%d"])
    gender = forms.ChoiceField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], label="Gender",widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.CharField(label="City", max_length=50, help_text='Employee City',widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone", max_length=20,min_length=10, help_text='Employee Phone',widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(label="Education", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    experience = forms.CharField(label="Experience", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    awards = forms.CharField(label="Awards", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    hobbies = forms.CharField(label="Hobbies", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    skills = forms.CharField(label="Skills", max_length=1000,widget=forms.Textarea(attrs={'class': 'form-control'}))
    references = forms.CharField(label="References", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    other = forms.CharField(label="Other", max_length=1000, required=False,widget=forms.Textarea(attrs={'class': 'form-control'}))  
    def clean_phone(self):
        data = self.cleaned_data['phone']

        for char in data:
           if not char.isdigit() and char not in '-+':
                raise ValidationError('Phone number can only contain digits, hyphens, and plus signs.')

        return data

    def clean_dateOfBirth(self):       
        data = self.cleaned_data["dateOfBirth"]
        birthyear = data.year
        today = date.today()
        age = today.year - birthyear
        if (today.month, today.day) < (data.month, data.day):
            age -= 1 
        if data > today:
            raise ValidationError('Date of birth cannot be in the future.')
        minimum_age = 16 
        maximum_age = 120  
        if age < minimum_age:
            raise ValidationError(f'You must be at least {minimum_age} years old to register.')
        if age > maximum_age:
            raise ValidationError(f'{age} years old is not a valid value.')

        return data

    class Meta:
        model = Employee
        fields = ('firstname','lastname','dateOfBirth','gender',
              'city','phone','education','experience','awards',
              'hobbies','skills','references','other')