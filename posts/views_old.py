from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView # new
# from django.urls import reverse_lazy # new

from .forms import PostForm # new
from .models import Post
from scanp import DocScanner1 
from scan import DocScanner
import shutil
import pytesseract
from django.http import HttpResponse, Http404
import itertools as it




from PIL import ImageFilter
import os
from e_checkapp.models import pp_path_m,PpPymntT,PpBnkM
from e_checkapp.serializers import masterbankSerializer
from django.conf import settings
from .serializers import printedcheckSerializer


def call():
    firstpost = PpBnkM.objects.last()
    print("firstpost ffffffffffffffffffffff",firstpost.cover)
    
    # path_test_image = "./media/" + str(firstpost.cover)
    path_test_image = settings.MEDIA_ROOT + '/' + str(firstpost.cover)
    print(path_test_image)
    scanner = DocScanner()
    valid_formats = [".jpg",".JPG",".jpeg","JPEG", ".jp2","JP2",".png","PNG",".bmp","BMP",".tiff","TIFF", ".tif"]
    get_ext = lambda f: os.path.splitext(f)[1].lower()
    print("get_ext", get_ext)
    scanner.scan(path_test_image)
    print("FINAL DONE")
    ocr()
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
# from  django.settings import MEDIA_ROOT
from django.conf import settings
from .models import Post
import csv
from uuid import getnode as get_mac

# #Read text file
# #Read text file

# #Read text file
# data_frame = pd.read_csv("test.txt", sep='\t', 
#                          names=['Name', 'Age', 'Profession']) 
  
#aftrer ML model genrated txt file
def ocr():

    path = settings.MEDIA_ROOT +"/inference/"
    os.chdir(path)
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
           
            print("######################################################",file_path)
            break
           
    with open(file_path, 'r'):
        # print(f.read())
        print(file_path)
        data = pd.read_csv(file_path, delim_whitespace=True, names = ['label','x1','y1','x2','y2'])  
        print(data)      

    data_label=data['label'].to_list()

    #Read class file (data.yaml)
    with open(settings.MEDIA_ROOT + '/yolov5/exp88_yolov5s_results_blank_cheque/cls.txt') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
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
           
            if sub_data == sub_index:
                list_label.append(sub_val)
    
        df = pd.DataFrame({'new_col':list_label})
        data['label']=df['new_col']
        folder = settings.MEDIA_ROOT + '/inference/'
        folder1 = settings.MEDIA_ROOT + '/CSV/'
        os.chdir(folder)
        print(os.listdir())


        for file in os.listdir():
            print(file)
            finalmerge=folder+file
            finalmerge1=folder1+file
            print('***********************',finalmerge)
            meargedata=os.path.splitext(finalmerge)[0]
            meargedata=os.path.splitext(finalmerge1)[0]
            labledata=(meargedata+'.csv')
           
            print("DDDDDDDDDDDDDDddddddd",labledata)
          
            data.to_csv(labledata, index = False)
            data.to_csv(labledata, index = False)
            print("FINAL DATA = \n", data)
            
            with open(labledata, newline='') as csvfile:
                print("OPEN CSV = ", csvfile)
                spamreader = csv.reader(csvfile, delimiter=';', quotechar=';')
                print(spamreader)
              

            
            

        
    
        print("OCR is working")


  

class HomePageView(ListView):
    model = Post
    template_name = 'home.html'


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from e_checkapp.serializers import PpPymntTSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated




class HomePageView(ListView):
    model = Post
    template_name = 'home.html'


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from e_checkapp.serializers import PpPymntTSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated




class model_form_upload(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class = masterbankSerializer
    def get(self, request, format=None):
        snippets = PpBnkM.objects.filter(usr_id=self.request.user)
        serializer = masterbankSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        mac = get_mac()
        serializer = masterbankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usr=self.request.user,entr_by=self.request.user,ip_addr=ip,mac_addr=mac)
            call()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


def printedcheckcall(request,pk):
    # user_login=request.user
    # print("VVVVVVVVVVVVVVVVV",user_login)
    print(request,pk)
    firstpost = PpPymntT.objects.get(pymnt_id=pk)
    print("firstpost ffffffffffffffffffffff",firstpost)
  
   
    # path_test_image = "./media/" + str(firstpost.cover)
    path_test_image = settings.MEDIA_ROOT + '/' + str(firstpost.priented_imag)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&",path_test_image)
    scanner = DocScanner1()
    valid_formats = [".jpg", ".jpeg", ".jp2", ".png", ".bmp", ".tiff", ".tif",".JPG",".JPEG",".JP2",".PNG",".TIFF",".TIF"]
    get_ext = lambda f: os.path.splitext(f)[1].lower()
    print("get_ext", get_ext)
    scanner.scanp(path_test_image)
    print("Priented FINAL DONE")
    printedocr()

def printedocr():
    path = settings.MEDIA_ROOT +"/printedinfrence/"
    os.chdir(path)
    print(os.listdir())
    # iterate through all file
    for file in os.listdir():
        print(file)
	# Check whether file is in text format or not
        if file.endswith(".txt"):
            print(file)
            # file_path = f"{path}{file}"
            print(settings.MEDIA_ROOT)
            file_path =  settings.MEDIA_ROOT + '/printedinfrence/' + file  
           
            print("######################################################",file_path)
         
           
    with open(file_path, 'r'):
        # print(f.read())
        print(file_path)
        data = pd.read_csv(file_path, delim_whitespace=True, names = ['label','x1','y1','x2','y2'])  
        print(data)      

    data_label=data['label'].to_list()

    #Read class file (data.yaml)
    with open(settings.MEDIA_ROOT+'/yolov5/exp106_yolov5s_results__written_cheque_5000/cls_wtrn_chq.txt') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
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
           
            if sub_data == sub_index:
                list_label.append(sub_val)
    
        df = pd.DataFrame({'new_col':list_label})
        data['label']=df['new_col']
        folder = settings.MEDIA_ROOT + '/printedinfrence/'
        

        folder1 = settings.MEDIA_ROOT + '/printedcsv/'
        if os.path.exists(folder1):
            shutil.rmtree(folder1)
            os.makedirs(folder1)
        os.chdir(folder)
        print(os.listdir())


        for file in os.listdir():
            print(file)
            finalmerge=folder+file
            finalmerge1=folder1+file
            print('***********************',finalmerge)
            meargedata=os.path.splitext(finalmerge)[0]
            meargedata=os.path.splitext(finalmerge1)[0]
            labledata=(meargedata+'.csv')
           
            print("DDDDDDDDDDDDDDddddddd",labledata)
          
            
            data.to_csv(labledata, index = False)
            print("FINAL DATA = \n", data)
   
               

        # csv = data.to_csv(r'/home/user4/Downloads/YOLO_OCR/black&white/axis.csv', index = False)


    for ind in df.index:
        print("@@@@@@@@@@@@@@@@@@",ind)
        path = settings.MEDIA_ROOT +"/printedcsv/"

        os.chdir(path)
        for file in os.listdir():
            if file.endswith(".csv"):
                print(file)
            # file_path = f"{path}{file}"
                print(settings.MEDIA_ROOT)
                file_path =  settings.MEDIA_ROOT + '/printedcsv/' + file  
           
                print("######################################################",file_path)
           
        with open(file_path, 'r'):
            data = pd.read_csv(file_path, index_col="label")
            print("ddddddddddddddddooooneee",data)
            # data = pd.read_csv(file_path, index_col ="label")
                    

            df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2'])
            print('&&&&&&&&&&&&&&&&&&77',df)
            print("HHHHHHHHHHHHHHHHHHHHHHHHHF%%%%") 
        # put condition if label ==  ifsc_code , micr, txn_code, san # this is to read from cls.txt file 
            rows = data.loc[["cheque_number", "micr", "txn_code", "san"]]
            print("%%%%%%%%%%%%%%%%%%%%%%%%^GGGGGGGGGGGGGGGGGGGGGGG")
            print("rows=", rows)

        
            folder = settings.MEDIA_ROOT + '/printedinfrence/'
            folder1 = settings.MEDIA_ROOT + '/temp/'
            if os.path.exists(folder1):  # output dir
             shutil.rmtree(folder1)  # delete dir
             os.makedirs(folder1)
            os.chdir(path)
            for file in os.listdir():
                print(file)
                finalmerge=folder+file
                finalmerge1=folder1+file
                print('***********************11',finalmerge)
                meargedata=os.path.splitext(finalmerge)[0]
                meargedata=os.path.splitext(finalmerge1)[0]
                labledata=(meargedata+'mcr.csv')
                    
                print("DDDDDDDDDDDDDDddddddd11",labledata)
                    
                data.to_csv(labledata, index = False)
                
                print("FINAL DATAttttttttttttt = \n", data)
                   
        # print(rows)
                rows.to_csv(labledata)


    for ind in df.index:
        print("@@@@@@@@@@@@@@@@@@",ind)
        path = settings.MEDIA_ROOT +"/printedcsv/"

        os.chdir(path)
        for file in os.listdir():
            if file.endswith(".csv"):
                print(file)
            # file_path = f"{path}{file}"
                print(settings.MEDIA_ROOT)
                file_path =  settings.MEDIA_ROOT + '/printedcsv/' + file  
           
                print("######################################################",file_path)
        with open(file_path, 'r'):
            data = pd.read_csv(file_path, index_col="label")
            print("another data is donennnnnnnnnnnnnnnnnnnnnn",data)
            
            print("another data list bbbbbbbbbbbbbbbbbbbbbgggtt",)
            df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2'])
            print("IIIIIIIIIIIIIIIIIIIIIIIII",df) 

        # rows1 = data.loc[["date","customer_name","amount","account_number","bank_name","cheque_number","amount_words"]]
            rows1 = data.loc[['cheque_number','micr','txn_code', 'san']]
        
        # print(rows1)
        folder = settings.MEDIA_ROOT + '/printedinfrence/'
        folder1 = settings.MEDIA_ROOT + '/temp/'
        os.chdir(path)
        for file in os.listdir():
                print(file)
                finalmerge=folder+file
                finalmerge1=folder1+file
                if os.path.exists(folder1):  # output dir
                    shutil.rmtree(folder1)  # delete dir
                    os.makedirs(folder1)
                print('***********************11',finalmerge)
                meargedata=os.path.splitext(finalmerge)[0]
                meargedata=os.path.splitext(finalmerge1)[0]
                labledata=(meargedata+'mcr.csv')
                rows1.to_csv(labledata)
    data_list = []
#Read text file
    path = settings.MEDIA_ROOT +"/temp/"

    os.chdir(path)
    for file in os.listdir():
        if file.endswith(".csv"):
            file_path =  settings.MEDIA_ROOT + '/temp/' + file  
           
        with open(file_path, 'r'):
            data = pd.read_csv(file_path) 
            df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2'])
            path = settings.MEDIA_ROOT +"/priendedoutput/"
            os.chdir(path)
            for file in os.listdir():
                if file.endswith(".jpg"):
                    print("file", file)
                    print(settings.MEDIA_ROOT)
                    file_path =  settings.MEDIA_ROOT + '/priendedoutput/' + file  
    #                 image = Image.open(file)
    # for ind in df.index: 
    #     cropped = image.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))
    #     weigth, height = cropped.size
    #     print( weigth, height)
    #     newsize = weigth*2, height*2
    #     croppedIm = cropped.resize(newsize)
    #     weigth, height = croppedIm.size
    #     print("newsize=", newsize)
    #     sharpened1 = croppedIm.filter(ImageFilter.SHARPEN)
                       # image = Image.open(file)
                    # image = cv2.imread(file)
    print(file)
    Image = Image.open(file) 
                    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # (thresh, image) = cv2.threshold(image, 100, 220, cv2.THRESH_BINARY)
                    # (thresh, image) = cv2.threshold(image, 110, 220, cv2.THRESH_BINARY)
                    # cv2.imwrite('image.jpeg',image)
    print("######################################################9695969",file_path)
    print("######################################&&&&&&&&&&&&&&&9695969",image)
                # with open(file_path, 'r'):
                #     # data = pd.read_csv(file_path)
                #     image = Image.open(file)
                #     print("dddddddddddddddddddonei11111111111111111",image)
    # Image = Image.open('2.jpeg') # read image from printed output 
    # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

    for ind in df.index: 
    # crop the image 
        # croppedIm = Image.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))
        # cropped = image.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))
        # cropped = cv2.(data['y1'][ind]:data['y2'][ind], data['x1'][ind]:data['x2'][ind])
        cropped = image[data['y1'][ind]:data['y2'][ind], data['x1'][ind]:data['x2'][ind]]
        height = cropped.shape[0]
        width = cropped.shape[1]
        newsize = width*2, height*2
        cropped = cv2.resize(cropped, (newsize))
        # cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        # (thresh, cropped) = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)
        # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        # cropped= cv2.filter2D(cropped, -1, kernel)
        # kernel = np.ones((5,5),np.uint8)
        # cropped = cv2.erode(cropped,kernel,iterations = 1) #  erosion
        # cropped = cv2.erode(cropped,kernel,iterations = 1)
        # cropped = cv2.erode(cropped,kernel,iterations = 1)
        # cropped = cv2.dilate(cropped,kernel,iterations = 1) #dilation
        # cropped = cv2.morphologyEx(cropped, cv2.MORPH_OPEN, kernel) # morphological transformation

        # cv2.imshow('crpd', cropped)
        # cv2.imwrite('cropped.jpg', cropped)
        
        

        results = pytesseract.image_to_string(cropped , lang= 'mcr')
        head = {'label': data['label'][ind], 'Object': results}
        data_list.append(head)
    df = pd.DataFrame(data_list, columns=['label','Object']) 
    folder = settings.MEDIA_ROOT + '/printedinfrence/'
    folder1 = settings.MEDIA_ROOT + '/temp/'
    os.chdir(path)
    for file in os.listdir():
            print(file)
            finalmerge=folder+file
            finalmerge1=folder1+file
            meargedata=os.path.splitext(finalmerge)[0]
            meargedata=os.path.splitext(finalmerge1)[0]
            labledata=(meargedata+'mcr.csv')
            df.to_csv(labledata)
    data_list1 = []
    path = settings.MEDIA_ROOT +"/temp/"

    os.chdir(path)
    for file in os.listdir():
        if file.endswith(".csv"):
            print(file)
            print(settings.MEDIA_ROOT)
            file_path =  settings.MEDIA_ROOT + '/temp/' + file  
        with open(file_path, 'r'):
            data1 = pd.read_csv(file_path)
            df = pd.DataFrame(data1, columns = ['label','x1', 'y1', 'x2', 'y2']) 
            path = settings.MEDIA_ROOT +"/priendedoutput/"

            os.chdir(path)
            for file in os.listdir():
                if file.endswith(".jpg"):
                    print("file", file)
                    print(settings.MEDIA_ROOT)
                    file_path =  settings.MEDIA_ROOT + '/priendedoutput/' + file  
                    image = Image.open(file)
                  
                  
class printedcheckupdate(APIView):
    """
    Retrieve, update or delete a org instance.
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = printedcheckSerializer
    parser_classes = (MultiPartParser, FormParser)
    def get_object(self, pk):
        try:
            return PpPymntT.objects.get(pk=pk)
        except PpPymntT.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = printedcheckSerializer(snippet)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        print("4444444$$$$$$$$$$$$$444",snippet,request.data,pk)
        serializer = printedcheckSerializer(snippet, data=request.data)
        if serializer.is_valid():          
            serializer.save()
        printedcheckcall(request,pk)
        path = settings.MEDIA_ROOT +"/temp/"
        os.chdir(path)
        print(os.listdir())
        for file in os.listdir():
            print(file)
            if file.endswith(".csv"):
                print(file)
                print(settings.MEDIA_ROOT)
                file_path =  settings.MEDIA_ROOT + '/temp/' + file  
        with open(file_path, 'r')as file:
            csv_reader = csv.DictReader(file)
            line_count = 0
            data_list=[]
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                data=(f'\t{row["Object"]}')
                data_list.append(data)
                line_count += 1
            PpPymntT.objects.filter(pymnt_id=snippet.pymnt_id).update(PYMNT_CHQ_MICR=data_list[0],PYMNT_CHQ_ACCID=data_list[1],PYMNT_CHQ_TRNSID=data_list[2],PYMENT_CHQ_NO=data_list[3])
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5")
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
