from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD

app = Flask(__name__)

# Load data
df = pd.read_csv("./data.csv")


# Utility function to get recommendations
def get_recommendations(user_id):
    # Create ratings utility matrix

    ratings_utility_matrix = df.pivot_table(
        values="rating", index="user", columns="product_id", fill_value=0
    )
    print(ratings_utility_matrix)

    X = ratings_utility_matrix.T
    SVD = TruncatedSVD(n_components=3)
    decomposed_matrix = SVD.fit_transform(X)
    correlation_matrix = np.corrcoef(decomposed_matrix)

    X.index[1]
    i = "Mechanic3"

    product_names = list(X.index)
    product_ID = product_names.index(i)
    print(product_ID)

    correlation_product_ID = correlation_matrix[product_ID]
    print(correlation_product_ID)

    Recommend = list(X.index[correlation_product_ID > 0.95])

    # Removes the item already bought by the customer
    Recommend.remove(i)

    return Recommend[:3]


@app.route("/popular", methods=["GET"])
def get_popular_products():
    # Group by product_id and count ratings
    df = pd.read_csv("./data.csv")
    popular_products = pd.DataFrame(df.groupby("product_id")["rating"].count())
    most_popular = popular_products.sort_values("rating", ascending=False)
    sorted_popular_products = dict(sorted(most_popular.to_dict().items()))

    # ll={'vals':((sorted_popular_products)['rating']).keys()}
    # return jsonify({"popular_products": (sorted_popular_products)})
    ll=list(sorted_popular_products["rating"].keys())
    return jsonify(ll)

@app.route("/recommendations", methods=["POST","GET"])
def recommend_products():
    user_id = request.args.get("user_id")
    # user_id='Bob'
    if user_id:
        recommendations = get_recommendations("user_id")
        return jsonify({"recommendations": recommendations})
    else:
        return jsonify({"error": "User ID not provided"})


if __name__ == "__main__":
    app.run(debug=True)
