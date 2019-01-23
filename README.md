# Recycling

## Endpoint Definition




<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/news/<news_id> [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the news and all its information.</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>From, to: From the news X to the news X, done for pagination.</td>
  </tr>
  <tr>
    <td><strong>Expected Response</strong></td>
    <td>total number of news.</td>
  </tr>
  <tr>
    <td><strong>Error Codes</strong></td>
    <td>N/A</td>
  </tr>
</table>


<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/news/<newsid>/likes [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the likes within a single news</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>newsId (array): Returns all</td>
  </tr>
  <tr>
    <td><strong>Expected Response</strong></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><strong>Error Codes</strong></td>
    <td>N/A</td>
  </tr>
</table>


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
