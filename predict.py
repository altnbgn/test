from mmcv import Config
from mmdet.models import build_detector
import mmcv
import matplotlib.pyplot as plt
from mmdet.apis import inference_detector, show_result_pyplot
from mmcv.runner import load_checkpoint
import os
import cv2
import numpy as np
import torch
from matplotlib.patches import Polygon
import pandas as pd
import time
from utils.preprocess import apply_preprocess
from utils.visualization import imshow_det_bboxes, bitmap_to_polygon, draw_result
from datetime import datetime


def Area(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area


def load_model(device='cpu', cfg_name='./configs/mask_rcnn_r50_caffe_fpn_mstrain-poly_1x_coco.py', checkpoint='./models/ot2_epoch_30.pth'):
    cfg = Config.fromfile(cfg_name)
    cfg.dataset_type = 'COCODataset'
    cfg.model.roi_head.bbox_head.num_classes = 1
    cfg.model.roi_head.mask_head.num_classes = 1
    cfg.gpu_ids = range(1)

    model = build_detector(cfg.model)
    checkpoint = load_checkpoint(model, checkpoint, map_location=device)
    model.CLASSES = ('rock',)
    model.cfg = cfg

    model.to(device)
    # Convert the model into evaluation mode
    model.eval()
    return model


def predict(model, img, THRESHOLD=0.5, AREA_THRESHOLD=1500, format='jpeg'):
    np_array = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    img = apply_preprocess(img)
    result = inference_detector(model, img)
    oversized = 0
    # show_result_pyplot(model, img, result, score_thr=THRESHOLD, out_file=os.path.join(save_path, filename))
    if isinstance(result, tuple):
        bbox_result, segm_result = result
        if isinstance(segm_result, tuple):
            segm_result = segm_result[0]  # ms rcnn
    else:
        bbox_result, segm_result = result, None
    
    bboxes = np.vstack(bbox_result)
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(bbox_result)
    ]
    labels = np.concatenate(labels)
    # draw segmentation masks
    segms = None
    if segm_result is not None and len(labels) > 0:  # non empty
        segms = mmcv.concat_list(segm_result)
        if isinstance(segms[0], torch.Tensor):
            segms = torch.stack(segms, dim=0).detach().cpu().numpy()
        else:
            segms = np.stack(segms, axis=0)
    
    # Area and region filtering
    polygons = []
    contours_list = []
    if segms is not None:
        for i, mask in enumerate(segms):
            contours, _ = bitmap_to_polygon(mask)
            polygons += [Polygon(c) for c in contours]
            contours_list += [c for c in contours]
    areas = [Area(x) for x in contours_list]
    areas_in_cm = [x*12.5 for x in areas]

    bboxes_dec = []
    areas_thresh = []
    bboxes_thresh = []
    c = 0
    for bbox in bboxes:
        bbox_rounded = [round(float(x), 2) for x in bbox]
        if bbox_rounded[4] > THRESHOLD:
            bboxes_dec.append(bbox_rounded)
            bboxes_thresh.append(bbox)
            areas_thresh.append(areas_in_cm[c])
        c += 1
    if len(bboxes_thresh) > 0:
        bboxes_thresh = np.vstack(bboxes_thresh)
        img = imshow_det_bboxes(img,
                        bboxes=bboxes,
                        labels=labels,
                        segms=segms,
                        class_names=('rock',),
                        score_thr=0.4,
                        bbox_color='green',
                        text_color='green',
                        mask_color=None,
                        thickness=2,
                        font_size=8,
                        win_name='',
                        show=False,
                        wait_time=0,
                        out_file=None)
        
        whs = [[round(abs(x[0] - x[2]), 1), round(abs(x[1] - x[3]), 1)] for x in bboxes_dec]
        whs_cm = [[x[0]*12.5, x[1]*12.5] for x in whs]
        
        bboxes_res = []
        c = 0
        for wh_cm in whs_cm:
            if wh_cm[0] > AREA_THRESHOLD or wh_cm[1] > AREA_THRESHOLD:
                oversized += 1
                bbox_int = bboxes_thresh[c].astype(np.int32)
                bboxes_res.append(bbox_int)
            c += 1
    
        img = draw_result(image=img, boxes=bboxes_res, text=str(oversized), timestamp=str(datetime.now()))
        # Encode the image in the specified format
    
    _, image_bytes = cv2.imencode('.' + format, img)

    # mmcv.imwrite(img, './test.png')
    return image_bytes.tobytes(), oversized


# img_dir = './examples'
# pred_save_path = 'results/'

# THRESHOLD = 0.5
# files = os.listdir(img_dir)
# c = 0
# model = load_model()
# res_list = []

# for filename in files:
#      if 'png' in filename or 'jpg' in filename:
#          c1 = 0

#          img = mmcv.imread(os.path.join(img_dir, filename))
#          start = time.time()
#          res_img, oversized = predict(model, img, pred_save_path, THRESHOLD, 1500)
#          mmcv.imwrite(res_img, './runs/'+filename)
#          print('Prediction:', c1, round(float(time.time() - start), 2))
#          c1 += 1
