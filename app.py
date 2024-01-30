from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import openpyxl

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # Prompt the user for the items they want to search for
    searchItems = request.args.get('searchItems')

    # Replace this URL with the Amazon sg webpage you want to scrape
    url = f"https://www.amazon.sg/s?k={searchItems.replace(' ', '+')}"

    # Send an HTTP request to the webpage and get the HTML content
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the divs with the specified class name
    divs = soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-expand-height puis-include-content-margin puis puis-vmsrh7ksw1p6r26mpgmpvetbls s-latency-cf-section puis-card-border")
    print(f"Number of divs found: {len(divs)}")

    # Create a list to store the results
    results = []

    # Loop through the divs and extract the product information
    for div in divs:
        try:
            # Try to find the product name
            productName = div.find("span", class_="a-size-base-plus a-color-base a-text-normal").text.strip()
            print(f"Product Name: {productName}")
        except AttributeError:
            productName = "Name Unavailable"

        try:
            # Try to find the product price
            productPrice = div.find("span", class_="a-offscreen").text.strip()
            print(f"Product Price: {productPrice}")
        except AttributeError:
            productPrice = "Price Unavailable"

        try:
            # Try to find the product link
            productLink = div.find("a", class_="a-link-normal")["href"]
            print(f"Product Link: {productLink}")
        except AttributeError:
            productLink = "Link Unavailable"

        # Add 'www.Amazon.sg' infront of each link
        productLink = f"www.Amazon.sg{productLink}"

        # Append the product information to the results list
        results.append({"productName": productName, "productPrice": productPrice, "productLink": productLink})

    # Return the results in JSON format
    print(f"Number of results found: {len(results)}")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)