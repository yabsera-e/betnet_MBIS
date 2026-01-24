# Rental House Marketplace

## Project Description

The Rental House Marketplace is a web application that serves as a platform for property owners, agents, and renters to connect and facilitate the rental process. The application allows property owners or agents to list available rental properties, and renters can search for properties, view details, and contact the property owner or agent to initiate the rental process.

## Key Features

1. **User Registration and Authentication**: Implement user registration and authentication functionality to allow property owners/agents and renters to create accounts and securely log in.

2. **Property Listing Creation**: Provide a form for property owners or agents to create listings for their rental properties. Include fields to capture relevant details such as property type, location, number of bedrooms/bathrooms, amenities, rental price, and availability dates.

3. **Property Search and Filtering**: Enable renters to search for rental properties based on location, price range, property type, and other relevant criteria. Implement filters to refine search results and sorting options to prioritize properties based on preferences (e.g., price, location).

4. **Property Detail View**: Display detailed information about each rental property, including property photos, description, amenities, contact information of the property owner or agent, and any additional details. Allow renters to save properties as favorites or add them to a shortlist for future reference.

5. **Messaging System**: Implement a messaging system that allows renters to contact property owners or agents directly to inquire about a property or initiate the rental process. Enable users to exchange messages within the application to facilitate communication.

6. **User Reviews and Ratings**: Provide a system for renters to leave reviews and ratings for the properties they have rented. Display these reviews and ratings to help other renters make informed decisions.

7. **Rental Application Process**: Allow renters to express interest in a property and submit rental applications. Implement a workflow for property owners or agents to review applications, conduct screenings, and communicate the rental decision to the renters.

8. **Responsive Design**: Ensure that the application is mobile-friendly and provides a seamless user experience across different devices.

9. **Error Handling and Validation**: Implement appropriate error handling and validation to ensure data integrity and provide feedback to users for any erroneous inputs.

🔗 **Live Preview:** [https://yba.onrender.com](https://yba.onrender.com)

## Setup instructions

**✅ Prerequisites**

- Python 3.10+
- PostgreSQL (or SQLite for dev)
- pipenv or virtualenv
- Docker & Docker Compose (optional)

---

1. **Clone the repository**

```bash
git clone https://github.com/natnael0024/rental_house_marketplace.git
cd rental_house_marketplace
```

2. **Create a virtual environment**
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```
pip install -r requirements.txt
```

4. **Create a .env file**
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

**💡 Use SQLite for quick setup:**

In settings.py, configure:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

5. **Run migrations and create a superuser**
```
python manage.py migrate
python manage.py createsuperuser
```

6. **Start the server**
```
python manage.py runserver
```

Now visit: http://127.0.0.1:8000


