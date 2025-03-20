import requests
import json
import sys

# API URL
API_URL = "https://www.googleapis.com/books/v1/volumes?q={search_term}"

# Define categories
categories = {
    "1": "fiction",
    "2": "science",
    "3": "Islam",
    "4": "education"
}

# User Data
favorites = []
user_books = []

def fetch_books(category):
    search_query = categories.get(category, "fiction")
    try:
        response = requests.get(API_URL.format(search_term=search_query), timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])[:5]
        else:
            print(f"Error {response.status_code}: Unable to fetch books.")
            return []
    except requests.exceptions.RequestException:
        print("Failed to fetch books. Please check your internet connection.")
        return []

def display_books(books):
    if not books:
        print("No books found.")
        return
    
    for i, book in enumerate(books, 1):
        info = book.get("volumeInfo", {})
        title = info.get("title", "No Title")
        authors = ", ".join(info.get("authors", ["Unknown"]))
        category = ", ".join(info.get("categories", ["No Category"]))
        print(f"{i}. {title} (by {authors}) [Category: {category}]")

def add_to_favorites(book):
    if book not in favorites:
        favorites.append(book)
        print(f"Added '{book['volumeInfo'].get('title', 'No Title')}' to favorites!")
    else:
        print("Book is already in favorites.")

def add_custom_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")
    if title and author and category:
        new_book = {
            "volumeInfo": {
                "title": title,
                "authors": [author],
                "categories": [category]
            }
        }
        user_books.append(new_book)
        print(f"Book '{title}' added successfully!")
    else:
        print("Please provide all details.")

def remove_book(book_list, book_title):
    for book in book_list:
        if book["volumeInfo"].get("title", "No Title").lower() == book_title.lower():
            book_list.remove(book)
            print(f"Removed '{book_title}'.")
            return
    print("Book not found.")

def main():
    while True:
        print("\n📚 Welcome to the CLI Book Library!")
        print("1. Search Books by Category")
        print("2. View Favorites")
        print("3. Add Custom Book")
        print("4. Remove a Book from Favorites")
        print("5. Remove a Custom Book")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Select a Category:")
            for key, value in categories.items():
                print(f"{key}. {value.capitalize()}")
            category_choice = input("Enter category number: ")
            books = fetch_books(category_choice)
            display_books(books)
            
            if books:
                fav_choice = input("Enter book number to add to favorites (or press Enter to skip): ")
                if fav_choice.isdigit():
                    book_index = int(fav_choice) - 1
                    if 0 <= book_index < len(books):
                        add_to_favorites(books[book_index])
                    else:
                        print("Invalid choice.")

        elif choice == "2":
            print("\n⭐ Favorite Books:")
            display_books(favorites)

        elif choice == "3":
            add_custom_book()

        elif choice == "4":
            title = input("Enter book title to remove from favorites: ")
            remove_book(favorites, title)

        elif choice == "5":
            title = input("Enter book title to remove from your collection: ")
            remove_book(user_books, title)

        elif choice == "6":
            print("Goodbye! Happy reading! 📖")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
