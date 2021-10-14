#Libraries implementation
import pandas as pd
import yaml
from functools import reduce
from PIL import Image 
import pandas as pd
import cv2
import imutils
from PIL import Image
import os
from django.conf import settings
from .models import Post

# #Read text file
# #Read text file

# #Read text file
# data_frame = pd.read_csv("test.txt", sep='\t', 
#                          names=['Name', 'Age', 'Profession']) 
  
#aftrer ML model genrated txt file
def ocr():
    ##########################
    # Import Module
    

    # Folder Path
    path = "./media/inference/"

    # Change the directory
    os.chdir(path)

    # Read text File


    # def read_text_file(file_path):
        
    

    print(os.listdir())
    # iterate through all file
    for file in os.listdir():
        print(file)
	# Check whether file is in text format or not
        if file.endswith(".txt"):
            print(file)
            # file_path = f"{path}{file}"
            print(settings.MEDIA_ROOT)
            file_path =  settings.MEDIA_ROOT + '/inference/' + file  
            print(file_path)
            break
           
    with open(file_path, 'r'):
        # print(f.read())
        print(file_path)
        data = pd.read_csv(file_path, delim_whitespace=True, names = ['label','x1','y1','x2','y2'])  
        print(data)      


		# call read text file function
            # read_text_file(file_path)


        ##########################

    # data = pd.read_csv(r'./inference/output/1.txt', delim_whitespace=True, names = ['label','x1','y1','x2','y2'])
    #Convert label column into list
    data_label=data['label'].to_list()

    #Read class file (data.yaml)
    with open(settings.MEDIA_ROOT + '/yolov5/exp88_yolov5s_results_blank_cheque/cls.txt') as file:
       
        data_list = yaml.load(file, Loader=yaml.FullLoader)
        #print(data_list)

    # Get the data into list format
    get_list=list(data_list.values())
    # print(get_list)
    #Convert data into single list
    single_list = reduce(lambda x,y: x+y, get_list)
    # print(single_list)
    #Store data into this temporary list
    list_label=[]

    #Logic to match text file and class file to extract each label class
    for sub_data in data_label:
        for sub_index,sub_val in enumerate(single_list):
            # print(sub_index,sub_val)
            if sub_data == sub_index:
                list_label.append(sub_val)
    # print(list_label)
    #create new dataframe 
        df = pd.DataFrame({'new_col':list_label})
        # print(df)
        #Replace label with new dataframe  
        data['label']=df['new_col']
        # print(data)
        ##################################################################
        folder = settings.MEDIA_ROOT + '/inference/'
        os.chdir(folder)
        print(os.listdir())
        for file in os.listdir():
            print(file)
            finalmerge=folder+file
            print('***********************',finalmerge)
            meargedata=os.path.splitext(finalmerge)[0]
            print("DDDDDDDDDDDDDDddddddd",meargedata) 
        
        ######################################################################
        #Create a new csv file with extracting data
            csv = data.to_csv(meargedata+'.csv')
            data=csv.label
            # data=Post.objects.all()
            print("pppppppppppppppppppppppp",data)
        print("OCR is working",csv)
            

    # def imagepath():
    #     image_path = 'inference/output/1.csv'
    #     return image_path
    #import printer
