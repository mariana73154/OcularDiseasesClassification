import os
import cv2
import matplotlib.pyplot as plt

input_path = './dataset/'
output_path = './dataPreprocessed/'

#create output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

#input data as 2 folders: 'Normal' and 'Glaucoma'
for folder in os.listdir(input_path):
    print ('Processing ' + folder + ' folder')
    #create output directory if it doesn't exist
    if not os.path.exists(output_path + folder):
        os.makedirs(output_path + folder)
    #input data as images
    for image in os.listdir(input_path + folder):
        #if image exist in output folder, skip
        if os.path.exists(output_path + folder + '/' + image) or image == 'InfoShape.txt':
            continue
        else :
            imageCop = plt.imread(input_path + folder + '/' + image)
            #read image
            img = cv2.imread(input_path + folder + '/' + image)
            #print image name and shape
            print (image + ' ' + str(imageCop.shape))
            #resize image
            img = cv2.resize(img, (1024, 1024), interpolation = cv2.INTER_AREA)
            #save image
            cv2.imwrite(output_path + folder + '/' + image, img)    
            
