from django.urls import path
from . import views
from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', views.index, name='index'),
    ]


#company
urlpatterns += [
    path('company/<int:pk>', views.CompanyDetailView.as_view(), name='company-detail'),    
    path('company/firstvisit/', views.firstVisitCompany, name='company-first-visit'),    
    path('company/<int:pk>/update/', views.CompanyUpdate.as_view(), name='company-update'),
]

#job posts
urlpatterns += [
    path('job_posts/', views.Job_PostListView.as_view(), name='posts'),
    path('company/myposts/', views.Company_Job_PostListView.as_view(), name='myposts'),
    path('job_post/<int:pk>', views.Job_PostDetailView.as_view(), name='job_post-detail'),
    path('job_post/create/', views.Job_PostCreate, name='job_post-create'),
    path('job_post/<int:pk>/update/', views.Job_PostUpdate.as_view(), name='job_post-update'),
    path('job_post/<int:pk>/delete/', views.Job_PostDelete.as_view(), name='job_post-delete'),
    path('employee/myposts/', views.Employee_Job_PostListView.as_view(), name='suggested-posts'),

]

#courses
urlpatterns += [
    path('courses',views.CourseListView.as_view(),name='courses'),
    path('company/mycourses/',views.Company_CourseListView.as_view(),name='mycourses'),
    path('course/<int:pk>', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/create/', views.CourseCreate, name='course-create'),
    path('course/<int:pk>/update/', views.CourseUpdate.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', views.CourseDelete.as_view(), name='course-delete'),
    path('employee/mycourses/', views.Employee_CourseListView.as_view(), name='suggested-courses'),
]

#employees
urlpatterns += [
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee-update'),
    path('employee/firstvisit/', views.firstVisitEmployee, name='employee-first-visit'),    
    path('employees',views.EmployeeListView.as_view(),name='employees'),
    path('employee/<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    
]

urlpatterns +=[
    path('train_model/', views.train_model_view, name='train_model'),
    path('model_results/', views.cluster_recordsListView.as_view(), name='model_results'),
    path('clusters_number_test/', views.test_n_clusters_view, name='test_clusters_number'),

]