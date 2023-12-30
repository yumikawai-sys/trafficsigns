import os
import random
# from road_sign_predict import Road_Sign_Predict
from model_load import sign_prediction

folder_path = "test_images"

# List all files and find png files from test_images folder
def random_image():
    file_list = os.listdir(folder_path)
    png_files = [file for file in file_list if file.lower().endswith(".png")]

    if png_files:
        random_file = random.choice(png_files)
        random_file_path = os.path.join(folder_path, random_file)

        print("chosen file:", random_file_path)
    else:
        print("No PNG files")
        
    prediction = sign_prediction(random_file_path)
    print("predicted sign is: ", prediction)
    result = [random_file_path, prediction]
    return result

random_image()
