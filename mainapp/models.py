from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.urls import reverse


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)    
    ROLES = (
    ('Employee', 'Employee'),
    ('Company', 'Company'),
    )
    role = models.CharField(max_length=30, choices=ROLES)
    firstvisit = models.IntegerField(default = 1)
    # Metadata
    class Meta:
        ordering = ['username']
        verbose_name = 'User'
      
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user_id)])

    def __str__(self):
        return str(self.username)
    
    def is_employee(self):
        return self.role == 'Employee'

    def is_company(self):
        return self.role == 'Company'
    
    def is_firstvisit(self):
        return self.firstvisit==1
    
    def get_name(self):
  
        if self.is_employee():
            employee = Employee.objects.get(employee_id=self)
            return f"{employee.firstname} {employee.lastname}"
        elif self.is_company():
            company = Company.objects.get(company_id=self)
            return company.name
        elif self.is_staff:
            return "Admin"
        else:
            return "Register"
    

class Employee(models.Model):

    # Fields
    employee_id = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    firstname   = models.CharField("First Name",max_length=100, help_text='Employee First Name')
    lastname    = models.CharField("Last Name",max_length=100, help_text='Employee Last Name')
    dateOfBirth = models.DateField("Date Of Birth",help_text='Employee Date of Birth')
    gender      = models.CharField(max_length = 8,choices = [('MALE','MALE'),('FEMALE','FEMALE')])
    city        = models.CharField(max_length=50, help_text='Employee City')
    phone       = models.CharField(max_length=20, help_text='Employee Phone')
    education   = models.TextField(max_length=1000,null=True,blank=True)
    experience  = models.TextField(max_length=1000,null=True,blank=True)
    awards      = models.TextField(max_length=1000,null=True,blank=True)
    hobbies     = models.TextField(max_length=1000,null=True,blank=True)
    skills      = models.TextField(max_length=1000)
    references  = models.TextField(max_length=1000,null=True,blank=True)
    other       = models.TextField(max_length=1000,null=True,blank=True)
    cluster     = models.IntegerField(null=True,blank=True)
    clusterable_text   = models.TextField(null=True,blank=True)
    # Metadata
    class Meta:
        verbose_name = 'Employee'


    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('employee-detail', args=[str(self.employee_id_id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.firstname+" "+self.lastname
    
    def get_age(self):
        today = date.today()
        birthyear = self.dateOfBirth.year
        age = today.year - birthyear
        # Account for birthdays not yet passed in the current year
        if (today.month, today.day) < (self.dateOfBirth.month, self.dateOfBirth.day):
            age -= 1
        return str(age)
    


class Company(models.Model):

    # Fields
    company_id = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    name  = models.CharField(max_length=100, help_text='Company Name') 
    city  = models.CharField(max_length=100, help_text='Company City')
    phone = models.CharField(max_length=20, help_text='Company Phone')

    # Metadata
    class Meta:
        verbose_name = 'Company'


    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('company-detail', args=[str(self.company_id_id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
    



class Job_Post(models.Model):
    # Fields
    job_id = models.BigAutoField(primary_key=True)
    job_title = models.CharField(max_length=350)
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,)
    jobDescription  = models.TextField("Job Description",max_length=1000)
    workhours = models.TextField("Work Hours",max_length=1000)
    contact = models.CharField("Contact",max_length=50,)
    city  = models.CharField(max_length=50)
    salary = models.CharField(max_length=50)
    cluster =  models.IntegerField(null=True,blank=True)
    added_date = models.DateField(auto_now_add=True)
    clusterable_text   = models.TextField(null=True,blank=True)
    
    # Metadata
    class Meta:
        verbose_name = 'Job Post'
        ordering = ['-added_date']


    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('job_post-detail', args=[str(self.job_id)])


    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.job_title


class Course(models.Model):

    # Fields
    course_id = models.BigAutoField(primary_key=True)
    courseTitle = models.CharField("Course Title",max_length=50)
    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE)
    description  = models.TextField("Course Description",max_length=1000)
    link = models.CharField("Course Link",max_length=100) 
    cluster =  models.IntegerField(null=True,blank=True)
    clusterable_text   = models.TextField(null=True,blank=True)
    
    # Metadata
    class Meta:
        verbose_name = 'Course'
        ordering = ['company_id']
        
    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.course_id)])

    def __str__(self):
        return self.courseTitle
    
class cluster_records(models.Model):
    added_date = models.DateTimeField(auto_now_add=True)
    silhouette_score = models.FloatField()
    calinski_harabasz_score = models.FloatField()
    number_of_clusters = models.TextField()
    total_records = models.TextField()
    word2vec_vector_size=models.TextField()
    word2vec_window_size=models.TextField()
    word2vec_word_min_count=models.TextField()
    from_date = models.TextField()
    applied = models.BooleanField()

    class Meta:
        ordering = ['-added_date']

    def __str__(self):
        return str(self.id)

class globals(models.Model):
    testing_thread_running = models.BooleanField(default = False)
    number_of_rows = models.IntegerField(default = 0)
    training_thread_running = models.IntegerField(default = False)
    
