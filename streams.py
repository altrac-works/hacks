import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from bs4 import BeautifulSoup

transport = AIOHTTPTransport(url="https://gql.api.alison.legislature.state.al.us/graphql", headers={'Content-type':'application/json'})
client = Client(transport=transport)

query = gql('query streamLocations {  locations: legislativeStreams(location: "") { Location EmbedCode } }')
result = client.execute(query)
rooms = result["locations"]

embed_urls = {}
for room in rooms:
    embedcode = room['EmbedCode'] #wut
    html = BeautifulSoup(embedcode, 'html.parser')
    embed_urls[room["Location"]] = html.select_one('iframe')['src']

print(json.dumps(embed_urls))
