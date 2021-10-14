# from django.test import TestCase

# # Create your tests here.
# path = settings.MEDIA_ROOT +"/inference/"
#     os.chdir(path)
#     for file in os.listdir():
#         if file.endswith(".txt"):
#             file_path =  settings.MEDIA_ROOT + '/inference/' + file
#             break

#     with open(file_path, 'r'):
#     data = pd.read_csv(file_path, delim_whitespace=True, names = ['label','x1','y1','x2','y2'])
#     data_label=data['label'].to_list()


#     with open(r'/home/user4/Downloads/YOLO_OCR/data_typed.txt') as file:
  
#         data_list = yaml.load(file, Loader=yaml.FullLoader)
#     get_list=list(data_list.values())
#     single_list = reduce(lambda x,y: x+y, get_list)
#     list_label=[]
#     for sub_data in data_label:
#         for sub_index,sub_val in enumerate(single_list):
       
#             if sub_data == sub_index:
#                 list_label.append(sub_val)

#     df = pd.DataFrame({'new_col':list_label})

#     data['label']=df['new_col']

#     csv = data.to_csv(r'/home/user4/Downloads/YOLO_OCR/black&white/axis.csv', index = False)

#     data_list = []

#     data = pd.read_csv('/home/user4/Downloads/YOLO_OCR/black&white/axis.csv')
#     df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
#     Image1 = Image.open('/home/user4/Downloads/YOLO_OCR/black&white/axis.jpg') 
#     for ind in df.index: 
#         croppedIm = Image1.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))
#     results = pytesseract.image_to_string(croppedIm, lang = 'mcr')
#     head = {'label': data['label'][ind], 'Object': results}		
#     data_list.append(head)
#     df = pd.DataFrame(data_list, columns=['label','Object']) 
#     df.to_csv('/home/user4/Downloads/YOLO_OCR/black&white/axis_mcr_ocr.csv',index=False)
#     print("OCR is working")

# a = ["a", "boy", "ccat", "date", "e"]
# b = ["f", "g","bof" "hcst", "date", "j"]
# set(a) & set(b)
# data=[i for i, j in zip(a, b) if i == j]
# print(data)




