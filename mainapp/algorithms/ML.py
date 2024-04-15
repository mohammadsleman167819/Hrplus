import re
import nltk
from nltk.stem import PorterStemmer
import csv
from ..models import Job_Post  
import os
from django.core.exceptions import ValidationError

#nltk.download('stopwords')

def generate_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, 'it_upload.csv')
    with open(absolute_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  
        for row in reader:
            try:
                jop_post = Job_Post(job_title=row[0],
                            company_id_id=39,
                            jobDescription=row[1],
                            workhours=24,
                            contact="abc",
                            city="damascus",
                            salary="123$",
                            clusterable_text=preprocess(row[0]+" "+row[1]))    
                jop_post.save()
            except ValidationError:
                pass


def preprocess(text):

    final_string = ""
    # Make lower
    text = text.lower()

    # Remove line breaks
    text = re.sub(r'\n', ' ', text)

    # Remove unwanted punctuation
    text = re.sub(r'"', ' ', text)  
    text = re.sub(r"[£'!$%&()*,-./:;<=>?@[\]^_`{|}~]",' ',text)
    text = re.sub(r"\s+",' ',text)
    

    # Remove stop words
    text = text.split()
    useless_words = nltk.corpus.stopwords.words("english")
    
    text_filtered = [word for word in text if not word in useless_words]
    stemmer = PorterStemmer() 
    text_stemmed = [stemmer.stem(y) for y in text_filtered]
    

    final_string = ' '.join(text_stemmed)
    return final_string
