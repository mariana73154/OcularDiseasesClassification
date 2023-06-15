import os
import matplotlib.pyplot as plt

data_dir = "./dataset/"
#Get shape of the images 

#Get the path of the images
normal_images = os.listdir(os.path.join(data_dir, "normal"))
glaucoma_images = os.listdir(os.path.join(data_dir, "glaucoma"))
cataract_images = os.listdir(os.path.join(data_dir, "cataract"))
diabetic_retinopathy_images = os.listdir(os.path.join(data_dir, "diabetic_retinopathy"))

image_sizes = dict()

for image in normal_images:
    normal_image_path = os.path.join(data_dir, "normal", image)
    #Get the shape of the image
    normal_image = plt.imread(normal_image_path)
    if len(image_sizes.keys())==0 or normal_image.shape not in image_sizes.keys():
        image_sizes.update(
            {
                normal_image.shape : 1
            }
        )
    else:
        for key in image_sizes.keys():
            if key == normal_image.shape:
                image_sizes[key] += 1
                break

for image in glaucoma_images:
    glaucoma_image_path = os.path.join(data_dir, "glaucoma", image)
    #Get the shape of the image
    glaucoma_image = plt.imread(glaucoma_image_path)
    if len(image_sizes.keys())==0 or glaucoma_image.shape not in image_sizes.keys():
        image_sizes.update(
            {
                glaucoma_image.shape : 1
            }
        )
    else:
        for key in image_sizes.keys():
            if key == glaucoma_image.shape:
                image_sizes[key] += 1
                break

for image in cataract_images:
    cataract_image_path = os.path.join(data_dir, "cataract", image)
    #Get the shape of the image
    cataract_image = plt.imread(cataract_image_path)
    if len(image_sizes.keys())==0 or cataract_image.shape not in image_sizes.keys():
        image_sizes.update(
            {
                cataract_image.shape : 1
            }
        )
    else:
        for key in image_sizes.keys():
            if key == cataract_image.shape:
                image_sizes[key] += 1
                break

for image in diabetic_retinopathy_images:
    diabetic_retinopathy_image_path = os.path.join(data_dir, "diabetic_retinopathy", image)
    #Get the shape of the image
    diabetic_retinopathy_image = plt.imread(diabetic_retinopathy_image_path)
    if len(image_sizes.keys())==0 or diabetic_retinopathy_image.shape not in image_sizes.keys():
        image_sizes.update(
            {
                diabetic_retinopathy_image.shape : 1
            }
        )
    else:
        for key in image_sizes.keys():
            if key == diabetic_retinopathy_image.shape:
                image_sizes[key] += 1
                break

#Print the shape of the images and the count
for key in image_sizes.keys():
    print("Shape: " + str(key) + " - Count: " + str(image_sizes[key]))
