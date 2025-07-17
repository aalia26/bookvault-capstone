# bookvault-capstone

**BookVault** is a Django-based online bookstore where users can browse books, view upcoming releases, leave reviews, and manage their shopping cart. This project was created as part of the Capstone Consolidation Task for HyperionDev's Web Development Bootcamp.

---

## Features

-  View all books and upcoming releases
-  Search books by title or author
-  Add reviews (for logged-in users)
-  Cart functionality (add/remove items)
-  User authentication (register/login/logout)
-  Admin panel for managing content

---

## Setup Instructions (Using `venv`)

1. **Clone the repository**:
   git clone https://github.com/aalia26/bookvault-capstone.git
   cd bookvault-capstone
   
2. **Create and activate a virtual enviroment**:
   python -m venv venv
   venv\Scripts\activate # Windows
   source venv/bin/activate # macOS

3. **Install independencies**:
   pip install -r requirements.txt

4. **Run migrations**:
   python manage.py migrate

5. **Run the developement server**:
   python manage.py runserver

## Project Structure

bookvault-capstone/
├── books/                  # Django app with models, views, templates
├── docs/                   # Sphinx-generated documentation
├── media/                  # Uploaded images (ignored by Git)
├── templates/              # Shared base and auth templates
├── Dockerfile              # Docker container definition
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore

## Security

This project does not include sensitive data like passwords or tokens.
If required, create a .env file locally and store credentials there.
The .env file and other private files are excluded via .gitignore.

## Author
Aalia Malek - Software Engineerings Bootcamp Student at HyperionDev
