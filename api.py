# https://www.googleapis.com/books/v1/volumes?q={search_term}

import requests

# Define the API URL
API_URL = "https://www.googleapis.com/books/v1/volumes?q={search_term}"

# response =requests.get("https://www.googleapis.com/books/v1/volumes?q={search_term}")
# print(response.status_code)
# print(response.json())

# # Search query (You can change this)
# search_query = "fiction"

# # Make a GET request to the API
# response = requests.get(f"{API_URL}?q={search_query}")

# # Check if request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()  # Convert response to JSON
#     books = data.get("items", [])  # Extract book items

#     # Loop through first 5 books and display their titles
#     for book in books[:5]:
#         title = book["volumeInfo"].get("title", "No Title")
#         authors = book["volumeInfo"].get("authors", ["Unknown"])
#         print(f"📖 {title} by {', '.join(authors)}")
# else:
#     print("❌ Error fetching book data.")
