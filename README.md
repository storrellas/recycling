# Recycling

## Endpoint Definition

### Sergi Endpoint Definition

- Scan Product to retrieve RecyclableComponents
- Get RecyclableSpot from RecyclableComponents
- GreenImpact Endpoint - Retrieve Green Impact from RecyclabeHistory
- News Retrieve

### Product
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/product/<barcode>/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve information of a product given a barcode together with RecyclabeComponents</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>N/A</td>
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

### RecyclableSpot
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/product/<barcode>/location/ [POST]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the points information within the given product id. It will insert a registry into Scan History with the scanned bar code, a location and a timestamp into the Scan_history table. A maximum of 10 spots with less than 15Km radius</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>startDate, endDate, UID (withing Gigya token)</td>
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

### Recycling Spot
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/recyclablespot/<spotid>/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the recycling spots and all its information.</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>recyclingspotid</td>
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

### Recycling History
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/recyclable/history/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the recycling history for an user and all its information</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>startDate, endDate, UID (within Gigya token)</td>
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



### Scan
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/scan/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the locations with a count of how many scans have been done there, grouped by location and component (or product).</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>Location, scanId</td>
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


### GreenImpact
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/scan/greenimpact [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve the green impact score of an user (We need to define calculations). TBD if it’s weekly, monthly</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>userId</td>
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

### News
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/news/ [GET]</td>
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

### News Likes
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/news/likes [GET]</td>
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
![alt text](https://raw.githubusercontent.com/storrellas/recycling/master/doc/datamodel.png)

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
