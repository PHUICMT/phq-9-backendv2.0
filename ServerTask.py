import os
import io
import cv2, base64
import json
import numpy as np
import glob
import re

class DirectoryTask:
        
    @staticmethod
    def create_image_directory(saved_image_path):
        try:
            if not os.path.exists(saved_image_path):
                os.makedirs(saved_image_path)
        except:
            print("[ERROR] Fail to creating directory. " + saved_image_path)   
        return saved_image_path
        
    @staticmethod
    def create_video_directory(saved_video_path):
        try:
            if not os.path.exists(saved_video_path):
                os.makedirs(saved_video_path)
        except:
            print("[ERROR] Fail to creating directory. " + saved_video_path)   
        return saved_video_path

class FileTask:
    
    @staticmethod
    def save_image(image_path, image_base64):
        img_file = open(image_path, 'wb')
        img_file.write(image_base64)
        img_file.close()

    @staticmethod
    def save_video(saved_image_path, saved_video_path):
        img_array = []
        numbers = re.compile(r'(\d+)')

        def numericalSort(value):
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts
        
        for filename in sorted(glob.glob(saved_image_path + "/*.jpg"), key=numericalSort):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
        out = cv2.VideoWriter(saved_video_path,cv2.VideoWriter_fourcc(*'DIVX'), 25, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

class GeneralTask:
    
    @staticmethod
    def get_image_path(user_data):
        image_path = "./images_storage/"
        user_email = user_data['user_email']
        user_id = user_data['user_id']
        saved_image_path = image_path + user_email + "_" + user_id
        return saved_image_path

    @staticmethod
    def get_video_path(user_data):
        video_path = "./videos_storage/"
        user_email = user_data['user_email']
        user_id = user_data['user_id']
        saved_video_path = video_path + user_email + "_" + user_id
        return saved_video_path

    
