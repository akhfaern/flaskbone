# FlaskBone

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

# Sample Requests

# login 
POST http://127.0.0.1:5000/auth/login

{
    "username": "admin",
    "password": "admin"
}

response: 
{
  "errorCode": 0,
  "refreshToken": "refresh-token",
  "token": "token"
}

# user list
GET http://127.0.0.1:5000/user_management

Header: Authorization Bearer token

# add user 
POST http://127.0.0.1:5000/user_management

Header: Authorization Bearer token

{
    "username": "muratcem",
    "password": "123",
    "fullname": "Murat Cem YALIN",
    "active": true
}

# delete user
DELETE POST http://127.0.0.1:5000/user_management/2

Header: Authorization Bearer token