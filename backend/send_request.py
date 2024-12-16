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
#     "email": "john.doe4@example.com",      
#     "password": "123",
# }

# response = requests.post(url, json=data)
# print(response.json())

# get user by id #

# url = "http://localhost:5000/get_user_by_id/3"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzMwOTIyMzV9.LkVTRzN_A0lT8GYj16wDW3OWbfr-OwZ7cTfAbpqGu5c"
# }

# response = requests.get(url, headers=headers)

# if response.headers.get("Content-Type") == "application/json":
#     print("Response JSON:", response.json())
# else:
#     print("Response is not JSON:", response.text)


# admin token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzE0NDI5NjN9.yBjBrzrxXmPZV6Qbnsf2tFTssjL50Oc0VGrIrWerWDs 
# user token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzE0NDY3Nzd9.T4s3L1tNPFmgAKvJ4FREIXuQmPgr5ebSuwtJ6QLDnfs 

# update user #


# url = "http://localhost:5000/update_user/1"
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
#     "email": "john.doe4@example.com",
#     "password": "123",
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

# url = "http://localhost:5000/get_all_users"


# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzMwOTIyMzV9.LkVTRzN_A0lT8GYj16wDW3OWbfr-OwZ7cTfAbpqGu5c"
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)


# try:
#     print(response.json())
# except ValueError: 
#     print("Response is not JSON:", response.text)



# add expense #

# url = "http://localhost:5000/add_expense"

# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoidXNlciIsImV4cCI6MTczMzAwMjU4MH0.nnjJv5Q-S8iJxhZvHvoepJ5imoZwFh8iYyOlfSS5Opc",
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

# url = "http://localhost:5000/update_expense/2"

# headers = { "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwicm9sZSI6InVzZXIiLCJleHAiOjE3MzI4NDQyMzl9.tSiHF-6Y8La1qGedIHuitxa8sATrW4fIzTdwamcjlNQ"
# }

# data = { 
#     "amount" : 200,
#     "category_id" : 1,
#     "description" : "some description",
#     "is_recurring" : False
# }

# response = requests.put(url, headers=headers, json=data)
# print("Response is not JSON:", response.text)



# get all categories #

# url = "http://localhost:5000/get_categories"

# headers = { 
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzMwMDI0OTh9.XiQt3mPZpr9036w5Cm8o6dEcIgVlxOAS_Etjd6ap_1E"

# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)


# get expense by category #

# url = "http://localhost:5000/get_expenses_by_category/1"

# headers = {
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoidXNlciIsImV4cCI6MTczMzAwMjU4MH0.nnjJv5Q-S8iJxhZvHvoepJ5imoZwFh8iYyOlfSS5Opc"
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)


# reset_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzMwOTIyMzV9.LkVTRzN_A0lT8GYj16wDW3OWbfr-OwZ7cTfAbpqGu5c"

# url = "http://localhost:5000/reset_password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzMwOTIyMzV9.LkVTRzN_A0lT8GYj16wDW3OWbfr-OwZ7cTfAbpqGu5c"

# new_password = "112233"

# payload = {
#     "token": reset_token,
#     "new_password": new_password
# }


# response = requests.post(url, json=payload)

# if response.status_code == 200:
#     print("Password reset successful!")
#     print(response.json())
# else:
#     print(f"Failed to reset password. Status code: {response.status_code}")
#     print(response.json())  



# url = "http://localhost:5000/get_category/1"

# headers = {
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzQzNzc3NzZ9.TDlPlz4EdEMTwQgLkJ1tPP4vknqtkfKdSkspRGYoPiM"
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)


# url = "http://localhost:5000/add_category"

# headers = {
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzQzNzc3NzZ9.TDlPlz4EdEMTwQgLkJ1tPP4vknqtkfKdSkspRGYoPiM",
#     "Content-Type" : "application/json",
# }

# data = {
#     "name" : "Food",
#     "description" : "Food expenses"
# }

# response = requests.post(url, headers=headers, json=data)
# print("Response is not JSON:", response.text)


# url = "http://localhost:5000/get_categories"

# headers = {
#     "Authorization" : "Beraer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MzQzNzc3NzZ9.TDlPlz4EdEMTwQgLkJ1tPP4vknqtkfKdSkspRGYoPiM "
# }

# response = requests.get(url, headers=headers)
# print("Response is not JSON:", response.text)
