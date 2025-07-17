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

## Setup instructions (using docker)
1. Ensure Docker is installed.

2. Build and run container
   docker build -t bookvault .
   docker run -p 8000:8000 bookvault

3. Access the app in your browser at:
   https://localhost:8000
   
## Project Structure

bookvault-capstone/
├── books/                  
├── docs/                   
├── media/                  
├── templates/              
├── Dockerfile              
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
