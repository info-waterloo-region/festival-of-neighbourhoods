---
title: Festival of Neighbourhoods Registered Activities
---
var registered2016 = {
  "type": "FeatureCollection", 
  "features": [{% for act in site.data.registered-activities-2016 %}{% assign place = site.data.codes | where:"postalCode",act.code %}{
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
        "quote": "{{act.quote | escape}}"
      }
    }
  }{% unless forloop.last %},{% endunless %}{% endfor %}]
}

