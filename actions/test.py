import json

f = open('./data/games.json')
json_dict = json.load(f)

output = []
for key, val in json_dict.items():
    if key == 'data':
        for key2, val2 in val.items():
            if key2 == 'categories':
                temp = val2[0]['subCategories']
                for i in range(len(temp)):
                    _title = temp[i]['title']
                    _content3 = temp[i]['content3']
                    for j in _content3:
                        _subtitle = j['title']
                        _image_url = j['previewImageUrl']
                        _url = j['gameurl']
                        output.append({
                            'title': _title,
                            'subtitle': _subtitle,
                            'image_url': _image_url,
                            'url': _url
                            })
print(output)
                        
                        
                        
                        