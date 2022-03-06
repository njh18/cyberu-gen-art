from PIL import Image 
from IPython.display import display 
import random
import json


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["1", "2","3","4","5"] 
background_weights = [20, 20, 20, 20, 20]

midground = ["0","1"]
midground_weights = [50,50]

base = ["1","2","3"]
base_weights = [33,33,33]


# TODO: add clothes and eye lashes

hair = ["1","2","3"]
hair_weights = [33,33,33]

eyelash = ["0","1"]
eyelash_weights = [50,50]

clothes = ["1", "2","3","4","5"] 
clothes_weights = [20, 20, 20, 20, 20]



# Dictionary variable for each trait. 
# Eech trait corresponds to its file name
# Add more shapes and colours as you wish

background_files = {
    "1": "background_1",
    "2": "background_2",
    "3": "background_3",
    "4": "background_4",
    "5": "background_5"
}

midground_files = {
    "0": "",
    "1":"midground"
}

base_files = {
    "1": "base_1",
    "2": "base_2",
    "3": "base_3"
}

hair_files = {
    "1":"hair_1",
    "2":"hair_2",
    "3":"hair_3"
}

eyelash_files = {
    "0":"",
    "1":"eyelash"
}

clothes_files = {
    "1": "clothes_1",
    "2": "clothes_2",
    "3": "clothes_3",
    "4": "clothes_4",
    "5": "clothes_5"
}



TOTAL_IMAGES = 15 # Number of random unique images we want to generate ( 5 x 2 x 3 x 3 x 2 x 5= 50)

all_images = [] 

def create_new_image():

    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image ["Background"] = random.choices(background, background_weights)[0]
    new_image ["Midground"] = random.choices(midground, midground_weights)[0]
    new_image ["Base"] = random.choices(base, base_weights)[0]
    new_image ["Hair"] = random.choices(hair, hair_weights)[0]
    new_image ["Eyelash"] = random.choices(eyelash, eyelash_weights)[0]
    new_image ["Clothes"] = random.choices(clothes, clothes_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


# TODO: check if unique before compiling
# Check if images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

# Add token id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1


# Get traits count 
background_count = {}
for item in background:
    background_count[item] = 0

midground_count = {}
for item in midground:
    midground_count[item] = 0

base_count = {}
for item in base:
    base_count[item] = 0

hair_count = {}
for item in hair:
    hair_count[item] = 0

eyelash_count = {}
for item in eyelash:
    eyelash_count[item] = 0

clothes_count = {}
for item in hair:
    clothes_count[item] = 0



for image in all_images:
    background_count[image["Background"]] += 1
    midground_count[image["Midground"]] +=1
    base_count[image["Base"]] +=1
    hair_count[image["Hair"]] +=1
    eyelash_count[image["Eyelash"]] += 1
    clothes_count[image["Clothes"]] += 1


print(background_count)
print(midground_count)
print(base_count)
print(hair_count)
print(eyelash_count)
print(clothes_count)

# Generate metadata
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


# Generate Image
for item in all_images:

    # Combine layers
    im1 = Image.open(f'./layers/background/{background_files[item["Background"]]}.png').convert('RGBA')
    try:
        im2 = Image.open(f'./layers/midground/{midground_files[item["Midground"]]}.png').convert('RGBA')
    except FileNotFoundError:
        im2 = ""
    im3 = Image.open(f'./layers/base/{base_files[item["Base"]]}.png').convert('RGBA')
    im4 = Image.open(f'./layers/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')

    try:
        im5 = Image.open(f'./layers/eyelash/{eyelash_files[item["Eyelash"]]}.png').convert('RGBA')
    except FileNotFoundError:
        im5 = ""

    im6 = Image.open(f'./layers/clothes/{clothes_files[item["Clothes"]]}.png').convert('RGBA')

    #Create each composite
    if im2 != "":
        com1 = Image.alpha_composite(im1, im2)
    else:
        com1 = im1
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    if im5 != "":
        com4 = Image.alpha_composite(com3,im5)
    else:
        com4 = com3
    com5 = Image.alpha_composite(com4,im6)

    #Convert to RGB
    rgb_im = com3.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)


# Generate Metadata for each image
f = open('./metadata/all-traits.json',) 
data = json.load(f)

IMAGES_BASE_URI = "baseurl/"
PROJECT_NAME = "Cyberu"


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Midground", i["Midground"]))
    token["attributes"].append(getAttribute("Base", i["Base"]))
    token["attributes"].append(getAttribute("Hair", i["Hair"]))
    token["attributes"].append(getAttribute("Eyelash", i["Eyelash"]))
    token["attributes"].append(getAttribute("Clothes", i["Clothes"]))

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()