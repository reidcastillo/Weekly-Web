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
        <title>Weekly Home Cleaning</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
            body {
                background-color: #007bff; /* Solid blue color for the entire page */
                font-family: 'Bebas Neue', sans-serif;
            }
            .header, .footer {
                background-color: white;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                position: relative;
                z-index: 10;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header img {
                width: 15%;
            }
            .content {
                background-color: #007bff; /* Solid blue background for the content */
                height: 70vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: flex-end;
                position: relative;
                z-index: 5;
                text-align: right;
                padding: 2rem;
            }
            .yellow-field {
                background-color: linear-gradient(to top, #007bff, #fff); /* Solid blue background for the yellow field */
                padding: 100px 0; 
                text-align: right;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: flex-end;
                width: 100%;
                padding-right: 15%;
            }
            .hero-text-container {
                display: flex;
                align-items: center;
                justify-content: flex-end;
                width: 100%;
                padding-right: 5%;
                flex-direction: column;
                position: relative;
                z-index: 2;
            }
            .hero-text {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: white; /* Bold and white text for "Cleaning Made Simple." */
            }
            .input-group {
                width: 50%; /* Adjusted width for the search bar */
                margin: 0 auto;
                text-align: right;
            }
            .search-box {
                background: #007bff;
                border-radius: 15px;
                padding: 0px;
                
                display: flex;
                align-items: left;
                justify-content: center;
                width: 133%;
                margin: left auto;
            }
            .sponge-box {
                width: 900px; /* Adjust size as needed */
                height: 600px;
                background:  #007bff;
                border-radius: 15px;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                
                margin-left: 10px; /* Space between text and sponge box */
                z-index: 1;
                padding: 20px;
            }
            .sponge-box img {
                width: 90%;
                height: auto;
                border-radius: 70%;
            }
            .sections-container {
                background: #007bff; /* Solid blue background for sections */
                padding: 20px;
                border-radius: 15px;
                margin: 20px;
                
            }
            .sections {
                display: flex;
                justify-content: space-around;
                color: black;
                padding: 20px;
            }
            .section {
                width: 28%; /* Adjusted width for the sections */
                background: white;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: left; /* Left-align text */
            }
            .section i {
                font-size: 3rem; /* Make icons bigger */
                color: #007bff;
                margin-bottom: 15px; /* Space between icon and text */
                display: block; /* Ensure icons are above text */
            }
            .section h3 {
                font-size: 1.5rem;
                font-weight: bold;
                color: #333;
                margin-bottom: 1rem;
            }
            .section p {
                font-size: 1rem;
                color: #555;
            }
            .contact-section {
                background: linear-gradient(to bottom, #007bff, #fff); /* Inverse blue gradient background */
                padding: 100px 0;
                text-align: center;
            }
            .contact-section h2 {
                color: black; /* White text for "GET IN TOUCH" */
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
            }
            .contact-section p {
                color: black;
                font-size: 1.25rem;
                margin-bottom: 2rem;
            }
            .contact-section .social-icons i {
                font-size: 2rem;
                color: black;
                margin: 0 10px;
            }
            .btn-primary {
                background-color: black; /* Black background for the magnifying glass */
                border:
            }
            .header-buttons {
                display: flex;
                gap: 10px;
            }
            .header .btn-book-now {
                background-color: blue;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 1.2rem;
                font-family: 'Bebas Neue', sans-serif;
                border-radius: 5px;
            }
            .header .btn-phone {
                background-color: yellow;
                color: blue;
                border: none;
                padding: 10px;
                font-size: 1.2rem;
                font-family: 'Bebas Neue', sans-serif;
                border-radius: 5px;
            }
            .btn-book-now {
    background-color: #007bff;
    color: white;
    font-size: 1rem;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
}

.btn-phone {
    background-color: #ffd700;
    color: #007bff;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    font-size: 1.5rem;
}


/* Existing styles */

.contact-section {
    background: linear-gradient(to bottom, #007bff, #fff); /* Inverse blue gradient background */
    padding: 100px 0;
    text-align: center;
}

.contact-section h2 {
    color: black; /* Black text for TOUCH" */
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.contact-section p {
    color: black;
    font-size: 1.25rem;
    margin-bottom: 2rem;
}

.contact-section .social-icons i {
    font-size: 2rem;
    color: black;
    margin: 0 10px;
}

.footer-content {
    display: flex;
    justify-content: space-around;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    margin-top: 50px;
}

.footer-section {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.footer-section img.footer-logo {
    width: 100px;
    margin-bottom: 10px;
    
}

.footer-section img.footer-yelp {
    width: 55px; /* Smaller size for Yelp logo (1/4 of 100px) */
    border-radius: 10px; /* Rounded edges for logos */
}

.footer-section p {
    margin: 5px 0;
    color: black;
    font-size: 1rem;
}


        </style>
    </head>
    <body>
        <div class="header">
        
            <img src="/static/logo.png" alt="Logo" class="img-fluid">
        </div>
        <div class="yellow-field">
            <div class="hero-text-container">
                <div class="hero-text">Cleaning Made Simple.</div>
                <div class="search-box">
                    <form action="/property" method="post" class="input-group">
                        <input type="text" id="address" name="address" class="form-control" placeholder="Enter an address and receive an estimate" required>
                        <div class="input-group-append">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="sponge-box">
                <img src="/static/sponge.png" alt="Sponge Image">
            </div>
        </div>
        <div class="sections-container">
            <div class="sections">
                <div class="section">
                    <i class="fas fa-calendar-alt"></i>
                    <h3>Standard Cleaning Service</h3>
                    <p>Our comprehensive cleaning service provides all the essential elements to maintain a clean and organized home. This package is ideal for weekly or bi-weekly touch-ups, ensuring that your home remains tidy and preventing clutter from accumulating.</p>
                </div>
                <div class="section">
                    <i class="fas fa-broom"></i>
                    <h3>Deep Cleaning Service</h3>
                    <p>Perfect for spring renewals or preparing for special events, our meticulous approach ensures a pristine sanctuary from floor to ceiling. Discover the transformative power of a deep clean designed to rejuvenate your space.</p>
                </div>
                <div class="section">
                    <i class="fas fa-box"></i>
                    <h3>Move-in/out Cleaning Service</h3>
                    <p>Transitioning homes can be overwhelming, but with our move-in/move-out cleaning service, you can easily focus on settling into your new chapter. Leave the cleaning to us – whether handing over the keys to the next occupant or stepping into your future residence, our team creates your fresh start.</p>
                </div>
            </div>
        </div>
       <div class="contact-section">
    <h2>Get In Touch</h2>
    <p>We proudly serve Richmond, VA.</p>
    <div class="social-icons">
        <a href="https://www.facebook.com/profile.php?id=61556378134570&mibextid=uzlsIk" target="_blank"><i class="fab fa-facebook"></i></a>
        <a href="https://www.instagram.com/wklycleaning?igsh=MWQ5Nzc3bzlmbXNodw%3D%3D&utm_source=qr" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="https://twitter.com/weeklycleaning" target="_blank"><i class="fab fa-twitter"></i></a>
        <a href="https://www.youtube.com/@WeeklyHomeCleaning" target="_blank"><i class="fab fa-youtube"></i></a>
        <a href="https://www.pinterest.com/weeklyhomecleaning/" target="_blank"><i class="fab fa-pinterest"></i></a>
        <a href="https://www.tiktok.com/@weeklyhomecleaning" target="_blank"><i class="fab fa-tiktok"></i></a>
        <a href="https://www.linkedin.com/company/weeklycleaning/" target="_blank"><i class="fab fa-linkedin"></i></a>
    </div>
    <div class="footer-content">
        <div class="footer-section">
            <img src="/static/bark.png" alt="Bark Professional" class="footer-logo">
            <p>Weekly Home Cleaning</p>
            <img src="/static/yelp.png" alt="Yelp" class="footer-logo footer-yelp">
        </div>
        <div class="footer-section">
            <p>Reviews</p>
            <p>Our Work</p>
            <p>Contact Us</p>
        </div>
        <div class="footer-section">
            <p>(804) 331-8472</p>
            <p>Email Us</p>
        </div>
    </div>
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
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #007bff;
                font-family: 'Bebas Neue', sans-serif;
            }}
            .container {{
                margin-top: 50px;
                background-color: #007bff;
                padding: 30px;
                border-radius: 10px;
                text-align: center;
            }}
            .header-img {{
                display: block;
                margin: 0 auto 20px auto;
                width: 200px; /* Adjust the size as needed */
            }}
            .quote-box {{
                width: 60%;
                background-color: white;
                color: black;
                padding: 30px;
                border-radius: 15px;
                border: 4px solid #B8860B; /* Darker gold color */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin: 0 auto 20px auto; /* Center the boxes and add space below */
            }}
            .quote-box h3 {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
                text-decoration: underline;
            }}
            .quote-box p {{
                font-size: 1rem;
                font-weight: normal; /* Make the paragraph text not bold */
                margin-bottom: 1rem;
            }}
            p {{
                font-size: 1.2rem;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            ul li {{
                font-size: 1.2rem;
                margin-bottom: 10px;
            }}
            .btn-secondary {{
                margin-top: 20px;
                font-size: 1.2rem;
            }}
            .contact-link {{
                color: blue;
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/static/logo.png" alt="Weekly Home Cleaning" class="header-img">
            <div class="quote-box">
                <h3>Pricing</h3>
                {pricing_info}
            </div>
            <div class="quote-box">
                <h3>Property Details</h3>
                <ul>
                    {stats_list}
                </ul>
                <p>If any of this information is incorrect, please <a href="https://www.weeklyhomecleaning.com/contact-us" class="contact-link">contact us</a></p>
            </div>
            <a href="/" class="btn btn-secondary">Go Back</a>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''
    return html_content





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
