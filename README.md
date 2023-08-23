# Wallet Transactions Web API

This Web API handles user sign in and sign up, wallet creation and transfers between wallets.

## Table of Contents

- Project Overview
- Features
- Getting Started
    - Prerequisites
    - Installation
    - Configuration
- Usage
    - API Endpoints
- Authentication and Authorization
- Testing
- License
- Acknowledgements

## Project Overview

The project allows one to create wallets and provide transactions between them.

## Features
- Transactions are available only for wallets with the same currency;
- When a user sends money from their wallet to another of their wallets - no commission is applied;
- When they send money to a wallet related to another user - a commission of 10% is applied;
- Users can't create more than 5 wallets.

## Getting Started

Prerequisites:

All package dependencies are listed in `pyproject.toml` file, so one needs only poetry in order to install everything.

- Python 3.10+
- Django 4.2.4+
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.2.2
- python-decouple 3.8

Installation:

1. Clone the repository via `git clone https://github.com/chedug/Wallet`
2. Create and set up virtual environment (Optional)
3. Install dependencies using Poetry (or manually)

Configuration:

1. Change database credentials in `settings.py` using environment variables (include appropriate variables in .env file)


## Usage

How to create wallets:

**POST** `/wallets`
```json
{
 "type": "visa",
 "currency": "GBP"
}
```

Get all user's wallets: Example:
**GET** `/wallets`
```json
{
[
"id": "1",
"name": "ER15096L",
"type": "Visa",
"currency": "USD",
"balance": "1.87",
"created_on": ...,
"modified_on": ...
],
[
"id": "2",
"name": "VB07N96L",
"type": "Visa",
"currency": "GBP",
"balance": "1000.50",
"created_on": ...,
"modified_on": ...
]
}
```

**GET** `/wallets/<name>` - get wallet where name=`<name>`. Example - `/wallets/VB07N96L`

**DELETE** `/wallets/<name>` - delete wallet

**POST** `/wallets/transactions/` - create new transaction. Example:
```json
{
"sender": "VB07N96L",
"receiver": "MJYR096L",
"transfer_amount": "100.00"
}
```
**GET** `/wallets/transactions/` - get all transactions for current user. Example:
```json
{
[
"id": 1,
"sender": "VB07N96L",
"receiver": "MJYR096L",
"transfer_amount": "100.00",
"commission": "0.00",
"status": "PAID",
"timestamp": ...
],
...
}
```

**GET** `/wallets/transactions/<transaction_id>` - get transaction
**GET** `/wallets/transactions/<wallet_name>` - get all transactions where wallet was sender or receiver

## Authentication and Authorization

The projects implements *JSON Web Token*-based authentication,

You can obtain authentication token by **POST** `/api-auth/login/` and entering user credentials,

and refresh token by **POST** `/api-auth/login/refresh`, by providing refresh token.

The duration of the JWT access token is 30 minutes, and of the refresh token – 1 day.

#### Permissions:

All endpoints, except the authorization ones, require user to be authenticated by `IsAuthenticated` permission.
Other custom permissions can be found in `permissions.py` file.


| Endpoint                                         | Permissions                                                                         |
|--------------------------------------------------|-------------------------------------------------------------------------------------|
| **GET**  `/wallets`                              | `IsAuthenticated`                                                                   |
| **POST** `/wallets`                              | `IsAuthenticated`                                                                   |
| **GET** `/wallets/<name>`                        | Must be an owner of the wallet (`IsAuthenticated`, `IsOwner`)                       |
| **DELETE** `/wallets/<name>`                     | Must be an owner of the wallet (`IsAuthenticated`, `IsOwner`)                       |
| **POST** `/wallets/transactions/`                | Must be an owner of the sender wallet (`IsAuthenticated`, `IsSenderOwner`)          |
| **GET** `/wallets/transactions/`                 | Authorized (`IsAuthenticated`)                                                      |
| **GET** `/wallets/transactions/<transaction_id>` | Must be an owner of the sender wallet (`IsAuthenticated`, `IsSenderOwner`)          |
| **GET** `/wallets/transactions/<wallet_name>`    | Either sender or receiver wallet should be of authorized user's (`IsAuthenticated`) | 

## Testing

To run the tests, you need to install pytest of the version ^7.4.0.

To install the latest version of pytest run:

```commandline
pip install pytest
```
To execute the tests run the following command in the project directory:
```commandline
python manage.py pytest
```

