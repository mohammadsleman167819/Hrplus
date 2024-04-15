from django.shortcuts import redirect
from django.urls import reverse



class FirstVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
       
        if request.path == "/accounts/logout/":
            response = self.get_response(request)
            return response

        if request.user.is_authenticated and request.user.is_firstvisit() :
            if request.user.is_employee():
                if request.path != reverse('employee-first-visit'):
                    return redirect(reverse("employee-first-visit"))
            elif request.user.is_company():
                if request.path != reverse('company-first-visit'):
                    return redirect(reverse("company-first-visit"))
   

        response = self.get_response(request)
        return response



class RedirectAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/':
            return redirect('/admin/mainapp')
        return self.get_response(request)
