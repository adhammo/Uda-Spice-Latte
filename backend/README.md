# Coffee Shop API

## About

**Coffee Shop API** is used as the back-end for **Uda-Spice Latte** full-stack web application.

**Uda-Spice Latte** front-end uses **Coffee Shop API** to retrieve, store, and manipulate drinks in the cafe.

## Getting Started

### Create Coffee Shop Database

Create a database called **"coffee_shop"** which will be used by the API to store drinks data.

Open up a new shell terminal and type in the following commands:

1. Follow this guide to [Install PostgreSQL](https://www.postgresqltutorial.com/install-postgresql/) on your machine
2. Follow this guide to [Start PostgreSQL service](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html) on your machine
3. Create a new database called **"coffee_shop"**
    ```bash
    dropdb coffee_shop && createdb coffee_shop
    ```

### Setup Virtual Environment (Optional)

Follow this guide to [Setup a Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) and **activate** it then continue following the next steps using virtual env.

```bash
pip install virtualenv
virtualenv env
```

##### Activation:

```bash
# Windows
	env\Scripts\activate
# Mac OS / Linux:
	source env/bin/activate
```

### Install Dependencies

Install all required packages:

```bash
cd backend
pip install -r requirements.txt
```

# Test API

1. Run flask server
2. Import and run "coffee_shop_postman" [Postman](https://www.postman.com/) collection.

# Set Flask App

Set flask app to coffee_shop and environment to development (debug).

```bash
# Windows
cd backend
set FLASK_APP=coffee_shop
set FLASK_ENV=development

# Mac OS / Linux
cd backend
export FLASK_APP=coffee_shop
export FLASK_ENV=development
```

### Migrate Database Schema

Initialize and upgrade a migration for **coffee_shop** database to create the tables necessary for the API to function correctly:

```bash
cd backend
flask db init
flask db migrate
flask db upgrade
```

### Add Template Data

Here are some data to insert into your drinks table to simulate real data.

**Drinks:**

```sql
INSERT INTO drinks(title, recipe)
VALUES
	(
		'matcha shake',
		'[{"name": "milk", "color": "grey", "parts": 1}, {"name": "matcha", "color": "green", "parts": 3}]'
	),
	(
		'flatwhite',
		'[{"name": "milk", "color": "grey", "parts": 3}, {"name": "coffee", "color": "brown", "parts": 1}]'
	),
	(
		'cap',
		'[{"name": "foam", "color": "white", "parts": 1}, {"name": "milk", "color": "grey", "parts": 2}, {"name": "coffee", "color": "brown", "parts": 1}]'
	);
```

### Run Flask Application

Follow this guide [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/) to know more ways to run a flask app.

```bash
flask run
```

## Introduction

**Coffee Shop API** is designed to run locally on your machine.

Invoke the following endpoint to interact with **Coffee Shop API**:

```http
Endpoint: http://localhost:5000/
```

### Schema

**Coffee Shop API** has two main objects; a Drink and an Ingredient.

**Ingredient Schema:**

```python
{
    "color": str,
    "parts": int
}
```

**Ingredient-Detailed Schema:**

```python
{
    "name": str,
    "color": str,
    "parts": int
}
```

**Drink Schema:**

```python
{
    "id": int,
    "title": str,
    "recipe": [
		(Ingredient Schema),
		(Ingredient Schema),
		...
	]
}
```

**Drink-Detailed Schema:**

```python
{
    "id": int,
    "title": str,
    "recipe": [
		(Ingredient-Detailed Schema),
		(Ingredient-Detailed Schema),
		...
	]
}
```

### Error Handling

If **Coffee Shop API** couldn't fulfill the request because an error has occurred for any reason it will respond with an error status and with the next standardized message:

```python
{
    "error": int, 		# status code
    "message": str, 		# brief error message
    "description": str, 	# detailed error message
    "success": False
}
```

## Drinks

### Get All Drinks

Retrieves all drinks from **coffee_shop** database.

**Request**

```http
GET /drinks
Host: localhost:5000
```

**Response**

```python
{
	"drinks": [
		(Drink Schema),
		(Drink Schema),
		...
	],
	"success": True
}
```

**Permissions**

```bash
no permissions needed
```

### Get Detailed Drinks

Retrieves all drinks in detail from **coffee_shop** database.

**Request**

```http
GET /drinks-detail
Host: localhost:5000
```

**Response**

```python
{
	"drinks": [
		(Drink-Detailed Schema),
		(Drink-Detailed Schema),
		...
	],
	"success": True
}
```

**Permissions**

```bash
get:drinks-detail
```

### Create a Drink

Creates a new drink in **coffee_shop** database.

**Request**

```http
POST /drinks
Host: localhost:5000
```

with body:

```python
{
    "title": str,
    "recipe": [
		(Ingredient-Detailed Schema),
		(Ingredient-Detailed Schema),
		...
	]
}
```

> Note: all fields are required.

**Response**
Returns the drink that was just created.

```python
{
	"drinks": [
		(Drink-Detailed Schema)
	]
	"success": True
}
```

**Permissions**

```bash
post:drinks
```

### Edit a Drink

Edits **some** values of a drink in **coffee_shop** database.

**Request**

```http
PATCH /drinks/<int:drink_id>
Host: localhost:5000
```

with body:

```python
{
    "title": str,
    "recipe": [
		(Ingredient-Detailed Schema),
		(Ingredient-Detailed Schema),
		...
	]
}
```

> Note: at least one field is required.

**Response**
Returns the drink that was just edited.

```python
{
	"drinks": [
		(Drink-Detailed Schema)
	]
	"success": True
}
```

**Permissions**

```bash
patch:drinks
```

### Delete a Drink

Delete a drink from **coffee_shop** database.

**Request**

```http
DELETE /drinks/<int:drink_id>
Host: localhost:5000
```

**Response**
Returns the drink that was just deleted.

```python
{
	"drinks": [
		(Drink-Detailed Schema)
	]
	"success": True
}
```

**Permissions**

```bash
delete:drinks
```
