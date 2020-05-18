# How Are You API

- [How Are You API](#how-are-you-api)
- [Preamble](#preamble)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
- [Running the API](#running-the-api)
- [API Overview](#api-overview)
- [Result Types](#result-types)
  - [Singletons](#singletons)
  - [Lists](#lists)
  - [Null](#null)
  - [Boolean](#boolean)
- [Resource Components](#resource-components)
  - [Address](#address)
  - [Answer](#answer)
  - [Question](#question)
  - [Email Log](#email-log)
  - [Auth](#auth)
- [Authorization](#authorization)
- [Documentation](#documentation)
- [Testing](#testing)

# Preamble
This is a web service API that sends daily emails, that answer pre-defined questions like "How are you?", "How was your day?", "Have you eaten?", to persons who make a point of asking these questions every day.

This codebase was built to test out [FastAPI](https://github.com/tiangolo/fastapi) and see what the hype is about. I am quite impressed.

This codebase was built with the [FastAPI](https://github.com/tiangolo/fastapi) framework and Redis.

# Requirements
- Python.
- Docker.

# Getting Started
1. Install the tools in the "Requirements" section.
2. Create a virtual environment and activate it.
3. Clone this repository.
   ```
   git clone https://github.com/Overrideveloper/HowAreYouAPI.git
   ```
4. Navigate to the cloned repository's directory.
   ```
   cd HowAreYouAPI
   ```
5. Install the packages used in the codebase.
   ```
   pip install -r requirements.txt
   ```
6. Use the `.env` and `.test.env` templates to create `.local.env` and `.local.test.env` files
7. Add correct values to the `.local.env` and `.local.test.env` files.

# Running the API
  ```
  docker-compose up
  ```
  This will start the server on port `8000` and the redis service on `6379`. 

# API Overview
The API is RESTful and returns results in JSON. The API responses use standard HTTP status codes and the results have this general format:

*GET /resource **Success***
```
{
    "data": "A list of resource(s)"
    "code": "The HTTP status code. Usually 200",
    "message": "Short user-friendly message describing the response"
}
```

*GET /resource/{id} **Success***
```
{
    "data": "A single resource in the form of a dictionary."
    "code": "The HTTP status code. Usually 200",
    "message": "Short user-friendly message describing the response"
}
```

*POST /resource **Success***
```
{
    "data": "The created resource in the form of a dictionary."
    "code": "The HTTP status code. Usually 201",
    "message": "Short user-friendly message describing the response"
}
```

*PUT /resource/{id} **Success***
```
{
    "data": "The modified resource in the form of a dictionary"
    "code": "The HTTP status code. Usually 200",
    "message": "Short user-friendly message describing the response"
}
```

*DELETE /resource/{id} **Success***
```
{
    "data": null
    "code": "The HTTP status code. Usually 200",
    "message": "Short user-friendly message describing the response"
}
```

**Error**
```
{
    "data": "Relevant information about the error. Usually a list of info or null, if there is no info about the error",
    "code": "The HTTP status code. The codebase uses the 404, 400, 401 and 403 error codes"
    "message": "Short user-friendly message describing the error.
}
```

**Failure** - (This is the framework default and is rarely used by the codebase)
```
{
    "detail": "Relevant information about the failure. Usually a string"
}
```

The `data` key is the most important part of the response. It can be a dictionary, a list, a boolean or null, depending on the nature of the request made. In the event of an error, it is usually a list of key-value pairs (dictionaries) containing information about the error, or null if no such information is provided.

The `code` key is a copy of the HTTP status code of the response.

The `message` key is a short user-friendly message that describes the response. This can be used in alerts, notifications, etc.

# Result Types
All results are returned in JSON. There are four general types of results
- Singletons
- Lists
- Null
- Boolean

## Singletons
Singletons are single results, in the form of a dictionary. This is a typical result when querying a single resource.

## Lists
List results contain multiple resource entries.

## Null
Null results are typical with errors or requests that don't return a resource, for example DELETE requests

## Boolean
Some requests return **true** or **false**

# Resource Components
The major resource components in this API are:
- Address
- Answer
- Email Log
- Question
- Auth

> Information on detailed documentation on resources can be found [here](#documentation).

## Address
An email address and a name to send answers to.

The address resource component can be used like this:
| Route                    | Description                       |
|--------------------------|-----------------------------------|
| GET /api/address         | Returns a list of all addresses   |
| GET /api/address/{id}    | Returns a single address          |
| POST /api/address        | Creates and returns a new address |
| PUT /api/address/{id}    | Modifies and returns an address   |
| DELETE /api/address/{id} | Deletes an address                |

## Answer
An answer to a predefined question.

The answer resource component can be used like this:
| Route                    | Description                       |
|--------------------------|-----------------------------------|
| GET /api/answer         | Returns a list of all answers   |
| GET /api/answer/{id}    | Returns a single answer          |
| POST /api/answer        | Creates and returns a new answer |
| PUT /api/answer/{id}    | Modifies and returns an answer   |
| DELETE /api/answer/{id} | Deletes an answer                |

## Question
A [predefined] question.

The question resource component can be used like this:
| Route                    | Description                       |
|--------------------------|-----------------------------------|
| GET /api/question         | Returns a list of all questions   |
| GET /api/question/{id}    | Returns a single question          |
| POST /api/question        | Creates and returns a new question |
| PUT /api/question/{id}    | Modifies and returns a question   |
| DELETE /api/question/{id} | Deletes a question                |

## Email Log
A log that records if the answer emails for a particular day have been sent and how many emails were sent.

The email log resource component can be used like this:
| Route                       | Description                       |
|-----------------------------|-----------------------------------|
| GET /api/log/today          | Returns the email log for the current day   |

## Auth
This resource deals with authentication.

> *Note: The API is designed to be a one-user system. That means there can only be one existing user at a time.*

The auth resource component can be used like this:
| Route                              | Description                                                                  |
|------------------------------------|------------------------------------------------------------------------------|
| GET /api/auth/status               | Returns a boolean indicating if a user exists                                |
| POST /api/auth/signup              | Creates a user and returns an auth token and the user data                   |
| POST /api/auth/login               | Logs in a user and returns an auth token                                     |
| PUT /api/auth/change-password/{id} | Modifies a user's password                                                   |
| POST /api/auth/reset-password      | Resets a user's password and sends an email with the auto-generated password |

# Authorization
The API is designed to be a one-user system. That means there can only be one existing user at a time.

Most of the API requests require authorization and will return a `HTTP 401` error when authorization is not provided.

To authorize an API request:
1. Login or signup as a user and get an authorization token.
2. Authorize the request by passing the token in the `Authorization` header.
   ```
   curl --header "Authorization: Bearer <TOKEN>" http://<YOUR-MACHINE-IP>:8000/api/address
   ```

# Documentation
Detailed documentations of the API endpoints, request parameters, request and response schemas are available at `http://<YOUR-MACHINE-IP>:8000/docs` and `http://<YOUR-MACHINE-IP>:8000/redoc`.

These documentations are powered by OpenAPI, Swagger and ReDoc.

# Testing
The API has unit and integration tests.

The unit tests can be found in the `tests/unit` directory.
The integration tests can be found in the `tests/integration` directory.

To run the tests:
1. Start the redis service (for integration tests).
   ```
   docker-compose -f docker-compose.redis.yml up
   ```
2. Run the tests
   ```
   python tests
   ```
