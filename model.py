from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn import metrics
import pickle
import pandas as pd

def prepare():
    df = pd.read_csv('data/data.csv')

    model = pickle.load(open('bin/recommender.sav', 'rb'))
    ord_enc = OrdinalEncoder()
    ord_enc.fit(df[['reviewed_by']].values)

    return df, model, ord_enc

def recommendation(username: str):
    df, model, ord_enc = prepare()

    products = df['product_id'].unique()
    user_id = int(ord_enc.transform([[username]])[0][0])
    #print(username, user_id)

    X_test = []
    product_urls = []
    for product in products:
        data_input = {}
        data_input['verified'] = df[df['reviewed_by'] == username]['verified'].mode()[0]
        data_input['reviewed_by'] = user_id
        data_input['helpful_count'] = df[df['product_id'] == product]['helpful_count'].max()
        data_input['not_helpful_count'] = df[df['product_id'] == product]['not_helpful_count'].max()
        data_input['average_rating'] = df[df['product_id'] == product]['average_rating'].mode()[0]
        data_input['product_id'] = product
        X_test.append(data_input)
        product_urls.append(list(df[df['product_id'] == product]['product_url'])[0])

    X_test = pd.DataFrame(X_test)
    predicted_rating = model.predict(X_test)
    predicted_df = pd.DataFrame({'product_id': X_test['product_id'], 'rating': predicted_rating, 'product_urls': product_urls})
    top10_df = predicted_df.sort_values(by='rating', ascending=False).head(10)

    return list(top10_df['product_id']), list(top10_df['rating']), list(top10_df['product_urls'])

# recommendation("Michael")
# recommendation("WalmartCustomer")