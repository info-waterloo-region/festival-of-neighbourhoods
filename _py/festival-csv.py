import gspread
import csv
import json
import geocoder

import config

from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open(config.json_key))
scope = ["https://spreadsheets.google.com/feeds"]

credentials = SignedJwtAssertionCredentials(json_key["client_email"], json_key["private_key"], scope)
g = gspread.authorize(credentials)
s = g.open("FON Map 2016")
code_sheet = s.worksheet("PostalCodes")
code_list = code_sheet.get_all_values()

with open("_data/codes.csv", "wb") as codes:
  c = csv.writer(codes, quoting=2)
  c.writerows(code_list)

new_codes = []

def activities_csv(activities, sheet=code_sheet, codes=code_list):
  acts = [["neighbourhood", "ward", "code", "activity", "date", "quote"]]
  new_codes = []
  for act in activities["sheet"].get_all_records():
    if act["postalCode"].strip() not in [c[1] for c in codes]:
      print "Missing postal code", act["postalCode"]
      geo = geocoder.google(act["postalCode"].strip())
      if geo.ok:
        print geo.latlng
        new_codes.append([
          act["neighbourhood"].strip(),
          act["postalCode"].strip(),
          geo.latlng["lng"],
          geo.latlng["lat"]
        ])
      else:
        print "Skipping", act["postalCode"], geo.status
    else:
      ward = 0 if not act["ward"] else int(act["ward"])
      acts.append([
        act["neighbourhood"].encode("utf-8").strip(),
        ward,
        act["postalCode"].encode("utf-8").strip(),
        act["activity"].encode("utf-8").strip(),
        act["date"].strip(),
        act["quote"].encode("utf-8").strip() if "quote" in act else None
      ])

  with open("_data/{}-activities.csv".format(activities["name"]), "wb") as f:
    c = csv.writer(f, quoting=2)
    c.writerows(acts)

  return new_codes
      
reg = {
  "name": "registered",
  "sheet": s.worksheet("RegisteredActivities")
}

new_codes.extend(activities_csv(reg))

unreg = {
  "name": "unregistered",
  "sheet": s.worksheet("UnregisteredActivities")
}

new_codes.extend(activities_csv(unreg))

grants = {
  "fields": [["code", "neighbourhood", "year", "description"]],
  "sheet": s.worksheet("CapitalGrants")
}

for grant in grants["sheet"].get_all_records():
  if grant["postalCode"].strip() not in [c[1] for c in code_list]:
    print "Missing postal code", grant["postalCode"]
    geo = geocoder.google(grant["postalCode"].strip())
    if geo.ok:
      print geo.latlng
      new_codes.append([
        grant["neighbourhood"].encode("utf-8").strip(),
        grant["postalCode"].encode("utf-8").strip(),
        geo.latlng["lng"],
        geo.latlng["lat"]
      ])
    else:
      print "Skipping", grant["postalCode"], geo.status
  else:
    grants["fields"].append([
      grant["postalCode"].encode("utf-8").strip(),
      grant["neighbourhood"].encode("utf-8").strip(),
      grant["year"],
      grant["description"].encode("utf-8").strip()
    ])

with open("_data/grants.csv", "wb") as f:
  c = csv.writer(f, quoting=2)
  c.writerows(grants["fields"])

if new_codes:
  n = "_py/new-codes.csv"
  with open(n, "ab") as f:
    c = csv.writer(f, quoting=2)
    c.writerows(new_codes)
    print "New postal codes in", n



