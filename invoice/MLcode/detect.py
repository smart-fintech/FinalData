import argparse
import os
import shutil
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh,strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized
from sys import path

from django.conf import settings
import pandas as pd
import yaml
from functools import reduce
from PIL import Image 
import pandas as pd
import cv2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
def latestcode():
    def detect(save_img=False):
        out, source, weights, view_img, save_txt, imgsz = \
            opt.save_dir, opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
        webcam = source.isnumeric() or source.startswith(('rtsp://', 'rtmp://', 'http://')) or source.endswith('.txt')
        set_logging()
        device = select_device(opt.device)
        if os.path.exists(out):  # output dir
            shutil.rmtree(out)  # delete dir
        os.makedirs(out)  # make new dir
        half = device.type != 'cpu'  # half precision only supported on CUDA
        model = attempt_load(weights, map_location=device)  # load FP32 model
        imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
        if half:
            model.half()  # to FP16
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
            modelc.to(device).eval()
        vid_path, vid_writer = None, None
        if webcam:
            view_img = True
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz)
        else:
            save_img = True
            dataset = LoadImages(str(settings.BASE_DIR)+'/invoice/MLcode/'+source, img_size=imgsz)
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
        t0 = time.time()
        img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
        _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            t1 = time_synchronized()
            pred = model(img, augment=opt.augment)[0]
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
            t2 = time_synchronized()
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)
                print("Prediction =", pred)
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
                else:
                    p, s, im0 = path, '', im0s

                save_path = str(Path(out) / Path(p).name)
                txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if det is not None and len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %ss, ' % (n, names[int(c)])  # add to string
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                        
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist() # normalized xywh
                            label = '%s %.2f' % (names[int(cls)], conf)
                            line = (cls, conf, *xyxy) if opt.save_conf else (cls, *xyxy)  # label format
                            with open(txt_path + '.txt', 'a') as f:
                                f.write(('%g ' * len(line) + '\n') % line)

                            if save_img or view_img:  # Add bbox to image
                                label = '%s %.2f' % (names[int(cls)], conf)
                                pred_class = '%s' % (names[int(cls)])
                print('%sDone. (%.3fs)' % (s, t2 - t1))

                if view_img:
                    cv2.imshow(p, im0)
                    if cv2.waitKey(1) == ord('q'):  # q to quit
                        raise StopIteration
                if save_img:
                    if dataset.mode == 'images':
                        cv2.imwrite(save_path, im0)
                    else:
                        if vid_path != save_path:
                            vid_path = save_path
                            if isinstance(vid_writer, cv2.VideoWriter):
                                vid_writer.release()
                            fourcc = 'mp4v'
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                        vid_writer.write(im0)
        if save_txt or save_img:
            print('Results saved to %s' % Path(out))
        print('Done. (%.3fs)' % (time.time() - t0))
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=str(settings.BASE_DIR)+'/invoice/MLcode/media/exp62_results_invoice/weights/best.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='output', help='source')
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt',  type=str, default='inference/output', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-dir', type=str, default='inference/output', help='directory to save results')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('runserver', default='', help='runserver')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()
    print("detect is working")
    data = pd.read_csv(str(settings.BASE_DIR)+'/invoice/MLcode/inference/output/test1.txt', delim_whitespace=True, names = ['label','x1','y1','x2','y2'])
    data_label=data['label'].to_list()
    with open(str(settings.BASE_DIR)+'/invoice/MLcode/media/exp62_results_invoice/cls.txt') as file:
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
    csv = data.to_csv(r'inference/output/test1.csv', index = False)
    print("OCR is working")
    data_list = []
    data = pd.read_csv('inference/output/test1.csv')
    df = pd.DataFrame(data, columns = ['label','x1', 'y1', 'x2', 'y2']) 
    Image1 = Image.open('inference/output/test1.jpeg') 
    for ind in df.index: 
        croppedIm = Image1.crop((data['x1'][ind], data['y1'][ind], data['x2'][ind],data['y2'][ind]))
        results = pytesseract.image_to_string(croppedIm)
        head = {'label': data['label'][ind], 'Object': results}
        data_list.append(head)	
    df = pd.DataFrame(data_list, columns=['label','Object']) 
    df.to_csv(str(settings.BASE_DIR)+'/invoice/MLcode/temp/ocr.csv',index=False)
    new_df=pd.read_csv('/home/user/Music/FinalProject-master/invoice/MLcode/temp/ocr.csv')
    df=new_df.T
    df.columns = df.iloc[0]
    df = df[1:]
    df.to_csv(str(settings.BASE_DIR)+'/invoice/MLcode/temp/newocr.csv',index=False)