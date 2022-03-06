from PIL import Image 
from IPython.display import display 
import random
import json


# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["1", "2","3","4","5"] 
background_weights = [20, 20, 20, 20, 20]

midground = ["1"]
midground_weights = [100]

base = ["1","2","3"]
base_weights = [50,25,25]

hair = ["1","2","3"]
hair_weights = [25,50,50]


# circle = ["Blue", "Orange"] 
# circle_weights = [30, 70]

# square = ["Blue","Orange"] 
# square_weights = [30, 70]


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




# square_files = {
#     "Blue": "blue-square",
#     "Orange": "orange-square",     
# }

# circle_files = {
#     "Blue": "blue-circle",
#     "Orange": "orange-circle", 
# }


TOTAL_IMAGES = 15 # Number of random unique images we want to generate ( 5 x 1 x 3 x 3 = 15)

all_images = [] 

def create_new_image():

    new_image = {} #

    # For each trait category, select a random trait based on the weightings 
    new_image ["Background"] = random.choices(background, background_weights)[0]
    new_image ["Midground"] = random.choices(midground, midground_weights)[0]
    new_image ["Base"] = random.choices(base, base_weights)[0]
    new_image ["Hair"] = random.choices(hair, hair_weights)[0]
    # new_image ["Circle"] = random.choices(circle, circle_weights)[0]
    # new_image ["Square"] = random.choices(square, square_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES): 

    new_trait_image = create_new_image()

    all_images.append(new_trait_image)


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



for image in all_images:
    background_count[image["Background"]] += 1
    midground_count[image["Midground"]] +=1
    base_count[image["Base"]] +=1
    hair_count[image["Hair"]] +=1


print(background_count)
print(midground_count)
print(base_count)
print(hair_count)

# Generate metadata
METADATA_FILE_NAME = './metadata/all-traits.json'; 
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)


# Generate Image
for item in all_images:

    im1 = Image.open(f'./layers/background/{background_files[item["Background"]]}.png').convert('RGBA')
    im2 = Image.open(f'./layers/midground/{circle_files[item["Midground"]]}.png').convert('RGBA')
    im3 = Image.open(f'./layers/base/{square_files[item["Base"]]}.png').convert('RGBA')
    im4 = Image.open(f'./layers/hair/{square_files[item["Hair"]]}.png').convert('RGBA')

    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)

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

    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()