---
title: Festival of Neighbourhoods Unregistered Activities
---
{% assign activities = site.data.unregistered-activities | group_by: "code" %}var unregistered = {
  "type": "FeatureCollection", 
  "features": [{% for act in activities %}{% assign place = site.data.codes | where:"postalCode",act.name %}{
    "type": "Feature", 
    "geometry": {
      "type": "Point", 
      "coordinates": [
        {{place[0].lon}},
        {{place[0].lat}}
      ]
    },
    "properties": {
      "neighbourhood": "{{place[0].neighbourhood}}",
      "activities": [{% for item in act.items %}{
        "date": "{{item.date}}",
        "activity": "{{item.activity}}"
      }{% unless forloop.last %},{% endunless %}{% endfor %}]
    }
  }{% unless forloop.last %},{% endunless %}{% endfor %}]
}

