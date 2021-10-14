# import required classes
 
from PIL import Image, ImageDraw, ImageFont
import csv



# create Image object with the input image
 
image = Image.open('/home/dds/Documents/cheque_printing/Blank Cheque templet.png')

draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/home/dds/Documents/cheque_printing/arial-cufonfonts/ARIAL.TTF', size=50)


with open('/home/dds/Documents/cheque_printing/data/14.csv', 'r') as file:
    csv_file = csv.DictReader(file)
    for row1 in csv_file:
        if row1['label'] == "rupee_w2":
            h = int(row1['x1'])
            w = int(row1['y1'])
            (new_x, new_y) = (h,w)                                 
            print(new_x, new_y)

with open('/home/dds/Documents/cheque_printing/data/14.csv', 'r') as file:
    csv_file = csv.DictReader(file)
    for row in csv_file:
        if row['label'] == "rupee_w1":
            h = int(row['x1'])
            w = int(row['y1'])
            
            (x, y) = (h+150,w+5)
            Payee = "**fourty four fifty crore ninty thouasnd nine paise nine fifty eight zero only**"
            color = 'rgb(0, 0, 0)' # black color
            N = 55
            add_string = "-"
            if len(Payee) > 55:
                res = Payee[ : N] + add_string + Payee[N : ] 
                u = res.split("-")
                pri=(u[0]+'-')
                draw.text((x+150, y), pri, fill=color, font=font)
                
                # z="".join(str(x_n) for x_n in u)
                # print(z)
                #print(new_x,new_y)

                draw.text((new_x+150, new_y), u[1], fill=color, font=font)
            else:
                draw.text((x+150, y), Payee, fill=color, font=font)                   
                # print("h")


        elif row['label'] == "date":

            h = int(row['x1'])
            w = int(row['y1'])
            # (x, y) = (h-20,w+20)
            (x, y) = (h+100,w+10)
            Payee = "02122021"
            new_Payee=Payee.replace("", "  ")[1: -1]
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y), new_Payee, fill=color, font=font)
        elif row['label'] == "payee":
            Payee = "**Mayank**"
            val_height = round(int(row['x2'])-int(row['x1'])/2)
            val_width = round(int(row['y2'])-int(row['y1'])/2)
            (W, H) = (val_height,val_width+200)

            w, h = draw.textsize(Payee)

            #draw.text(((W-w)/2,(H-h)/2), msg, fill="black")
            
            color = 'rgb(0, 0, 0)' # black color
            draw.text(((W-w)/2,(H-h)/2),Payee, fill=color, font=font)

        # elif row['label'] == "rupee_w2":
        #     continue   

        elif row['label'] == "rupee_n":
            h = int(row['x1'])
            w = int(row['y1'])
        
            (x, y) = (h+150,w)
            Payee = "**2,585,07800/-**"
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y), Payee, fill=color, font=font)
        image.save('/home/dds/Documents/cheque_printing/printer/citi23.png', dpi=image.info['dpi'])

        
# from drf_multiple_model.views import ObjectMultipleModelAPIView
# from PIL import Image, ImageDraw, ImageFont
# class blankimage(APIView):
#     serializer_class = blankimgSerializer
#     def get(self, request,format=None):

#         image = Image.open('/home/dds/Documents/cheque_printing/Blank Cheque templet.png')

#         draw = ImageDraw.Draw(image)
#         font = ImageFont.truetype('/home/dds/Documents/cheque_printing/arial-cufonfonts/ARIAL.TTF', size=50)
        
#         # image = Image.open('/home/dds/Documents/cheque_printing/Blank Cheque templet.png')

#         snippets = pp_bankcrd_m.objects.all()
#         # for i in snippets:
#         #     print("===============++====",i.lable)
       
#         # # image_path=[]
#         # for i in snippets:
#         #     image_path.append(i.path_img_nm1.url)
#         for row1 in snippets:
#             if row1.lable == "rupee_w2":
#                 h = int(row1.bnkcrd_x1)
#                 w = int(row1.bnkcrd_y1)
#                 print("66666666666666666666",w)
#                 (new_x, new_y) = (h,w)                                 
#                 print('###########################333',new_x, new_y)
#         for row in snippets:
#             print('rrrrrrrrrrrrrrrrrrrr',row)
#             if row.lable == "rupee_w1":
#                 h = int(row.bnkcrd_x1)
#                 w = int(row.bnkcrd_y1)
#                 print("sssssssssssssssssssssssssssssss",w)
#                 (x, y) = (h+150,w+5)
#                 print("tttttttttttttttttttttt",x,y)
#                 Payee = "**fourty four fifty crore ninty thouasnd nine paise nine fifty eight zero only**"
#                 color = 'rgb(0, 0, 0)' # black color
#                 N = 55
#                 add_string = "-"
#                 if len(Payee) > 55:
#                     res = Payee[ : N] + add_string + Payee[N : ] 
#                     u = res.split("-")
#                     pri=(u[0]+'-')
#                     draw.text((x+150, y), pri, fill=color, font=font)

#                     draw.text((new_x+150, new_y), u[1], fill=color, font=font)
#                 else:
#                     draw.text((x+150, y), Payee, fill=color, font=font)

#             elif row.lable == "date":
    
#                 h = int(row.bnkcrd_x1)
#                 w = int(row.bnkcrd_y1)
#                 # (x, y) = (h-20,w+20)
#                 (x, y) = (h+100,w+10)
#                 print("GGGGGGGGGGGGGGGGGGGGGGGGGGg",x,y)
#                 Payee = "02122021"
#                 new_Payee=Payee.replace("", "  ")[1: -1]
#                 color = 'rgb(0, 0, 0)' # black color
#                 draw.text((x, y), new_Payee, fill=color, font=font)

#             elif row.lable == "payee":
#                 Payee = "**Mayank**"
#                 print("&&&&&&&&&&&&&&7777",Payee)
#                 val_height = round(int(row.bnkcrd_x2)-int(row.bnkcrd_x1)/2)
#                 val_width = round(int(row.bnkcrd_y2)-int(row.bnkcrd_y1)/2)
#                 (W, H) = (val_height,val_width+200)

#                 w, h = draw.textsize(Payee)
#                 print("ddddddddddddddddddddddddddddllll",w,h)

#                 #draw.text(((W-w)/2,(H-h)/2), msg, fill="black")
                
#                 color = 'rgb(0, 0, 0)' # black color
#                 print("$$$@@@@@@@@@@@@@@@@@@@@",draw.text(((W-w)/2,(H-h)/2),Payee, fill=color, font=font))

#             # elif row['label'] == "rupee_w2":
#             #     continue   

#             elif row.lable == "rupee_n":
#                 h = int(row.bnkcrd_x1)

#                 w = int(row.bnkcrd_y1)
            
#                 (x, y) = (h+150,w)
#                 Payee = "**2,585,07800/-**"
#                 color = 'rgb(0, 0, 0)' # black color
#                 draw.text((x, y), Payee, fill=color, font=font)
#                 # print(draw.Payee) 
#             image.save('/home/dds/Documents/cheque_printing/printer/citi787.png', dpi=image.info['dpi'])               
                 
#         # print("##############3",image_path)
#         serializer = blankimgSerializer(snippets, many=True)
#         return Response(serializer.data)





# class blankimage(APIView):
#     # authentication_classes = (SessionAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#     serializer_class = PpPymntTSerializer
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = PpPymntTSerializer(snippet)
#         return Response(serializer.data)




# class blankimage(APIView):
#     serializer_class = blankimgSerializer
#     def get_object(self, pk):
#         try:
#             return PpPymntT.objects.get(pk=pk)
#         except PpPymntT.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None,*args, **kwargs):
#     #    for genreate csv file
#         users = pp_bankcrd_m.objects.all()
#         imagedata=pp_bankcrd_m.objects.get(id=2)

#         imgdata=imagedata.path_img_nm1.url
#         removeslace=imgdata
#         removeslace=imgdata[1:]
#         image=Image.open((removeslace))

#         # image = Image.open('/home/dds/Documents/cheque_printing/Blank Cheque templet.png')

#         draw = ImageDraw.Draw(image)
#         font = ImageFont.truetype('/home/dds/Documents/cheque_printing/arial-cufonfonts/ARIAL.TTF', size=50)
    
#         # Create the HttpResponse object with the appropriate CSV header.
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="csv_database_write.csv"'
#         filename="csv_database_write.csv"

#         writer = csv.writer(response)
#         writer.writerow(['label', 'x1', 'y1', 'x2','y2'])

#         for user in users:
#             writer.writerow([user.label, user.x1, user.y1, user.x2,user.y2])
#         # with open('/home/dds/Documents/cheque_printing/data/14.csv', 'r') as file:    
#         with open('media/blankImg/csv_database_write.csv', 'r') as file:
#             csv_file = csv.DictReader(file)
#             for row1 in csv_file:
#                 if row1['label'] == "rupee_w2":
#                     h = int(row1['x1'])
#                     w = int(row1['y1'])
#                     (new_x, new_y) = (h,w)                                 
#                     print(new_x, new_y)

#         with open('/home/dds/Documents/cheque_printing/data/14.csv', 'r') as file:
#             csv_file = csv.DictReader(file)
#             for row in csv_file:
#                 finaldata=[]
#                 # paymentdata=PpPymntT.objects.all()
#                 paymentdata = self.get_object(pk)
#                 # serializer = masterbankSerializer(snippet)
#                 # return Response(serializer.data)



#                 print('##############3333444',paymentdata.pymnt_nm)
#                 if row['label'] == "rupee_w1":
#                     h = int(row['x1'])
#                     w = int(row['y1'])
#                     (x, y) = (h+150,w+5)
#                     Payee = "**fourty four fifty crore ninty thouasnd nine paise nine fifty eight zero only**"
#                     color = 'rgb(0, 0, 0)' # black color
#                     N = 55
#                     add_string = "-"
#                     if len(Payee) > 55:
#                         res = Payee[ : N] + add_string + Payee[N : ] 
#                         u = res.split("-")
#                         pri=(u[0]+'-')
#                         draw.text((x+150, y), pri, fill=color, font=font)
                
#                 # z="".join(str(x_n) for x_n in u)
#                 # print(z)
#                 #print(new_x,new_y)

               
#                         draw.text((new_x+150, new_y), u[1], fill=color, font=font)
#                     else:
#                         draw.text((x+150, y), Payee, fill=color, font=font)                   
#                 # print("h")


#                 elif row['label'] == "date":

#                     h = int(row['x1'])
#                     w = int(row['y1'])
#             # (x, y) = (h-20,w+20)
#                     (x, y) = (h+100,w+10)
                    
#                     Payee = str(paymentdata.pymnt_chq_dt)
#                     new_Payee=Payee.replace("", "  ")[1: -1]
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text((x, y), new_Payee, fill=color, font=font)
#                 elif row['label'] == "payee":
#                     Payee = paymentdata.pymnt_nm
#                     val_height = round(int(row['x2'])-int(row['x1'])/2)
#                     val_width = round(int(row['y2'])-int(row['y1'])/2)
#                     (W, H) = (val_height,val_width+200)

#                     w, h = draw.textsize(Payee)

#             #draw.text(((W-w)/2,(H-h)/2), msg, fill="black")
            
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text(((W-w)/2,(H-h)/2),Payee, fill=color, font=font)

#         # elif row['label'] == "rupee_w2":
#         #     continue   

#                 elif row['label'] == "rupee_n":
#                     h = int(row['x1'])
#                     w = int(row['y1'])
        
#                     (x, y) = (h+150,w)
#                     Payee =str(paymentdata.pymnt_chq_amt)
                   
#                     color = 'rgb(0, 0, 0)' # black color
#                     draw.text((x, y), Payee, fill=color, font=font)

  
 
#                 # image.save('/home/dds/Documents/cheque_printing/printer/citi5445.png', dpi=image.info['dpi'])

#                 image.save('media/blankImg/citi1.png',dpi=image.info['dpi'])

#         # serializer = blankimgSerializer(User, many=True)
#         serializer = blankimgSerializer(users, many=True)
#         return Response(serializer.data)  
