def printedimgocr():
    path = settings.MEDIA_ROOT +"/inference/"
    os.chdir(path)
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path =  settings.MEDIA_ROOT + '/inference/' + file
            break

    with open(file_path, 'r'):
    data = pd.read_csv(file_path, delim_whitespace=True, names = ['label','x1','y1','x2','y2'])
    data_label=data['label'].to_list()


    with open(r'/home/user4/Downloads/YOLO_OCR/data_typed.txt') as file:
  
        data_list = yaml.load(file, Loader=yaml.FullLoader)
    get_list=list(data_list.values())
    single_list = reduce(lambda x,y: x+y, get_list)
    list_label=[]
    for sub_data in data_label:
        for sub_index,sub_val in enumerate(single_list):
       
            if sub_data == sub_index:
                list_label.append(sub_val)

    df = pd.DataFrame({'new_col':list_label})

    data['label']=df['new_col']

    csv = data.to_csv(r'/home/user4/Downloads/YOLO_OCR/black&white/axis.csv', index = False)



for ind in df.index: 
    data = pd.read_csv("axis.csv", index_col ="label")
    df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
    # put condition if label ==  ifsc_code , micr, txn_code, san # this is to read from cls.txt file 
    rows = data.loc[["ifsc_code", "micr", "txn_code", "san"]]
    # print(rows)
    rows.to_csv("temp/axis_mcr_lable_change.csv")


for ind in df.index: 
    data = pd.read_csv("axis.csv", index_col ="label")
    df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 

    # rows1 = data.loc[["date","customer_name","amount","account_number","bank_name","cheque_number","amount_words"]]
    rows1 = data.loc[['date','customer_name','amount','account_number','cheque_number','amount_words']]
    
    # print(rows1)
    rows1.to_csv("temp/axis_lable_change.csv")
  
data_list = []
#Read text file
data = pd.read_csv('temp/axis_mcr_lable_change.csv')
# df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 

# open the image 
Image = Image.open('2.jpeg') 

for ind in df.index: 
    # crop the image 
    croppedIm = Image.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))

    # results = pytesseract.image_to_string(croppedIm, lang='mcr')
    results = pytesseract.image_to_string(croppedIm)
 
 
    head = {'label': data['label'][ind], 'Object': results}
			# head = {'xmin': x, 'ymin': y, 'xmax': w, 'ymax': h, 'Object': text, 'label' :row['label'] }
    data_list.append(head)
			
	
df = pd.DataFrame(data_list, columns=['label','Object']) 
df.to_csv('axis_ocr_final_ocr.csv',index=False)

data_list1 = []
#Read text file
data1 = pd.read_csv('temp/axis_lable_change.csv')
# df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
df = pd.DataFrame(data1, columns = ['label','x1', 'y1', 'x2', 'y2']) 

# open the image 
# Image1 = Image.open('2.jpeg') 

for ind in df.index: 
    # crop the image 
    croppedIm1 = Image.crop((data1['x1'][ind], data1['y1'][ind], data1['x2'][ind],data1['y2'][ind]))

    resultss = pytesseract.image_to_string(croppedIm1)
 
    head = {'label': data1['label'][ind], 'Object': results}
			# head = {'xmin': x, 'ymin': y, 'xmax': w, 'ymax': h, 'Object': text, 'label' :row['label'] }
    data_list1.append(head)
			
	
df = pd.DataFrame(data_list1, columns=['label','Object']) 
df.to_csv('axis_ocr_final.csv','a',index=False)

with open(settings.MEDIA_ROOT+'/yolov5/exp106_yolov5s_results__written_cheque_5000/cls_wtrn_chq.txt') as file:








#########################################
def printedcheckcall(request,pk):
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
   
               

        # csv = data.to_csv(r'/home/user4/Downloads/YOLO_OCR/black&white/axis.csv', index = False)

    for ind in df.index:
        path = settings.MEDIA_ROOT +"/printedinfrence/"
        os.chdir(path)
        for file in os.listdir():
            if file.endswith(".txt"):
                file_path =  settings.MEDIA_ROOT + '/printedinfrence/' + file

                for file in os.listdir():
            
                    finalmerge=folder+file
                
                    print('***********************',finalmerge)
                    meargedata=os.path.splitext(finalmerge)[0]
                    labledata=(meargedata+'.csv') 

                    data = pd.read_csv(labledata, index_col ="label")
            df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
        # put condition if label ==  ifsc_code , micr, txn_code, san # this is to read from cls.txt file 
            rows = data.loc[["ifsc_code", "micr", "txn_code", "san"]]
        # print(rows)
            rows.to_csv(settings.MEDIA_ROOT+'/temp/axis_mcr_lable_change.csv')


    for ind in df.index: 
        data = pd.read_csv("axis.csv", index_col ="label")
        df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 

        # rows1 = data.loc[["date","customer_name","amount","account_number","bank_name","cheque_number","amount_words"]]
        rows1 = data.loc[['date','customer_name','amount','account_number','cheque_number','amount_words']]
        
        # print(rows1)
        rows1.to_csv("temp/axis_lable_change.csv")
    
    data_list = []
#Read text file
    data = pd.read_csv('temp/axis_mcr_lable_change.csv')
# df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
    df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 

# open the image 
    Image = Image.open('2.jpeg') 

    for ind in df.index: 
    # crop the image 
        croppedIm = Image.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))

        # results = pytesseract.image_to_string(croppedIm, lang='mcr')
        results = pytesseract.image_to_string(croppedIm)
    
    
        head = {'label': data['label'][ind], 'Object': results}
                # head = {'xmin': x, 'ymin': y, 'xmax': w, 'ymax': h, 'Object': text, 'label' :row['label'] }
        data_list.append(head)
			
	
    df = pd.DataFrame(data_list, columns=['label','Object']) 
    df.to_csv('axis_ocr_final_ocr.csv',index=False)

    data_list1 = []
    #Read text file
    data1 = pd.read_csv('temp/axis_lable_change.csv')
    # df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
    df = pd.DataFrame(data1, columns = ['label','x1', 'y1', 'x2', 'y2']) 

# open the image 
# Image1 = Image.open('2.jpeg') 

    for ind in df.index: 
        # crop the image 
        croppedIm1 = Image.crop((data1['x1'][ind], data1['y1'][ind], data1['x2'][ind],data1['y2'][ind]))

        resultss = pytesseract.image_to_string(croppedIm1)
    
        head = {'label': data1['label'][ind], 'Object': results}
                # head = {'xmin': x, 'ymin': y, 'xmax': w, 'ymax': h, 'Object': text, 'label' :row['label'] }
        data_list1.append(head)
                
	
    df = pd.DataFrame(data_list1, columns=['label','Object']) 
    df.to_csv('axis_ocr_final.csv','a',index=False)



####################################
