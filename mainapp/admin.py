from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Company,Employee,Course,Job_Post,cluster_records



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id',"email", "username","role")

admin.site.register(CustomUser, CustomUserAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name','city','phone')
    list_filter  = ('city',)

admin.site.register(Company, CompanyAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('firstname', 'lastname', 'dateOfBirth','city','phone')
        }),
        ('Resume', {
            'fields': ('education', 'experience','awards','hobbies','skills','references','other')
        }),
        (None,{
            'fields':('cluster',)
        }),
    )
    list_display = ('firstname','lastname','dateOfBirth','city','phone','cluster')

    list_filter  = ('cluster','city')

admin.site.register(Employee, EmployeeAdmin)

class Job_PostAdmin(admin.ModelAdmin):
    list_display = ('job_title','company_id','contact','city','salary','cluster','added_date')
    list_filter  = ('company_id','cluster','city')

admin.site.register(Job_Post, Job_PostAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseTitle','company_id','link','cluster')
    list_filter  = ('cluster',)

   
admin.site.register(Course, CourseAdmin)

class cluster_recordsAdmin(admin.ModelAdmin):
    list_display = ('silhouette_score','calinski_harabasz_score','number_of_clusters','total_records','word2vec_word_min_count','word2vec_window_size','word2vec_vector_size','added_date',)
    list_filter  = ('number_of_clusters',)


admin.site.register(cluster_records,cluster_recordsAdmin)

