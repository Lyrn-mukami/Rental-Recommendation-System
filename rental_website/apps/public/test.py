import sys, django, os
from django.conf import settings
sys.path.append(r"C:\Users\mbote\OneDrive\Desktop\Projects\Rental-Recommendation-System")
os.environ["DJANGO_SETTINGS_MODULE"] = "rental_website.settings"
django.setup()

from joblib import load
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from rental_website.apps.employee.models import Property
# model = load('Rental-Recommendation-System/rental_website/SavedModel/model.joblib')
model_path = os.path.join(settings.BASE_DIR, "rental_website", "SavedModel", "model.joblib")
model = load(model_path)
class Recommender():
    def transformer(user_df):
    #Get the listing of all properties from the DB and convert it to a dataframe
        listing = Property.objects.all() 
        listing_df = pd.DataFrame.from_records(listing.values('location__area', 'bedrooms', 'bathrooms', 'price'))
        listing_df.rename(columns={'location__area': 'location'}, inplace=True)
        processed_df = listing_df[['location','bedrooms','bathrooms','price']].copy()

    #Encode the location column and scale all the record DB values      
        label_encoder = LabelEncoder()
        label_encoder.fit(processed_df['location'])
        processed_df['location'] = label_encoder.transform(processed_df['location'])
        scaler = MinMaxScaler()
        scaler.fit(processed_df)        

    #Encode the location column and scale all the record DB values 
        user_df['location'] = label_encoder.transform(user_df['location'].values)
        user_df[['location','bedrooms','bathrooms','price']] = scaler.transform(user_df)
        return listing_df, user_df
    
    def list_predict(features_df, clustered_df,user_df): #used to provide predictions when multiple listings exists
        preds = model.predict(user_df)
        user_df['cluster'] = preds
        # Store results for each user record
        all_results = []

        for i, pred in enumerate(preds):
            # Extract single user row for cosine similarity
            single_user = user_df.iloc[[i]]

            # Retrieve the listings from the same cluster
            property_df = clustered_df[clustered_df['cluster'] == pred].copy()

            # Perform cosine similarity (compare only with single_user)
            cosine_similarity_score = cosine_similarity(property_df, single_user)
            property_df['cos_score'] = cosine_similarity_score

            # Sort by similarity score and then by price
            sorted_df = property_df.sort_values(['cos_score', 'price'], ascending=[False, True])

            # Replace normalized values with actual feature values
            sorted_df = sorted_df.astype({'location': 'object'})
            sorted_df.loc[:, ['location', 'bedrooms', 'bathrooms', 'price']] = features_df[['location', 'bedrooms', 'bathrooms', 'price']]

            # Take top 3 results
            sorted_df = sorted_df.iloc[:3]

            # Final sort by price
            final_df = sorted_df.sort_values('price')

            # Store each listing's recommendations
            all_results.append(final_df)

        return all_results
    
    def predict(features_df, clustered_df, user_df): #used to provide predictions when one listing exists
        pred = model.predict(user_df)
        pred = int(pred[0])

        user_df['cluster'] = pred
    #Retrieve the listings from the same cluster
        property_df = clustered_df[clustered_df['cluster'] == pred].copy()

        #Perform cosine similarity
        cosine_similarity_score = cosine_similarity(property_df, user_df)
        property_df['cos_score'] = cosine_similarity_score
        #Sorting the data by cos_score descending
        sorted_df = property_df.sort_values(['cos_score' ,'price'], ascending=[False,True])
        #Replacing normalized values with actual values
        sorted_df = sorted_df.astype({'location': 'object'})
        sorted_df.loc[:, ['location', 'bedrooms', 'bathrooms','price']] = features_df[['location', 'bedrooms', 'bathrooms','price']]
        # sorted_df = sorted_df.sample(n=3, weights=sorted_df['cos_score'])
        sorted_df = sorted_df.iloc[:3,]
        final_df = sorted_df.sort_values(['price'])
        return final_df
    
    def recommend(userdata):
        if isinstance(userdata, dict):
            user_df = pd.DataFrame([userdata])  # wrap in list
        else:
            user_df = pd.DataFrame(userdata)

        clustered_df = os.path.join(settings.BASE_DIR, "rental_website", "SavedModel", "clustered.csv")
        clustered_df = pd.read_csv(clustered_df)
        clustered_df = clustered_df.drop(['Unnamed: 0'], axis=1)
        features_df, data = Recommender.transformer(user_df)
        if user_df.shape[0] == 1: #checks if the dataframe has more than one record 
            return Recommender.predict(features_df, clustered_df, data)
        else:
           return Recommender.list_predict(features_df, clustered_df, data)


        

user_data = {
        "location": "Off Denis Pritt, Kilimani, Dagoretti North",
        "bedrooms": 2,
        "bathrooms": 1,
        "price": 40000
            }

    
transformed_user = Recommender.recommend(user_data)
print("User Data:\n", transformed_user)
