---
title: Festival of Neighbourhoods Capital Grants
---
{% assign grants = site.data.grants | group_by: "code" %}var grants = {
  "type": "FeatureCollection", 
  "features": [{% for grant in grants %}{% assign place = site.data.codes | where:"postalCode",grant.name %}{
    "type": "Feature", 
    "geometry": {
      "type": "Point", 
      "coordinates": [
        {{place[0].lon}},
        {{place[0].lat}}
      ]
    },
    "properties": {
      "grants": [{% for item in grant.items %}{
        "neighbourhood": "{{item.neighbourhood}}",
        "year": "{{item.year}}",
        "description": "{{item.description}}"
      }{% unless forloop.last %},{% endunless %}{% endfor %}]
    }
  }{% unless forloop.last %},{% endunless %}{% endfor %}]
}

