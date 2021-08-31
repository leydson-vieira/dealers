# i-dealers

![GitHub](https://img.shields.io/github/license/leydson-vieira/dealers?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/leydson-vieira/dealers?style=plastic)

This is an API that provides endpoints for cashback generations based on orders made by dealers.

The app is entirely dockerized and its steps needs the installation of [Docker](https://www.docker.com/) and Docker Compose.

### Install

    git clone https://github.com/leydson-vieira/dealers.git
    cd dealers
    make build

### Run the app

    make run

### Run the tests

    make test

# REST API

### Usage

#### Auth:

Here we're using [JWT](https://jwt.io/) authentication. 

##### Headers:

    Authorization: Bearer <token>

#### Endpoints:

Here I make avaliable for you a [Insomnia Collection](https://github.com/leydson-vieira/dealers/blob/master/idealers-insomnia.json) to help

---

##### Create a Dealer account:

    POST /api/v1/dealers/
    
    curl --request POST \
      --url http://localhost:8000/api/v1/dealers/ \
      --header 'Content-Type: application/json' \
      --data '{
      "full_name": "Second User",
      "cpf": "15350946056",
      "email": "second.user@gmail.com",
      "password": "teste123"
    }'

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131528239-38ee9cf6-482a-40d3-9286-7beba7cc0467.png)

![image](https://user-images.githubusercontent.com/18724892/131528048-32167bf7-9488-4e5f-8fb4-dfd8afdf2dbf.png)


---

##### Get the token:

    POST /api/login/
    
    curl --request POST \
      --url http://localhost:8000/api/login/ \
      --header 'Content-Type: application/json' \
      --data '{
      "email": "second.user@gmail.com",
      "password": "teste123"
    }'
    
##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131528431-852d84a5-7996-4007-b9b1-61cc7f69a22a.png)

![image](https://user-images.githubusercontent.com/18724892/131528617-829e5e67-bb1d-41d1-af3e-3b2608382c04.png)

---

##### (Authenticated) Create an Order:

    POST /api/v1/orders/

    curl --request POST \
      --url http://localhost:8000/api/v1/orders/ \
      --header 'Authorization: Bearer <TOKEN>' \
      --header 'Content-Type: application/json' \
      --data '{
      "code": "007162t39",
      "cpf": "38723274884",
      "amount": "2000",
      "date": "2021-08-28T13:45:00.000Z"
    }'

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131528829-196256bf-9e71-4fdd-8411-2907ad8cf4d5.png)

![image](https://user-images.githubusercontent.com/18724892/131528956-0be65dba-fb7e-46cf-9037-38a6603f35bf.png)

![image](https://user-images.githubusercontent.com/18724892/131529025-e5f1c822-a158-48c5-8c1c-03640a9d8e68.png)

---

##### (Authenticated) Get all orders:

    GET /api/v1/orders/
    
    curl --request GET \
      --url 'http://localhost:8000/api/v1/orders/?limit=10&offset=0' \
      --header 'Authorization: Bearer <TOKEN>'

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131529142-409ffd00-1363-47b6-808d-0e5ef9e29c34.png)

---

##### (Authenticated) Update an order:

    PATCH /api/v1/orders/<uuid:order_id>/
    
    curl --request PATCH \
      --url http://localhost:8000/api/v1/orders/<uuid:order_id>/ \
      --header 'Authorization: Bearer <TOKEN>' \
      --header 'Content-Type: application/json' \
      --data '{
      "amount": "2500"
    }'

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131529294-242aea4d-b2f6-4212-97dc-1781a5b4b133.png)

![image](https://user-images.githubusercontent.com/18724892/131529365-48aff8bb-3ad2-46b9-8d4c-17fe91317c44.png)

![image](https://user-images.githubusercontent.com/18724892/131529408-1d1613c4-c8eb-4abe-b613-6a22fb1bbf0e.png)

![image](https://user-images.githubusercontent.com/18724892/131529025-e5f1c822-a158-48c5-8c1c-03640a9d8e68.png)

---

##### (Authenticated) Delete an order:

    DELETE /api/v1/orders/<uuid:order_id>/

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131529627-a0f8006d-1158-4d09-9981-942e751f6dbb.png)

![image](https://user-images.githubusercontent.com/18724892/131529723-2106923c-6f92-46a6-a71c-6e0f3ff82d19.png)

![image](https://user-images.githubusercontent.com/18724892/131529809-01c8995c-0402-4e96-950d-e5ad0765f8af.png)


---

##### (Authenticated) Get accumulated cashback:

    GET /api/v1/cashback/

    curl --request GET \
      --url http://localhost:8000/api/v1/cashback/ \
      --header 'Authorization: Bearer <TOKEN>' \
      --header 'Content-Type: application/json'

##### Responses:

![image](https://user-images.githubusercontent.com/18724892/131530477-48457cdb-f816-45b7-b37d-8cd1cadb1aeb.png)

---