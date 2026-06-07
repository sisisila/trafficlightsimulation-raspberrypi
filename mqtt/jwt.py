'''
Example from: https://vegibit.com/json-web-tokens-in-python/
'''

import jwt
import datetime
import time

SECRET = "my-secret"

def authenticate():

    # Create a JWT token with a subject claim "admin" and an expiration time of 1 hour
    expire_on = datetime.datetime.utcnow() + datetime.timedelta(days=10)
    payload = {"sub": "admin", "exp": expire_on.timestamp()}
    #token = jwt.encode(payload, SECRET, algorithm="HS256")
    return payload

    
    # valid_token = authenticate("admin", "password")
    # print('valid token: ', valid_token)

    # #Incorrect user or incorrect password
    # invalid_token = authenticate("admin", "incorrect_password")
    # print('invalid token: ', invalid_token)

    # # Decode and verify the JWT, and print the subject claim



valid_token = authenticate()
# decoded = jwt.decode(valid_token, SECRET, verify=True, algorithms=["HS256"])
# # print(decoded["sub"])  # "admin"

def check_expiration_date():
    # Check the expiration time of the JWT
    if datetime.datetime.utcnow().timestamp() > valid_token["exp"]:
        print("JWT has expired")
    else:
        print("JWT is valid")

    time.sleep(1) #to pass 0.5 seconds
    if datetime.datetime.utcnow().timestamp() > valid_token["exp"]:
        print("JWT has expired")