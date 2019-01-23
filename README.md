# Recycling

## Endpoint Definition

URL
/news/<news_id>
Action
GET
Description
This endpoint will be used to retrieve all the news and all its information.
Body
From, to: From the news X to the news X, done for pagination.
Expected Response
It will include the total number of news.
Error Codes

URL
/news/<newsid>/likes
Action
GET
Description
This endpoint will be used to retrieve all the likes within a single news.
Body
newsId (array): Returns all 
Expected Response

Error Codes

URL
/product
Action
GET
Description
This endpoint will be used to retrieve all the products and all its information.
Body
Productid (barcode)
Expected Response

Error Codes

URL
/recycling/<spotid>
Action
GET
Description
This endpoint will be used to retrieve all the recycling spots and all its information.
Body
recyclingspotid
Expected Response

Error Codes


URL
/recycling/history
Action
GET
Description
This endpoint will be used to retrieve all the recycling history for an user and all its information.
Body
startDate, endDate, UID (withing Gigya token)
Expected Response

Error Codes

URL
/product/<product_id>/location/
Action
POST
Description
This endpoint will be used to retrieve all the points information within the given product id. It will insert a registry into Scan History with the scanned bar code, a location and a timestamp into the Scan_history table.
Body
startDate, endDate, UID (withing Gigya token)
Expected Response

Error Codes

URL
scan/
Action
GET
Description
This endpoint will be used to retrieve all the locations with a count of how many scans have been done there, grouped by location and component (or product).
Body
Location, scanId
Expected Response

Error Codes


URL
scan/greenimpact
Action
GET
Description
This endpoint will be used to retrieve the green impact score of an user (We need to define calculations). TBD if it’s weekly, monthly
Body
userId
Expected Response

Error Codes

Los recycling points serán multilenguaje

En un rango de 15 km se mostrarán máximo 10 resultados en los recycling points

Recycling_groups:

[
{
  "id":0,
  "name": "Aluminium",
  "bulletColour": "#f9027a",
  "letterColour" "#ffffff"
},
{
  "id":1,
  "name": "Batteries",
  "bulletColour": "#ff7b00",
  "letterColour" "#ffffff"
},
{
  "id":2,
  "name": "Electric Equipment",
  "bulletColour": "#aaad01",
  "letterColour" "#ffffff"
},
{
  "id":3,
  "name": "Household Appliances",
  "bulletColour": "#59ad01",
  "letterColour" "#ffffff"
},
{
  "id":4,
  "name": "Electric Equipment",
  "bulletColour": "#01ad96",
  "letterColour" "#ffffff"
},
{
  "id":5,
  "name": "Glass",
  "bulletColour": "#0162ad",
  "letterColour" "#ffffff"
},
{
  "id":6,
  "name": "PET Bottles",
  "bulletColour": "#a701ad",
  "letterColour" "#ffffff"
},
]


## DataModel
Insert Here PlantUML Image
```
@startuml
 
title Data Model
 

class Products {
  id
  name
  description
  location
  timestamp
  material_id(FK)
}
 
class Materials {
  id
  name
  description
  group_id(FK)
  timestamp
}
 
class Recycling_groups {
  id
  name
  country
  component_id(FK)
  bullet_colour
  letter_colour
}
 
class Recycling_spots {
  id
  name
  location
  phone
  opening_hours
  group_id (FK)
}

class Scan_history {
  bar_code
  location
  timestamp
  user
}

class Recycling_history {
  bar_code
  timestamp
  user
}

class News {
  id
  country
  language
  title
  content
  category
  icon
  main_image
  scheduled_date
  published
  timestamp
  author
  likes_id(FK)
}

class Likes {
  id
  quantity
}

class Users {
  id
  name
  email
  likes_id(FK)
}

class Green_ranking {
  id
  user_id
  name
  scan_count
}
 

Products "N" -right- "M" Materials
Materials "1" -right- "N" Recycling_groups
Recycling_groups "1" -down- "N" Recycling_spots
Recycling_history "1" -up- "N" Products
News "1" -down- "N" Likes
Likes "1" -left- "N" Users

@enduml
```
