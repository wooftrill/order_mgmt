import requests,time

session = requests.Session()
session.maxsize = 100
start_time = time.time()
url = 'http://localhost:5007/forward_to_Order'

jwt_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoieWNtZGVmbWU5cWc4QlNSTVNQcVYxcEtaZkg5MyIsInNlc3Npb25faWQiOiJnaHNnZGhzaDc4NzM2NzNod2dpa2siLCJleHAiOjE2OTQxODI2MTF9.6tpeJxjmFlNbn0R_65O2J_sjZJCKfqr9FSTTGnXmDrA'
item_id = '201816_03_02'



response = session.post(url, headers={'Authorization': f'Bearer {jwt_token}'})
time= time.time()-start_time
print(time)

print(response.text)
if response.status_code == 200:
    print('Items added to cart successfully')
else:
    print('Failed to add items to cart')