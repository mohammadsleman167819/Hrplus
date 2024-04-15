import numpy as np
from ..models import Job_Post,cluster_records,Course,Employee  
from .ML import generate_data
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import silhouette_score
from joblib import dump
from datetime import date  
from django.db.models import Max
import gensim
from .predicting import predict


def train_model(start_date,number_of_clusters,word2vec_vector_size,word2vec_window_size,word2vec_word_min_count):

    first_row = globals.objects.first()
    
    first_row.training_thread_running = True
    first_row.save()
    
    job_posts = Job_Post.objects.filter(added_date__gte=start_date)
    if len(job_posts)==0:
        generate_data()
    
    number_of_records = job_posts.count()
    if word2vec_word_min_count==0:
        word2vec_word_min_count = number_of_records//number_of_clusters
        reduction_factor = 0.15  
        word2vec_word_min_count_reduced = word2vec_word_min_count - (word2vec_word_min_count * reduction_factor)
        word2vec_word_min_count = word2vec_word_min_count_reduced
    
    
    word2vecmodel = gensim.models.Word2Vec(
    window = word2vec_window_size, 
    min_count = word2vec_word_min_count,
    vector_size = word2vec_vector_size)
    
    text_data = list(job_posts.values_list('clusterable_text', flat=True))
    for text in text_data:
            text = gensim.utils.simple_preprocess(text)

    
    
    word2vecmodel.build_vocab(text_data)
    word2vecmodel.train(text_data,total_examples=word2vecmodel.corpus_count,epochs = word2vecmodel.epochs)
    dump(word2vecmodel, 'word2vecmodel.joblib')

    def text_to_vector(text):
      words = text.split()
      return word2vecmodel.wv.get_mean_vector(words)

    vectors=[]
    for text in text_data:
        vectors.append(text_to_vector(text))
        

    vectors_2d = np.stack(vectors)
    model = KMeans(n_clusters = number_of_clusters, init='k-means++', max_iter=5000,n_init='auto')
   
    labels = model.fit_predict(vectors_2d)
     
    dump(model, 'Kmeans_model.joblib')  

    ch_score = calinski_harabasz_score(vectors_2d, labels)
    sil_score = silhouette_score(vectors_2d, labels)

    for i in range(len(job_posts)):
        job_posts[i].cluster=labels[i]
        job_posts[i].save()

    job_posts = Job_Post.objects.filter(added_date__lt=start_date)
    for i in range(len(job_posts)):
        job_posts[i].cluster = predict(job_posts[i].clusterable_text)
        job_posts[i].save()

    courses = Course.objects.all()
    for course in courses:
        course.cluster = predict(course.clusterable_text)
    
    employees = Employee.objects.all()
    for emp in employees:
        emp.cluster = predict(emp.clusterable_text)

    cluster_records.objects.create(calinski_harabasz_score=ch_score, 
                            silhouette_score=sil_score,
                            number_of_clusters=number_of_clusters,
                            total_records=number_of_records,
                            word2vec_vector_size=word2vec_vector_size,
                            word2vec_window_size=word2vec_window_size,
                            word2vec_word_min_count=word2vec_word_min_count,
                            from_date = start_date,
                            applied=True)

    first_row.testing_thread_running = False
    first_row.save()
    
    
from ..models import globals   
import matplotlib.pyplot as plt
import os
def test_n_clusters(start_clusters, end_clusters, step, start_date,word2vec_vector_size,word2vec_window_size,word2vec_word_min_count):
    first_row = globals.objects.first()
    
    first_row.testing_thread_running = True
    first_row.save()
    job_posts = Job_Post.objects.filter(added_date__gte=start_date)
    if len(job_posts)==0:
        generate_data()
    
    ch_scores = []
    silhouette_scores = []
    
    records=[]
    num = 0
    compute = False
    if word2vec_word_min_count==0:
        compute = True
    for n_clusters in range(start_clusters, end_clusters + 1, step):
        number_of_records = job_posts.count()
        num=num+1
        
        if compute:
            word2vec_word_min_count = number_of_records//n_clusters
            reduction_factor = 0.15  
            word2vec_word_min_count_reduced = word2vec_word_min_count - (word2vec_word_min_count * reduction_factor)
            word2vec_word_min_count = word2vec_word_min_count_reduced
        
    
        word2vecmodel = gensim.models.Word2Vec(
        window = word2vec_window_size, 
        min_count = word2vec_word_min_count,
        vector_size = word2vec_vector_size)
        
        text_data = list(job_posts.values_list('clusterable_text', flat=True))
        
        for text in text_data:
            text = gensim.utils.simple_preprocess(text)

        word2vecmodel.build_vocab(text_data, progress_per=1000)
        word2vecmodel.train(text_data,total_examples=word2vecmodel.corpus_count,epochs = word2vecmodel.epochs)
        
        
        def text_to_vector(text):
            words = text.split()
            return word2vecmodel.wv.get_mean_vector(words)

        vectors=[]
        for text in text_data:
            vectors.append(text_to_vector(text))
            

        vectors_2d = np.stack(vectors)
        model = KMeans(n_clusters = n_clusters, init='k-means++', max_iter=5000,n_init=5)

        model.fit(vectors_2d)
        cluster_labels = model.labels_

        # Count the number of data points in each cluster
        unique_labels, counts = np.unique(cluster_labels, return_counts=True)


        ch_score = calinski_harabasz_score(vectors_2d, model.labels_)
        ch_scores.append(ch_score)
        sil_score = silhouette_score(vectors_2d, model.labels_)
        silhouette_scores.append(sil_score)
        new_record = {'calinski_harabasz_score':ch_score, 
                            'silhouette_score':sil_score,
                            'number_of_clusters':n_clusters,
                            'total_records':number_of_records,
                            'word2vec_vector_size':word2vec_vector_size,
                            'word2vec_window_size':word2vec_window_size,
                            'word2vec_word_min_count':word2vec_word_min_count,
                            'from_date' : start_date,
                            'applied':False}
        records.append(new_record)

    for record in records:
        cluster_records.objects.create(
                            calinski_harabasz_score = record['calinski_harabasz_score'], 
                            silhouette_score = record['silhouette_score'],
                            number_of_clusters = record['number_of_clusters'],
                            total_records = record['total_records'],
                            word2vec_vector_size = record['word2vec_vector_size'],
                            word2vec_window_size = record['word2vec_window_size'],
                            word2vec_word_min_count = record['word2vec_word_min_count'],
                            from_date = record['from_date'],
                            applied = record['applied']
        )
    
    first_row.number_of_rows = num
    first_row.save()
    
    fig, ax1 = plt.subplots()  # Create a figure with two subplots
    ax1.plot(range(start_clusters, end_clusters + 1, step),silhouette_scores, marker='o', linestyle='-', label='Silhouette Score')
    ax1.set_xlabel("Number of Clusters")
    ax1.set_ylabel("Silhouette Score", color='b')

    # Create a secondary axis for the silhouette score
    ax2 = ax1.twinx()
    ax2.plot(
      range(start_clusters, end_clusters + 1, step),
      ch_scores,
      marker='s',
      linestyle='-',
      label='Calinski Harabasz Score',
      color='g',)
    ax2.set_ylabel("Calinski Harabasz Score", color='g')

  
    
    plt.title("Scores Per Number Of Clusters")
    plt.grid(True)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent

    static_folder = os.path.join(BASE_DIR, 'static/images')  
    filename = "test_plot.png" 
    filepath = os.path.join(static_folder, filename)

    plt.savefig(filepath, format='png')  # Save as PNG
    plt.close()
    first_row.testing_thread_running=False
    first_row.save()

  
