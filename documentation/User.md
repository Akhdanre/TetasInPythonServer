# User API Spec

## Register
Endpoint : post /api/register

Request Body :
```json
{
    "username" : "Oukenze12",
    "password" : "superone",
    "name" : "Akhdan Robbani"
}
```

Response Body (Success): 
```json
{
    "data" : "ok"
}
```

Response Body (failed) : 
```json 
{
    "detail" : "username must not blank"
}
```

Response Body (failed duplicat) : 
```json 
{
    "detail" : "username already exist"
}
```

## login
Endpoint : post /api/authentication

Request Body : 

```json
{
    "username" : "Oukenze12",
    "password" : "superone"
}
```

Response Body (success) : 
```json
{
    "username" : "Oukenze12", 
    "name" : "AKhdan Robbani", 
    "token" : "12kajsdlkekjdl"
}
```


Response Body (failed) :
```json
{
    "error" : "wrong username and password"
}
```

## udpate user data 
Endpoint : patch /api/udpateUser

Request Body : 
```json
{
    "oldpassword" : "superone" ,
    "password" : "supersepo", // new password
    "name" : "dani" // new name
}
```

Response Body (success) :
```json
{
    "message" : "success change user data"
}
```

Response Body (failed) : 
```json 
{
    "error" : "wrong old password"
}
```

## logout
Endpoint : get /api/logout

header body :
- X-API-TOKEN = "klajsdlkjf"

Response Body : 
```json
{
    "message" : "logout success"
}
```
