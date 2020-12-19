import json as js


def save_json(face, eyes, smile):
    data = {
        'Face': face,
        'Eyes': eyes,
        'Smile': smile
    }
    with open('output.json', 'w') as json_file:
        js.dump(data, json_file)