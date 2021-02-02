import requests

req = requests.get('https://www.pathofexile.com/character-window/get-items?character=YourAvgCascade', cookies={'POESESSID': '3b379908b193f539ae18fda1b8e86865'}, headers={'User-Agent': 'Mozilla/5.0'})
data = req.json()
print(data)
for i in range(0,len(data['items'])):
    if data['items'][i]['inventoryId']=='MainInventory':
        print(data['items'][i]['typeLine'])