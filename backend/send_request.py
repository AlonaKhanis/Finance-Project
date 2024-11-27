import requests

# profile request #

# url = "http://localhost:5000/get_user_profile"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI2Nzg2NDF9.JD-198Cj9BCpO_bPMEjISM7msZlteyR2sPmamvr_QeM"
# }

# response = requests.get(url, headers=headers)
# print(response.json())


# login request # 

# url = "http://localhost:5000/login"
# data = {
#     "email": "alonakhani1993@gmail.com",      
#     "password": "some",
# }

# response = requests.post(url, json=data)
# print(response.json())

# get user by id #

# url = "http://localhost:5000/get_user/5"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwicm9sZSI6InVzZXIiLCJleHAiOjE3MzE0NDIyODd9.0J4GAXW0P3GLbE8Skfvk-bRthroIFVpnHB_RS0J4ZEw"
# }

# response = requests.get(url, headers=headers)
# print(response.json()) 


# admin token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzE0NDI5NjN9.yBjBrzrxXmPZV6Qbnsf2tFTssjL50Oc0VGrIrWerWDs 
# user token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzE0NDY3Nzd9.T4s3L1tNPFmgAKvJ4FREIXuQmPgr5ebSuwtJ6QLDnfs 

# update user #


# url = "http://localhost:5000/update_user/10"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzE0NDY3Nzd9.T4s3L1tNPFmgAKvJ4FREIXuQmPgr5ebSuwtJ6QLDnfs",
#     "Content-Type": "application/json"
# }
# data = {
#     "first_name": "Alona",
#     "last_name": "Khanis"
# }

# response = requests.put(url, headers=headers, json=data)
# print(response.json())

# delete user #

# url = "http://localhost:5000/delete_user/2"
# headers = {
#     "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzE0NDI5NjN9.yBjBrzrxXmPZV6Qbnsf2tFTssjL50Oc0VGrIrWerWDs"
# }

# response = requests.delete(url, headers=headers)
# print(response.json())


# change password #

# url = "http://localhost:5000/request_reset" 
# data = {
#     "email": "alen4ik24444@gmail.com"
# }

# response = requests.post(url, json=data)
# print("JSON Response:", response.json())


# reset password #

# url = "http://localhost:5000/reset_password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE3MzE0MjU0MjJ9.ca_MbPKXg7r25pUsoMDuxL73W1xHh3_GED8i1YmCnwk"  # Replace with the actual token from the email
# data = {
#     "new_password": "your_new_password"
# }

# response = requests.post(url, json=data)
# print("JSON Response:", response.json())


# register user #

# url = "http://localhost:5000/register"
# data = {
#     "email": "john.doe@example.com",
#     "password": "john123",
#     "first_name": "John",
#     "last_name": "Doe",
#     "role": "user"
# }

# response = requests.post(url, json=data)

# if response.status_code == 201:
#     print("Registration successful:", response.json())
# elif response.status_code == 400:
#     print("Error:", response.json())
# else:
#     print("Unexpected response:", response.status_code, response.json())

# get all users #

# url = "http://localhost:5000/get_users"


# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzI2NzkwNjR9.83RIf913cNLgvQoR9sKlNS5xQ1noKiwTdAW5u8mKbnI"
# }

# response = requests.get(url, headers=headers)


# try:
#     print(response.json())
# except ValueError: 
#     print("Response is not JSON:", response.text)



# add expense #

# url = "http://localhost:5000/add_expense"

# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI3NTE2NDh9.ies8qnGhcW4uksc1W1j8AA7AGFzuP6qWJ2mbzA4HT-A",
#     "Content-Type" : "application/json"
# }

# data = {
#     "amount" : 100,
#     "category_id" : 1,
#     "price" : 100,
#     "description" : "some description",
#     "is_recurring" : False
# }

# response = requests.post(url, headers=headers, json=data)

# try:
#     print(response.json())
# except ValueError: 
#     print("Response is not JSON:", response.text)


# get expenses #

# url = "http://localhost:5000/get_expenses"

# headers = {
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI3NTE2NDh9.ies8qnGhcW4uksc1W1j8AA7AGFzuP6qWJ2mbzA4HT-A"
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)

# get expense by id#

# url = "http://localhost:5000/get_expense/2"

# headers = { 
#     "Authorization": "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI3NTE2NDh9.ies8qnGhcW4uksc1W1j8AA7AGFzuP6qWJ2mbzA4HT-A"
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)

# delete expense #

# url = "http://localhost:5000/delete_expense/1"

# headers = { 
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI3NTE2NDh9.ies8qnGhcW4uksc1W1j8AA7AGFzuP6qWJ2mbzA4HT-A"
# }

# response = requests.delete(url, headers=headers)
# print("Response is not JSON:", response.text)


# update expense #

# url = "http://localhost:5000/update_expense/1"

# headers = { "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI3NTE2NDh9.ies8qnGhcW4uksc1W1j8AA7AGFzuP6qWJ2mbzA4HT-A"
# }

# data = { 
#     "amount" : 200,
#     "category_id" : 1,
#     "description" : "some description",
#     "is_recurring" : False
# }

# response = requests.put(url, headers=headers, json=data)
# print("Response is not JSON:", response.text)