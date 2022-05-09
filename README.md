# FlaskBone

A simple base application to be used in flask api projects 

- api based structure
- user authentication 
- auto routing with generic blueprint and base request class
- python data validation for requests with base data class and validation


## Usage

Linux / MacOs 
```
export FLASK_APP=fb
flask run
```

Windows
```
CMD
set FLASK_APP=fb

PS
$env:FLASK_APP = "fb"

flask run
```

## Data classes
To create new end point, just create a class that extends BaseRequestClass inside lib folder. That class needs to handle
get, post, put and delete methods. if you want to write data, use BaseDataClass. further example about BaseDataClass could
be found in [pythonDataValidation](https://github.com/akhfaern/pythonDataValidation)

# Sample Requests

## Login
```
POST http://127.0.0.1:5000/auth/login

{
    "username": "admin",
    "password": "admin"
}
```

```
response: 
{
  "errorCode": 0,
  "refreshToken": "refresh-token",
  "token": "token"
}
```

## Get User List
```
GET http://127.0.0.1:5000/user_management

Header: Authorization Bearer token
```

## Add user 
```
POST http://127.0.0.1:5000/user_management

Header: Authorization Bearer token

{
    "username": "muratcem",
    "password": "123",
    "fullname": "Murat Cem YALIN",
    "active": true
}
```

## Delete user
```
DELETE POST http://127.0.0.1:5000/user_management/2

Header: Authorization Bearer token
```