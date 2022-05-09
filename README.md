# flaskbone

A simple base application to be used in flask projects 

- user authentication 
- auto routing with generic blueprint and base request class
- python data validation for requests with base data class and validation


# usage

- export FLASK_APP=fb or for windows set FLASK_APP=fb
- flask run
- login url: /auth/login
- auth header: Authorization: Bearer token
- sample api end point: /user_management

# sample request

# login 
POST http://127.0.0.1:5000/auth/login
{
    "username": "admin",
    "password": "admin"
}

response: 
{
  "errorCode": 0,
  "refreshToken": "bdb8139b-aa5e-442d-851b-d00f5b548a30",
  "token": "token"
}

# user list
GET http://127.0.0.1:5000/user_management

# add user 
POST http://127.0.0.1:5000/user_management
{
    "username": "muratcem",
    "password": "123",
    "fullname": "Murat Cem YALIN",
    "active": true
}

# delete user
DELETE POST http://127.0.0.1:5000/user_management/2