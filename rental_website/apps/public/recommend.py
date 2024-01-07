from joblib import load
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
model = load('rental_website/SavedModel/model.joblib')

class Recommender():
    def recommend(data):
        #transforming dictionary to a dataframe
        data= pd.DataFrame.from_dict(data)
        features_df = pd.read_csv('rental_website/SavedModel/features.csv')
        features_df = features_df.drop(['Unnamed: 0'], axis=1)
        encoded_df = pd.read_csv('rental_website/SavedModel/encoded_df.csv')
        encoded_df =encoded_df.drop(['Unnamed: 0'], axis=1)
        clustered_df = pd.read_csv('rental_website/SavedModel/clustered.csv')
        clustered_df = clustered_df.drop(['Unnamed: 0'], axis=1)
        #encode the location
        label_encoder = LabelEncoder()
        label_encoder.fit(features_df['location'])
        data['location'] = label_encoder.transform(data['location'])

        #normalizing the data
        scaler = MinMaxScaler()
        scaler.fit(encoded_df)
        data[['location','bedrooms','bathrooms','price']] = scaler.transform(data)

        #Predict the cluster
        pred = model.predict(data)

        data['cluster'] = pred
        #Retrieve the listings from the same cluster
        if pred == 0:
            property_df = clustered_df[clustered_df['cluster'] == 0]
        elif pred == 1:
            property_df = clustered_df[clustered_df['cluster'] == 1]
        else:
            property_df = clustered_df[clustered_df['cluster'] == 2]

        #Perform cosine similarity
        cosine_similarity_score = cosine_similarity(property_df, data)
        property_df['cos_score'] = cosine_similarity_score
        #Sorting the data by cos_score descending
        sorted_df = property_df.sort_values(['cos_score'], ascending=False)
        #Replacing normalized values with actual values
        sorted_df.loc[:, ['location', 'bedrooms', 'bathrooms','price']] = features_df[['location', 'bedrooms', 'bathrooms','price']]
        sorted_df = sorted_df.iloc[ :10 ,:-2]
        return sorted_df