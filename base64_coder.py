import base64

with open("ИМЯ/ПУТЬ", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    # decoded_string = base64.b64decode(encoded_string)

print(encoded_string)
# print(decoded_string)
