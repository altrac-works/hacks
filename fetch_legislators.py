import csv
import json
import os
import pprint

import requests

query = """
query legislativeMembers($leaders: Boolean, $elected: Boolean, $body: LegislativeBody, $search: String, $order: Order) {
  legislativeMembers(
    where: {leader: {eq: $leaders}, elected: {eq: $elected}, body: {eq: $body}, active: {eq: true}}
    search: $search
    order: $order
  ) {
    data {
      id
      body
      leadershipTitle
      fullName
      lastName
      honorificFullNameAffiliation
      honorific
      districtPhone
      phone
      districtEmail
      email
      fullAddress
      fullDistrictAddress
      affiliation
      district
      counties
      __typename
    }
    __typename
  }
}
"""


def get_house_members():
    result = requests.post(
        "https://alison.legislature.state.al.us/graphql",
        json={
            "query": query,
            "operationName": "legislativeMembers",
            "variables": {
                "body": "House",
                "leaders": False,
                "order": "sortOrder",
            },
        },
    ).json()

    return result["data"]["legislativeMembers"]["data"]


def get_senate_members():
    result = requests.post(
        "https://alison.legislature.state.al.us/graphql",
        json={
            "query": query,
            "operationName": "legislativeMembers",
            "variables": {
                "body": "Senate",
                "leaders": False,
                "order": "sortOrder",
            },
        },
    ).json()

    return result["data"]["legislativeMembers"]["data"]


columns = [
    "alison_id",
    "ocdid",
    "name",
    "name_with_title",
    "party",
    "phone_district",
    "phone_capitol",
    "office_district",
    "office_capitol",
    "email_district",
    "email_capitol",
]


def chomp(x):
    if x is None:
        return ""

    if x == "None Listed":
        return ""

    if "No District Address Listed" in x:
        return ""

    if "Email Not" in x:
        return ""

    return x


def clean_phone(x):
    x = chomp(x)
    if not x:
        return ""

    result = ""
    for i in x:
        if i.isnumeric():
            result += i

    assert len(result) == 10

    return f"{result[:3]}-{result[3:6]}-{result[6:]}"


def clean_office(address, m):
    a1, a2, _ = address.split("\n", maxsplit=3)
    if a1 not in {
        "11 South Union Street",
        "11 S Union Street",
    }:
        if m["id"] not in {"100579", "100563"}:
            print(m)
            raise ValueError(f"{a1} is not 11 South Union Street")

        else:
            return ""

    result = "-".join(a2.split()[1:])
    if result == "Listed":
        return ""

    return result


def transform_member(m):
    ocd_type = "sldu" if m["body"] == "Senate" else "sldl"
    district = int(m["district"].split()[-1])
    ocdid = f"ocd-division/country:us/state:al/{ocd_type}:{district}"

    return [
        int(m["id"]),
        ocdid,
        " ".join(m["fullName"].split()),
        f'{m["honorific"]} {m["lastName"].strip()}',
        m["affiliation"],
        clean_phone(m["districtPhone"]),
        clean_phone(m["phone"]),
        chomp(m["fullDistrictAddress"]).replace("\n", "; "),
        clean_office(m["fullAddress"], m),
        chomp(m["districtEmail"]),
        chomp(m["email"]),
    ]


if not os.path.exists("members.json"):
    house = get_house_members()
    senate = get_senate_members()

    pprint.pprint(house)
    pprint.pprint(senate)

    with open("members.json", "w") as f:
        json.dump(house + senate, f)

with open("members.json") as f:
    members = json.load(f)

rows = []
for member in members:
    rows.append(transform_member(member))

rows.sort(key=lambda k: ((p := k[1].split("/")[-1].split(":"))[0], int(p[1])))
rows.insert(0, columns)

with open("members.csv", "w") as f:
    csv.writer(f).writerows(rows)
