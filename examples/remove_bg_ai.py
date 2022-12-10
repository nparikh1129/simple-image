import requests


response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('/Users/nparikh/Library/Mobile Documents/com~apple~CloudDocs/Work/Elite Tutoring/image_manipulation/data/girl_shadows_gs.png', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'v5Xt1nWiR5VvThmBw34nwhiu'},
)
if response.status_code == requests.codes.ok:
    with open('girl_shadows_gs_bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
