# Airport API Service 

The Airport API Service is a Django REST framework-based project designed to track flights from airports worldwide. This API allows you to retrieve information about airports, airplanes, flights, routes and crew members, making it a valuable tool for managing and analyzing flight data. Registered user can make an order for few or more flight tickets.

## Features

* Role information: Give information about roles of crew members.

* Crew information: Retrive details about full name and role of crew member.

* Country information: Give list of countries' names 

* Airport Information: Retrieve details about airports worldwide, including their names, closest big city and country. List of airport can be filtered using id of country.

* Route Information: Provide information about different routes which includes source and destination airports name, and distance between them.

* Airplane Type information: Give list of airplane type's names

* Airplane Information: Retrieve information about airplane's name and type, number of rows for passangers and number of seats in every row. List of airplanes can be filtered with the field "name".

* Flight Information: Get information about flights, including route, departure and arrival times, crew and aircraft details, as well as information about number of available seats. List of flights can be filtered using id of route. 

* Order Information: Give possibility to check his/her orders for authenticated user. 

* Ticket Information: Allow to add to order tickets for the flight with mentioning specific row and seat number. 

* Authentication: User can create profile entering email and password. API is secured with JWT (JSON Web Tokens) authentication to protect sensitive flight data. 

## Getting Started
### Prerequisites
Before you begin, ensure you have met the following requirements:

- **Python**: Make sure you have Python 3.x installed on your system.

- **Pip**: Pip should be installed. Pip is a package manager for Python. You can check if you have it installed by running pip --version.

### Installation
Clone the repository:

```shell
git clone https://github.com/OksanaAdamchuk/airport-api-service.git
cd airport-api-service
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

- Create a .env file in the project root directory and set your configuration variables

- Migrate the database:
```shell
python manage.py migrate
```

- Create a superuser account:
```shell
python manage.py createsuperuser
```

- Start the development server:
```shell
python manage.py runserver
```
The API should now be accessible at http://localhost:8000/.

## Usage
### Authentication
To access certain endpoints, you need to authenticate your requests using JWT (JSON Web Tokens). You can obtain a token by registering a user account through the Django API and use the token endpoint to obtain a token.

To authenticate, include the obtained token in your request headers with the format:

```makefile
Authorization: Bearer <your-token>
```

### API Documentation
You can interact with the API using Swagger, a user-friendly API documentation tool. To access Swagger, open a web browser and navigate to http://localhost:8000/api/schema/swagger/. Here, you will find detailed information about the available endpoints and how to use them.

### Endpoints
The API provides the following endpoints:

* Airplane Types
  - GET /api/airport/airplane-types/: List all airplane types.
  - POST /api/airport/airplane-types/: Create a new airplane type (admin authentication required).
  - GET /api/airport/airplane-types/{id}/: Retrieve details of a specific airplane type.
  - PUT /api/airport/airplane-types/{id}/: Update an airplane's type information (admin authentication required).
  - PATCH /api/airport/airplane-types/{id}/: Partially update an airplane's type information (admin authentication required).
  - DELETE /api/airport/airplane-types/{id}/: Delete airplane type (admin authentication required).
* Airplanes:
  - GET /api/airport/airplanes/: List all airplanes. 
  - POST /api/airport/airplanes/: Create a new airplane (admin authentication required).
  - GET /api/airport/airplanes/{id}/: Retrieve details of a specific airplane.
  - PUT /api/airport/airplanes/{id}/: Update an airplane's information (admin authentication required).
  - PATCH /api/airport/airplanes/{id}/: Partially update an airplane's information (admin authentication required).
  - DELETE /api/airport/airplanes/{id}/: Delete airplane (admin authentication required).
* Airports:
  - GET /api/airport/airports/: List all airports. 
  - POST /api/airport/airports/: Create a new airport (admin authentication required).
  - GET /api/airport/airports/{id}/: Retrieve details of a specific airport.
  - PUT /api/airport/airports/{id}/: Update an airport's information (admin authentication required).
  - PATCH /api/airport/airports/{id}/: Partially update an airport's information (admin authentication required).
  - DELETE /api/airport/airports/{id}/: Delete airport (admin authentication required).
* Countries:
  - GET /api/airport/countries/: List all countries. 
  - POST /api/airport/countries/: Create a new country (admin authentication required).
  - GET /api/airport/countries/{id}/: Retrieve details of a specific country.
  - PUT /api/airport/countries/{id}/: Update an country's information (admin authentication required).
  - PATCH /api/airport/countries/{id}/: Partially update an country's information (admin authentication required).
  - DELETE /api/airport/countries/{id}/: Delete country (admin authentication required).
* Crews:
  - GET /api/airport/crews/: List all crews. 
  - POST /api/airport/crews/: Create a new crew member (admin authentication required).
  - GET /api/airport/crews/{id}/: Retrieve details of a specific crew member.
  - PUT /api/airport/crews/{id}/: Update an crew's member information (admin authentication required).
  - PATCH /api/airport/crews/{id}/: Partially update an crew's member information (admin authentication required).
  - DELETE /api/airport/crews/{id}/: Delete crew member (admin authentication required).
* Flights:
  - GET /api/airport/flights/: List all flights. 
  - POST /api/airport/flights/: Create a new flight (admin authentication required).
  - GET /api/airport/flights/{id}/: Retrieve details of a specific flight.
  - PUT /api/airport/flights/{id}/: Update an flight's information (admin authentication required).
  - PATCH /api/airport/flights/{id}/: Partially update an flight's information (admin authentication required).
  - DELETE /api/airport/flights/{id}/: Delete flight (admin authentication required).
* Orders:
  - GET /api/airport/orders/: List all orders  with tickets that belong to them (authentication required). 
  - POST /api/airport/orders/: Create a new order (authentication required).
  - GET /api/airport/orders/{id}/: Retrieve details of a specific order (authentication required).
* Roles:
  - GET /api/airport/roles/: List all roles. 
  - POST /api/airport/roles/: Create a new role (admin authentication required).
  - GET /api/airport/roles/{id}/: Retrieve details of a specific role.
  - PUT /api/airport/roles/{id}/: Update an role's information (admin authentication required).
  - PATCH /api/airport/roles/{id}/: Partially update an role's information (admin authentication required).
  - DELETE /api/airport/roles/{id}/: Delete role (admin authentication required).
* Routes:
  - GET /api/airport/routes/: List all routes. 
  - POST /api/airport/routes/: Create a new route (admin authentication required).
  - GET /api/airport/routes/{id}/: Retrieve details of a specific route.
  - PUT /api/airport/routes/{id}/: Update an route's information (admin authentication required).
  - PATCH /api/airport/routes/{id}/: Partially update an route's information (admin authentication required).
  - DELETE /api/airport/routes/{id}/: Delete route (admin authentication required).
* User:
  - POST /api/user/create/: Create new user.
  - GET /api/user/me/: Retrieve details of logined user (authentication required).
  - PUT /api/user/me/: Update details of logined user (authentication required).
  - PATCH /api/user/me/: Partially update details of logined user (authentication required).
  - POST /api/user/token/: Retrieve access and refresh tokens for specific user.
  - POST /api/user/token/refresh/: Receive new access token passing refresh token in the body.
  - POST /api/user/token/verify/: Verify validity of token.

