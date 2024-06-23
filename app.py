from flask import Flask, request
import requests
import pandas as pd

app = Flask(__name__)

# Hardcoded API key
RENT_CAST_API_KEY = 'acfccec5460e4959ac61d2c61cc476c2'

pricing_data = [

    {"sqft_range": "0-999", "bedrooms": 1, "bathrooms": 1, "deep_clean": 229, "standard_clean": 119, "move_in_out": 279},
    {"sqft_range": "0-999", "bedrooms": 1, "bathrooms": 1.5, "deep_clean": 239, "standard_clean": 129, "move_in_out": 289},
    {"sqft_range": "0-999", "bedrooms": 1, "bathrooms": 2, "deep_clean": 239, "standard_clean": 139, "move_in_out": 289},
    {"sqft_range": "0-999", "bedrooms": 1, "bathrooms": 2.5, "deep_clean": 249, "standard_clean": 149, "move_in_out": 299},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 1, "deep_clean": 239, "standard_clean": 129, "move_in_out": 289},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 1.5, "deep_clean": 249, "standard_clean": 139, "move_in_out": 299},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 2, "deep_clean": 249, "standard_clean": 149, "move_in_out": 299},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 2.5, "deep_clean": 259, "standard_clean": 159, "move_in_out": 309},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 3, "deep_clean": 259, "standard_clean": 169, "move_in_out": 309},
    {"sqft_range": "0-999", "bedrooms": 2, "bathrooms": 3.5, "deep_clean": 299, "standard_clean": 179, "move_in_out": 349},
    {"sqft_range": "1000-1499", "bedrooms": 1, "bathrooms": 1, "deep_clean": 259, "standard_clean": 159, "move_in_out": 279},
    {"sqft_range": "1000-1499", "bedrooms": 1, "bathrooms": 1.5, "deep_clean": 269, "standard_clean": 169, "move_in_out": 289},
    {"sqft_range": "1000-1499", "bedrooms": 1, "bathrooms": 2, "deep_clean": 269, "standard_clean": 179, "move_in_out": 289},
    {"sqft_range": "1000-1499", "bedrooms": 1, "bathrooms": 2.5, "deep_clean": 279, "standard_clean": 189, "move_in_out": 299},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 1, "deep_clean": 269, "standard_clean": 169, "move_in_out": 289},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 1.5, "deep_clean": 279, "standard_clean": 179, "move_in_out": 299},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 2, "deep_clean": 279, "standard_clean": 189, "move_in_out": 299},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 2.5, "deep_clean": 289, "standard_clean": 199, "move_in_out": 309},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 3, "deep_clean": 289, "standard_clean": 209, "move_in_out": 309},
    {"sqft_range": "1000-1499", "bedrooms": 2, "bathrooms": 3.5, "deep_clean": 329, "standard_clean": 219, "move_in_out": 349},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 1, "deep_clean": 279, "standard_clean": 179, "move_in_out": 299},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 1.5, "deep_clean": 289, "standard_clean": 189, "move_in_out": 309},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 2, "deep_clean": 289, "standard_clean": 199, "move_in_out": 309},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 2.5, "deep_clean": 299, "standard_clean": 209, "move_in_out": 319},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 3, "deep_clean": 299, "standard_clean": 219, "move_in_out": 319},
    {"sqft_range": "1000-1499", "bedrooms": 3, "bathrooms": 3.5, "deep_clean": 339, "standard_clean": 229, "move_in_out": 359},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 1, "deep_clean": 289, "standard_clean": 189, "move_in_out": 309},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 1.5, "deep_clean": 299, "standard_clean": 199, "move_in_out": 319},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 2, "deep_clean": 299, "standard_clean": 209, "move_in_out": 319},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 2.5, "deep_clean": 309, "standard_clean": 219, "move_in_out": 329},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 3, "deep_clean": 309, "standard_clean": 229, "move_in_out": 329},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 3.5, "deep_clean": 349, "standard_clean": 239, "move_in_out": 369},
    {"sqft_range": "1000-1499", "bedrooms": 4, "bathrooms": 4, "deep_clean": 349, "standard_clean": 249, "move_in_out": 369},
    {"sqft_range": "1500-1999", "bedrooms": 1, "bathrooms": 1, "deep_clean": 289, "standard_clean": 179, "move_in_out": 359},
    {"sqft_range": "1500-1999", "bedrooms": 1, "bathrooms": 1.5, "deep_clean": 299, "standard_clean": 189, "move_in_out": 369},
    {"sqft_range": "1500-1999", "bedrooms": 1, "bathrooms": 2, "deep_clean": 299, "standard_clean": 199, "move_in_out": 369},
    {"sqft_range": "1500-1999", "bedrooms": 1, "bathrooms": 2.5, "deep_clean": 309, "standard_clean": 209, "move_in_out": 379},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 1, "deep_clean": 299, "standard_clean": 189, "move_in_out": 369},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 1.5, "deep_clean": 309, "standard_clean": 199, "move_in_out": 379},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 2, "deep_clean": 309, "standard_clean": 209, "move_in_out": 379},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 2.5, "deep_clean": 319, "standard_clean": 219, "move_in_out": 389},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 3, "deep_clean": 319, "standard_clean": 229, "move_in_out": 389},
    {"sqft_range": "1500-1999", "bedrooms": 2, "bathrooms": 3.5, "deep_clean": 359, "standard_clean": 239, "move_in_out": 429},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 1, "deep_clean": 309, "standard_clean": 199, "move_in_out": 379},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 1.5, "deep_clean": 319, "standard_clean": 209, "move_in_out": 389},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 2, "deep_clean": 319, "standard_clean": 219, "move_in_out": 389},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 2.5, "deep_clean": 329, "standard_clean": 229, "move_in_out": 399},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 3, "deep_clean": 329, "standard_clean": 239, "move_in_out": 399},
    {"sqft_range": "1500-1999", "bedrooms": 3, "bathrooms": 3.5, "deep_clean": 369, "standard_clean": 249, "move_in_out": 439},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 1, "deep_clean": 319, "standard_clean": 209, "move_in_out": 389},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 1.5, "deep_clean": 329, "standard_clean": 219, "move_in_out": 399},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 2, "deep_clean": 329, "standard_clean": 229, "move_in_out": 399},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 2.5, "deep_clean": 339, "standard_clean": 239, "move_in_out": 409},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 3, "deep_clean": 339, "standard_clean": 249, "move_in_out": 409},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 3.5, "deep_clean": 379, "standard_clean": 259, "move_in_out": 449},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 4, "deep_clean": 379, "standard_clean": 269, "move_in_out": 449},
    {"sqft_range": "1500-1999", "bedrooms": 4, "bathrooms": 4.5, "deep_clean": 389, "standard_clean": 279, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 1, "bathrooms": 1, "deep_clean": 349, "standard_clean": 199, "move_in_out": 439},
    {"sqft_range": "2000-2499", "bedrooms": 1, "bathrooms": 1.5, "deep_clean": 359, "standard_clean": 209, "move_in_out": 449},
    {"sqft_range": "2000-2499", "bedrooms": 1, "bathrooms": 2, "deep_clean": 359, "standard_clean": 219, "move_in_out": 449},
    {"sqft_range": "2000-2499", "bedrooms": 1, "bathrooms": 2.5, "deep_clean": 369, "standard_clean": 229, "move_in_out": 459},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 1, "deep_clean": 359, "standard_clean": 209, "move_in_out": 449},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 1.5, "deep_clean": 369, "standard_clean": 219, "move_in_out": 459},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 2, "deep_clean": 369, "standard_clean": 229, "move_in_out": 459},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 2.5, "deep_clean": 379, "standard_clean": 239, "move_in_out": 469},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 3, "deep_clean": 379, "standard_clean": 249, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 2, "bathrooms": 3.5, "deep_clean": 419, "standard_clean": 259, "move_in_out": 509},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 1, "deep_clean": 369, "standard_clean": 219, "move_in_out": 459},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 1.5, "deep_clean": 379, "standard_clean": 229, "move_in_out": 469},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 2, "deep_clean": 379, "standard_clean": 239, "move_in_out": 469},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 2.5, "deep_clean": 389, "standard_clean": 249, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 3, "deep_clean": 389, "standard_clean": 259, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 3, "bathrooms": 3.5, "deep_clean": 429, "standard_clean": 269, "move_in_out": 519},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 1, "deep_clean": 379, "standard_clean": 229, "move_in_out": 469},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 1.5, "deep_clean": 389, "standard_clean": 239, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 2, "deep_clean": 389, "standard_clean": 249, "move_in_out": 479},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 2.5, "deep_clean": 399, "standard_clean": 259, "move_in_out": 489},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 3, "deep_clean": 399, "standard_clean": 269, "move_in_out": 489},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 3.5, "deep_clean": 439, "standard_clean": 279, "move_in_out": 529},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 4, "deep_clean": 439, "standard_clean": 289, "move_in_out": 529},
    {"sqft_range": "2000-2499", "bedrooms": 4, "bathrooms": 4.5, "deep_clean": 469, "standard_clean": 299, "move_in_out": 559},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 2, "deep_clean": 399, "standard_clean": 259, "move_in_out": 489},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 2.5, "deep_clean": 409, "standard_clean": 269, "move_in_out": 499},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 3, "deep_clean": 409, "standard_clean": 279, "move_in_out": 499},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 3.5, "deep_clean": 449, "standard_clean": 289, "move_in_out": 539},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 4, "deep_clean": 449, "standard_clean": 299, "move_in_out": 539},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 4.5, "deep_clean": 479, "standard_clean": 309, "move_in_out": 569},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 5, "deep_clean": 479, "standard_clean": 319, "move_in_out": 569},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 5.5, "deep_clean": 509, "standard_clean": 329, "move_in_out": 599},
    {"sqft_range": "2000-2499", "bedrooms": 5, "bathrooms": 6, "deep_clean": 509, "standard_clean": 339, "move_in_out": 599},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 1.5, "deep_clean": 409, "standard_clean": 259, "move_in_out": 499},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 2, "deep_clean": 409, "standard_clean": 269, "move_in_out": 499},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 2.5, "deep_clean": 419, "standard_clean": 279, "move_in_out": 509},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 3, "deep_clean": 419, "standard_clean": 289, "move_in_out": 509},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 3.5, "deep_clean": 459, "standard_clean": 299, "move_in_out": 549},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 4, "deep_clean": 459, "standard_clean": 309, "move_in_out": 549},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 4.5, "deep_clean": 489, "standard_clean": 319, "move_in/out": 579},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 5, "deep_clean": 489, "standard_clean": 329, "move_in_out": 579},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 5.5, "deep_clean": 519, "standard_clean": 339, "move_in_out": 609},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 6, "deep_clean": 519, "standard_clean": 349, "move_in/out": 609},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 6.5, "deep_clean": 549, "standard_clean": 359, "move_in_out": 639},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 7, "deep_clean": 549, "standard_clean": 369, "move_in/out": 639},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 7.5, "deep_clean": 579, "standard_clean": 379, "move_in_out": 669},
    {"sqft_range": "2000-2499", "bedrooms": 6, "bathrooms": 8, "deep_clean": 579, "standard_clean": 389, "move_in/out": 669}
]

def format_price(price):
    return f"${price}.99"

def get_cleaning_prices(sqft, bedrooms, bathrooms):
    for data in pricing_data:
        sqft_min, sqft_max = map(int, data["sqft_range"].split('-'))
        if sqft_min <= sqft <= sqft_max and data["bedrooms"] == bedrooms and data["bathrooms"] == bathrooms:
            deep_clean = format_price(data["deep_clean"])
            standard_clean = format_price(data["standard_clean"])
            move_in_out = format_price(data["move_in_out"])
            return deep_clean, standard_clean, move_in_out
    return None, None, None  # If no match found

def get_property_records(rent_cast_api_key, address):
    url = "https://api.rentcast.io/v1/properties"
    querystring = {"address": address}
    headers = {
        "accept": "application/json",
        "X-Api-Key": rent_cast_api_key
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Real Estate App</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            .hero-text {
                font-size: 3rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="text-center">
                <img src="/static/logo.png" alt="Logo" class="img-fluid mb-4" style="width: 25%;">
            </div>
            <div class="hero-text">Cleaning Made Simple.</div>
            <form action="/property" method="post" class="mt-4">
                <div class="row">
                    <div class="col-md-6">
                        <div class="input-group">
                            <input type="text" id="address" name="address" class="form-control" placeholder="Enter an address, neighborhood, city, or ZIP code" required>
                            <div class="input-group-append">
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-search"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''
    return html_content

@app.route('/property', methods=['POST'])
def property():
    address = request.form['address']
    property_data = get_property_records(RENT_CAST_API_KEY, address)
    df_prop = pd.json_normalize(property_data)

    property_stats = {}
    expected_columns = {
        "squareFootage": "Square Footage",
        "bedrooms": "Bedrooms",
        "bathrooms": "Bathrooms",
        "yearBuilt": "Year Built",
        "lotSize": "Lot Size",
        "propertyType": "Property Type"
    }

    for col, display_name in expected_columns.items():
        if col in df_prop.columns:
            property_stats[display_name] = df_prop.loc[0, col]
        else:
            property_stats[display_name] = "N/A"

    sqft = property_stats.get("Square Footage", 0)
    bedrooms = property_stats.get("Bedrooms", 0)
    bathrooms = property_stats.get("Bathrooms", 0)
    deep_clean, standard_clean, move_in_out = get_cleaning_prices(sqft, bedrooms, bathrooms)

    if deep_clean is None and standard_clean is None and move_in_out is None:
        pricing_info = "Please contact us for a customized quote."
    else:
        pricing_info = f"""
        <p><strong>Deep Clean Price:</strong> {deep_clean}</p>
        <p><strong>Standard Clean Price:</strong> {standard_clean}</p>
        <p><strong>Move in/out Price:</strong> {move_in_out}</p>
        <p>If any of this information is incorrect, please contact us.</p>
        """

    stats_list = ''.join([f"<li><strong>{key}:</strong> {value}</li>" for key, value in property_stats.items()])
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Property Info</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center">Property Information</h1>
            <div class="card mt-4">
                <div class="card-body">
                    {pricing_info}
                    <h2>Property Details</h2>
                    <ul>
                        {stats_list}
                    </ul>
                </div>
            </div>
            <img src="/static/mop.jpg" alt="Mop Image" class="img-fluid mt-4">
            <a href="/" class="btn btn-secondary mt-3">Go Back</a>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''
    return html_content

if __name__ == '__main__':
    app.run(debug=True)