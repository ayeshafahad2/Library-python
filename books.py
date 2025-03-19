import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="📚 Book Explorer", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background-color: #FFDAB9;
        }
        [data-testid="stSidebar"] {
            background-color: #D2B48C;
        }
        .stButton > button {
            background-color: #8B4513 !important;
            color: white !important;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# API URL
API_URL = "https://www.googleapis.com/books/v1/volumes?q={search_term}"

# Define categories
categories = {
    "📖 Fiction": "fiction",
    "🔬 Science & Technology": "science",
    "🕌 Islamic Books": "Islam",
    "🎓 Knowledge & Learning": "education"
}

# Initialize session state for favorites and user-added books
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "user_books" not in st.session_state:
    st.session_state.user_books = []

# Function to fetch books
def fetch_books(category):
    search_query = categories.get(category, "fiction")
    response = requests.get(API_URL.format(search_term=search_query))
    if response.status_code == 200:
        data = response.json()
        return data.get("items", [])[:5]
    st.error("Failed to fetch books. Please try again later.")
    return []

# Function to add a book to favorites
def add_to_favorites(book):
    if book not in st.session_state.favorites:
        st.session_state.favorites.append(book)
        st.success(f"✅ '{book['volumeInfo'].get('title', 'No Title')}' added to favorites!")

# Function to remove a book from favorites
def remove_from_favorites(book):
    if book in st.session_state.favorites:
        st.session_state.favorites.remove(book)
        st.warning(f"❌ '{book['volumeInfo'].get('title', 'No Title')}' removed from favorites.")

# Function to add a custom book
def add_custom_book(title, author, category, image_url):
    if title and author and category:
        new_book = {
            "volumeInfo": {
                "title": title,
                "authors": [author],
                "categories": [category],
                "imageLinks": {"thumbnail": image_url if image_url else "https://via.placeholder.com/128x195.png?text=No+Image"},
            }
        }
        st.session_state.user_books.append(new_book)
        st.success(f"✅ '{title}' added to the list!")
    else:
        st.error("⚠️ Please provide Title, Author, and Category.")

# Function to remove a custom book
def remove_custom_book(book):
    if book in st.session_state.user_books:
        st.session_state.user_books.remove(book)
        st.warning(f"❌ '{book['volumeInfo']['title']}' removed from your list.")

# Title
st.title("📚 Book Explorer")

# Sidebar for category selection
category_name = st.sidebar.selectbox("📂 Choose a Category:", list(categories.keys()))

# Fetch books based on selection
books = fetch_books(category_name)

# Display books in a grid
st.subheader(f"🔍 Books in {category_name}")
col1, col2 = st.columns(2)
for index, book in enumerate(books):
    info = book.get("volumeInfo", {})
    title = info.get("title", "No Title")
    authors = info.get("authors", ["Unknown"])
    category = info.get("categories", ["No Category"])
    thumbnail = info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/128x195.png?text=No+Image")
    preview_link = info.get("previewLink", "#")

    with col1 if index % 2 == 0 else col2:
        st.image(thumbnail, width=120)
        st.write(f"**📖 {title}**")
        st.write(f"👨‍💼 **Authors:** {', '.join(authors)}")
        st.write(f"📂 **Category:** {', '.join(category)}")
        st.markdown(f"[🔗 Preview Book]({preview_link})", unsafe_allow_html=True)

        if st.button(f"⭐ Add to Favorites {index+1}", key=f"add_{index}"):
            add_to_favorites(book)

# User-Added Books Section
st.subheader("📝 Add Your Own Book")
with st.form("add_book_form"):
    title = st.text_input("📖 Book Title")
    author = st.text_input("👨‍💼 Author")
    category = st.text_input("📂 Category")
    image_url = st.text_input("🖼️ Image URL (Optional)")

    if st.form_submit_button("➕ Add Book"):
        add_custom_book(title, author, category, image_url)

# Display user-added books
if st.session_state.user_books:
    st.subheader("📚 Your Added Books")
    col1, col2 = st.columns(2)
    for index, book in enumerate(st.session_state.user_books):
        info = book.get("volumeInfo", {})
        title = info.get("title", "No Title")
        authors = info.get("authors", ["Unknown"])
        category = info.get("categories", ["No Category"])
        thumbnail = info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/128x195.png?text=No+Image")

        with col1 if index % 2 == 0 else col2:
            st.image(thumbnail, width=120)
            st.write(f"**📖 {title}**")
            st.write(f"👨‍💼 **Authors:** {', '.join(authors)}")
            st.write(f"📂 **Category:** {', '.join(category)}")

            if st.button(f"❌ Remove '{title}'", key=f"remove_user_{index}"):
                remove_custom_book(book)

# Favorites Section
st.sidebar.subheader("⭐ My Favorite Books")
if st.session_state.favorites:
    for book in st.session_state.favorites:
        info = book.get("volumeInfo", {})
        title = info.get("title", "No Title")
        authors = info.get("authors", ["Unknown"])
        thumbnail = info.get("imageLinks", {}).get("thumbnail", "https://via.placeholder.com/128x195.png?text=No+Image")
        preview_link = info.get("previewLink", "#")

        with st.sidebar:
            st.image(thumbnail, width=80)
            st.write(f"**📖 {title}**")
            st.write(f"👨‍💼 **Authors:** {', '.join(authors)}")
            st.markdown(f"[🔗 Preview Book]({preview_link})", unsafe_allow_html=True)
            if st.button(f"❌ Remove '{title}'", key=f"remove_fav_{title}"):
                remove_from_favorites(book)
else:
    st.sidebar.write("😢 No favorites yet.")