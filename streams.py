import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from bs4 import BeautifulSoup

transport = AIOHTTPTransport(url="https://gql.api.alison.legislature.state.al.us/graphql", headers={'Content-type':'application/json'})
client = Client(transport=transport)

query = gql('{legislativeStreamsByLocation(location:""){ Location }}')
result = client.execute(query)
rooms = [x['Location'] for x in result['legislativeStreamsByLocation']]

embed_urls = {}
for room in rooms:
    query = gql('{legislativeStreamsByLocation(location:"' + room.removeprefix('Room ') + '"){ EmbedCode }}')
    result = client.execute(query)
    embedcode = result['legislativeStreamsByLocation'][0]['EmbedCode'] #wut
    html = BeautifulSoup(embedcode, 'html.parser')
    embed_urls[room] = html.select_one('iframe')['src']

print(json.dumps(embed_urls))
