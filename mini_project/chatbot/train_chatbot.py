import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def load_and_preprocess_data(csv_file):
    data = pd.read_csv(csv_file)
    vectorizer = TfidfVectorizer(stop_words='english')
    feature_vectors = vectorizer.fit_transform(data['query'])
    return data, vectorizer, feature_vectors

def train_kmeans_model(feature_vectors, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(feature_vectors)
    return kmeans

def predict_cluster(query, vectorizer, kmeans_model):
    query_vec = vectorizer.transform([query])
    cluster_label = kmeans_model.predict(query_vec)[0]
    return cluster_label

def main():
    csv_file = r'C:\Users\SHAFIA SABA\OneDrive\Desktop\chatbot_query.csv'  # Update with your actual path
    data, vectorizer, feature_vectors = load_and_preprocess_data(csv_file)
    kmeans_model = train_kmeans_model(feature_vectors)
    return kmeans_model, vectorizer

if __name__ == "__main__":
    kmeans_model, vectorizer = main()


