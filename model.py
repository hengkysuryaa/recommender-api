from sklearn.preprocessing import OrdinalEncoder
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

def history(username: str):
    # Get top 10 recently bought product
    df, _, _ = prepare()
    bought_products = df[df['reviewed_by'] == username]['product_id'].unique()
    top10_recently = []
    for product in bought_products:
        data_input = {}
        data_input['product_id'] = str(product)
        data_input['rating'] = list(df[(df['product_id'] == product) & (df['reviewed_by'] == username)]['rating'])[0]
        data_input['product_urls'] = list(df[df['product_id'] == product]['product_url'])[0]
        top10_recently.append(data_input)
    
    top10_recently = pd.DataFrame(top10_recently).head(10)

    return list(top10_recently['product_id']), list(top10_recently['rating']), list(top10_recently['product_urls'])


def recommendation(username: str):
    # Get top 10 recommended products
    df, model, ord_enc = prepare()

    bought_products = df[df['reviewed_by'] == username]['product_id'].unique()
    products = df[(df['reviewed_by'] != username) & (~df['product_id'].isin(bought_products))]['product_id'].unique()
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