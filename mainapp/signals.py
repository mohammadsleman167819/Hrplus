from .models import Employee
from .models import Job_Post
from .models import Course
from django.db.models.signals import post_save
from .algorithms.ML import preprocess
from .algorithms.predicting import predict


def preprocess_text(sender, instance, created, **kwargs):
        text_field_name = {
            Employee: lambda instance: instance.education +" "+ instance.experience +" "+ instance.awards +" "+ instance.skills,
            Job_Post: lambda instance: instance.jobDescription + " " + instance.job_title,
            Course:   lambda instance: instance.description,
        }.get(sender)
        
        if text_field_name:
            text = text_field_name(instance)
            clusterable_text = preprocess(text)
            instance.clusterable_text = clusterable_text

            try:
                predicted_cluster = predict(clusterable_text)  # Replace with your ML model
                instance.cluster = predicted_cluster
            except Exception as e:
                print(f"Error during prediction for {instance.__str__} : {e}")
        else:
            print(f"Unexpected sender model: {sender}")

