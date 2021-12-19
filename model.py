from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn import metrics
import surprise
import pickle
import pandas as pd

MODEL_NAME = "SVD.sav"

def prepare():
    df = pd.read_csv('data/data.csv')

    model = pickle.load(open('bin/' + MODEL_NAME, 'rb'))

    ord_enc = OrdinalEncoder()
    ord_enc.fit(df[['reviewed_by']].values)

    return df, model, ord_enc

def recommendation(username: str):
    df, model, ord_enc = prepare()

    products = df['product_id'].unique()
    user_id = int(ord_enc.transform([[username]])[0][0])

    predicted_rating = []
    product_urls = []
    for product in products:
        data_input = {}
        data_input['product_id'] = str(product)
        data_input['rating'] = model.predict(str(product), user_id).est
        predicted_rating.append(data_input)
        product_urls.append(list(df[df['product_id'] == product]['product_url'])[0])

    predicted_rating = pd.DataFrame(predicted_rating)
    recommendations = pd.DataFrame({'product_id': predicted_rating['product_id'], 'rating': predicted_rating['rating'],
                                'product_urls': product_urls})
    top10_df = recommendations.sort_values(by='rating', ascending=False).head(10)

    return list(top10_df['product_id']), list(top10_df['rating']), list(top10_df['product_urls'])