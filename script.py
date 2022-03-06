# Global variables
variations = 3 # number of variations for each trait
images_count = 10 # total number of images
layers = 3 # number of traits


#Function to generate a filename, with number of characters same to 
#number of layers, each character is a number, randomly selected 
#from 1 to the number of variations in each layer.
def generate_filename():
    name=””
    for i in range(layers):
         name=name+str(randint(1,variations))
    return name#List that will contain the filenames.files=[]

#Now dependent on how many images we want, we call the function to
#generate a filename and add it to out list if a similar filename 
#doesnt exist, this way we make sure all filenames are unique.
for i in range(images_count):
    name=generate_filename()
    if name not in files:
         files.append(name) 
         

from PIL import Image
from IPython.display import display


for item in files:
# loading the image from each layer
    layer1=Image.open(f’./1/{item[0]}.png’).convert(‘RGBA’)
    layer2=Image.open(f’./2/{item[1]}.png’).convert(‘RGBA’)
    layer3=Image.open(f’./3/{item[2]}.png’).convert(‘RGBA’)

# Now combining the layers
 
    com1 = Image.alpha_composite(layer1, layer2)
    com2 = Image.alpha_composite(com1, layer3)
 
    rgb_im = com2.convert(‘RGB’)
    file_name = item + “.png”
    rgb_im.save(“./images/” + file_name)

