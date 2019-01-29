# Recycling

## InteractionDiagram

![alt text](https://innersource.soprasteria.com/digitalfactory/recycling/raw/master/doc/interaction.png)

```
@startuml

title "Recyling - Sequence Diagram"

participant Mobile
participant Backend


note over Mobile: Get Product Details with RecyclableProduct
Mobile -> Backend : /product/<barcode>/

note over Mobile: Get RecyclableSpots from barcode filtered with recyclablegroupsover Mobile
Mobile -> Backend : /product/<barcode>/recyclablespot/?latitude=<latitude>&longitude=<longitude>

note over Mobile: Get RecyclableSpots
Mobile -> Backend : /recyclablespot/

note over Mobile: Get Nearby RecyclableSpot
Mobile -> Backend : /recyclablespot/nearby/?latitude=<latitude>&longitude=<longitude>

note over Mobile 
    Get Stats 
    Green Impact, N_Recycles, Ranking
    Week/Month/Year (N_Scan, Percentage of Material)
end note
Mobile -> Backend : /greenimpact/?startdate=<startdate>&enddate=<enddate>

note over Mobile: Get Ranking
Mobile -> Backend : /ranking/

note over Mobile: Get News
Mobile -> Backend : /news/

note over Mobile: Get Default location
Mobile -> Backend : /location/default/

note over Mobile: Get Partners (Partners with description)
Mobile -> Backend : /partners/


@enduml
```

## DataModel
![alt text](https://innersource.soprasteria.com/digitalfactory/recycling/raw/master/doc/datamodel.png)

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
 
class RecyclableMaterial {
  id
  name
  country
  component_id(FK)
  bullet_colour
  letter_colour
}
 
class RecyclableSpot {
  id
  name
  location
  phone
  opening_hours
  group_id (FK)
}

class RecyclableHistory {
  barcode_not_linked_to_product
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
Materials "1" -right- "N" RecyclableMaterial
RecyclableMaterial "M" -down- "N" RecyclableSpot
News "1" -down- "N" Likes
Likes "1" -left- "N" Users

@enduml
```

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

### Product - RecyclableSpot
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/product/<barcode>/recyclablespot/?latitude=<latitude>&longitude=<longitude> [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the recyclable spots for the product nearby location. It will insert a registry into Scan History with the scanned bar code, a location and a timestamp into the Scan_history table. A maximum of 10 spots with less than 15Km radius</td>
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

### RecyclableSpot - Nearby
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/recyclablespot/nearby/?latitude=<latitude>&longitude=<longitude> [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve all the recyclable spots nearby locationA maximum of 10 spots with less than 15Km radius</td>
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


### Stats (GreenImpact)
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/stats/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To stats of the user</td>
  </tr>
  <tr>
    <td><strong>Body</strong></td>
    <td>userId</td>
  </tr>
  <tr>
    <td><strong>Expected Response</strong></td>
    <td style="font-family: Consolas,monaco,monospace;">{<br>
    "n_scan": 876,<br>
    "ranking": 765,<br>
    "green_impact": 81.8,<br>
    "weekly": {<br>
        "n_scan": 103,<br>
        "material_set": {<br>
            "cardboard": 50,<br>
            "paper": 30,<br>
            "aluminum": 20<br>
        }<br>
    },<br>
    "monthly": {<br>
        "n_scan": 221,<br>
        "material_set": {<br>
            "cardboard": 50,<br>
            "paper": 30,<br>
            "aluminum": 20<br>
        }<br>
    },<br>
    "yearly": {<br>
        "n_scan": 456,<br>
        "material_set": {<br>
            "cardboard": 50,<br>
            "paper": 30,<br>
            "aluminum": 20<br>
        }<br>
    }<br>
}</td>
  </tr>
  <tr>
    <td><strong>Error Codes</strong></td>
    <td>N/A</td>
  </tr>
</table>

### Ranking
<table>
  <tr>
    <td><strong>URL</strong></td>
    <td>/ranking/ [GET]</td>
  </tr>
  <tr>
    <td><strong>Description</strong></td>
    <td>To retrieve a ranking of the users according to the number of recycle history he made</td>
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


### RecyclingHistory
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
