from django.apps import AppConfig

class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
    def ready(self):
        from .models import Employee,Job_Post,Course,CustomUser
        from django.db.models.signals import post_save
        from .signals import preprocess_text
        post_save.connect(preprocess_text, sender=Job_Post)
        post_save.connect(preprocess_text, sender=Course)
        post_save.connect(preprocess_text, sender=Employee)
