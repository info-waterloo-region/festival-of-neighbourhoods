---
title: Festival of Neighbourhoods Unregistered Activities
---
var unregistered2016 = {
  "type": "FeatureCollection", 
  "features": [{% for act in site.data.unregistered-activities-2016 %}{% assign place = site.data.codes | where:"postalCode",act.code %}{
    "type": "Feature", 
    "geometry": {
      "type": "Point", 
      "coordinates": [
        {{place[0].lon}},
        {{place[0].lat}}
      ]
    },
    "properties": {
      "neighbourhood": "{{act.neighbourhood}}",
      "activity": {
        "date": "{{act.date | date: "%b %d, %Y"}}",
        "activity": "{{act.activity | escape}}",
        "quote": ""
      }
    }
  }{% unless forloop.last %},{% endunless %}{% endfor %}]
}

