import json
import pandas as pd
import os
from sys import argv
import shutil

images_folder = argv[1]
training_folder = argv[2]
print( images_folder, "====>", training_folder)

image_store = []
for folder in os.listdir(images_folder):
    folder_path = os.path.join(images_folder, folder)
    folder_images = os.listdir(folder_path)
    
    # Read Name of species
    xmls = [ x for x in folder_images if x[-3:] == 'xml']
    if len(xmls) > 0:
        detail = {}
        detail['code'] = folder
        detail['n_images'] = round(len(folder_images)/2)
        xml_path = os.path.join(folder_path, xmls[0])
        with open(xml_path, encoding="utf8") as f:
            xml = f.read()
        specie_name = xml.split('<Species>')[1].split('</Species>')[0].strip().lower()
        detail['name'] = specie_name
        image_store.append(detail)

df1 = pd.DataFrame(image_store)
df1.sort_values('n_images', ascending=False, inplace=True)

# training_folder = r'D:\PlantCLEF-TfLite\to_train'                       # path to save new training data
# Copy the filetered images to appropirate folder 
idx = 0
for i, row in df1.head(100).iterrows():                                 # taking a subset of PlantCLEF data with 100 species
    specie_folder = os.path.join(training_folder, row['name'])
    if not os.path.exists(specie_folder):
        os.mkdir(specie_folder)
    source_folder = os.path.join(images_folder, row['code'])
    for im in os.listdir(source_folder):
        src_path = os.path.join(source_folder, im)
        dst_path = os.path.join(specie_folder, im)
        shutil.copy(src_path, dst_path)
    idx+=1        