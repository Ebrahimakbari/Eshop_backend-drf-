# Eshop_django_backend with DRF and JWT

This is a Django project for an e-commerce website. The project includes the following features:

- User registration and login
- Product management
- Product comments
- Product views tracking
- Cart management
- Email verification
- Password reset

## Features

- User registration and login: Users can register and log in to the website using their email and password.
- Product management: Products can be added, edited, and deleted from the website.
- Product comments: Users can leave comments on products.
- Product views tracking: The number of views for each product is tracked.
- Cart management: Users can add products to their cart and checkout.
- Email verification: Users must verify their email address before they can log in.
- Password reset: Users can reset their password if they forget it.

## Installation

To install the project, follow these steps:

1. Clone the repository:
```
https://github.com/Ebrahimakbari/Eshop_backend.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Run the database migrations:
```
python manage.py migrate
```
4. Create a superuser:
```
python manage.py createsuperuser
```
5. Run the development server:
```
python manage.py runserver
```

## Docker:
1. 
   ```
   docker compose up --build
   ```
2. 
   ```
   docker compose run python manage.py migrate
   ```

## Usage

To use the project, follow these steps:

1. Log in to the website using your email and password.
2. Add products to your cart.
3. Checkout and complete your purchase.
4. Leave comments on products.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.
