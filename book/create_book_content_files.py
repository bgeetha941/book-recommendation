import os
import pandas as pd

# Load the dataset
df = pd.read_csv("books.csv", on_bad_lines='skip')

# Directory where content will be stored
base_dir = "static/books"

# Make sure the base directory exists
os.makedirs(base_dir, exist_ok=True)

# Loop through each row in the dataset
for index, row in df.iterrows():
    isbn = str(row['isbn']).strip()
    
    if pd.notnull(isbn) and isbn != '':
        # Create directory for this ISBN
        book_dir = os.path.join(base_dir, isbn)
        os.makedirs(book_dir, exist_ok=True)
        
        # Create content.txt with dummy content
        content_path = os.path.join(book_dir, "content.txt")
        with open(content_path, "w", encoding='utf-8') as f:
            f.write(f"This is a sample preview of the book titled '{row['title']}' by {row['authors']}.\n\n")
            f.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus.\n")
            f.write("Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.\n")

print("✅ All content.txt files generated successfully!")
