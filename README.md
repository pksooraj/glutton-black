# Black T-shirt Designer Shop

This is a Django e-commerce application for designing and purchasing custom black t-shirts.

## Project Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Create a virtual environment** (recommended)

   ```
   python -m venv venv
   ```

2. **Activate the virtual environment**

   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install required packages**

   ```
   pip install django pillow
   ```

### Database Setup

1. **Apply migrations**

   ```
   python manage.py migrate
   ```

2. **Create a superuser** (for admin access)

   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

### Running the Development Server

1. **Start the server**

   ```
   python manage.py runserver
   ```

2. **Access the website**

   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Adding Sample Data

1. **Log in to the admin panel** using your superuser credentials

2. **Add products**:
   - Navigate to Products > Add Product
   - Fill in the details (name, price, description)
   - Upload product images
   - Mark featured products as needed

3. **Add testimonials** (if applicable):
   - Navigate to Testimonials > Add Testimonial
   - Add customer reviews to display on the site

## Project Structure

- **shop_products**: Product catalog management
- **shop_customization**: T-shirt customization features
- **shop_cart**: Shopping cart functionality
- **shop_orders**: Order processing and history
- **shop_testimonials**: Customer reviews and testimonials
- **core**: Core website functionality

## Features

- Product browsing and filtering
- T-shirt customization
- Shopping cart management
- Checkout process
- Order history and tracking
- User authentication