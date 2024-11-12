import requests

# profile request #

# url = "http://localhost:5000/get_user_profile"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwicm9sZSI6InVzZXIiLCJleHAiOjE3MzE0NDIyODd9.0J4GAXW0P3GLbE8Skfvk-bRthroIFVpnHB_RS0J4ZEw"
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


# url = "http://localhost:5000/reset_password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE3MzE0MjU0MjJ9.ca_MbPKXg7r25pUsoMDuxL73W1xHh3_GED8i1YmCnwk"  # Replace with the actual token from the email
# data = {
#     "new_password": "your_new_password"
# }

# response = requests.post(url, json=data)
# print("JSON Response:", response.json())