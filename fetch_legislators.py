import csv
import json
import os

import requests

query = """
{
  houseMembers {
    ID
    MemberId
    MemberBody
    MemberType
    Title_1
    Title_2
    ImgUrl
    NewImgUrl
    TitleFullNameAffiliation
    FullName
    FirstName
    LastName
    ProperFirstName
    ProperLastName
    Affiliation
    Address_1
    Address_2
    AddressCity
    AddressState
    Phone
    AddressZip
    FullAddress
    Fax
    Email
    Website
    WebsiteText
    Bio
    District
    TermEnded
    Counties
    DistrictPhone
    DistrictFax
    DistrictAddress_1
    DistrictOffice
    DistrictCity
    DistrictState
    DistrictZip
    DistrictEmail
    FullDistrictAddress
    IsActive
  }
}
"""


def get_house_members():
    result = requests.post(
        "https://alison.legislature.state.al.us/graphql",
        json={"query": query, "variables": {}},
    ).json()

    return result["data"]["houseMembers"]


def get_senate_members():
    result = requests.post(
        "https://alison.legislature.state.al.us/graphql",
        json={"query": query.replace("houseMembers", "senateMembers"), "variables": {}},
    ).json()

    return result["data"]["senateMembers"]


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


def clean_office(a1, a2, m):
    if a1 not in {
        "11 South Union Street",
        "11 S Union Street",
    }:
        if m["MemberId"] not in {"100579", "100563"}:
            print(m)
            raise ValueError(f"{a1} is not 11 South Union Street")

        else:
            return ""

    result = "-".join(a2.split()[1:])
    if result == "Listed":
        return ""

    return result


def transform_member(m):
    ocd_type = "sldu" if m["MemberBody"] == "Senate" else "sldl"
    district = int(m["District"].split()[-1])
    ocdid = f"ocd-division/country:us/state:al/{ocd_type}:{district}"

    return [
        int(m["MemberId"]),
        ocdid,
        " ".join(m["FullName"].split()),
        f'{m["Title_2"]} {m["LastName"].strip()}',
        m["Affiliation"],
        clean_phone(m["DistrictPhone"]),
        clean_phone(m["Phone"]),
        chomp(m["FullDistrictAddress"]).replace("\n", "; "),
        clean_office(m["Address_1"], m["Address_2"], m),
        chomp(m["DistrictEmail"]),
        chomp(m["Email"]),
    ]


if not os.path.exists("members.json"):
    house = get_house_members()
    senate = get_senate_members()

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
