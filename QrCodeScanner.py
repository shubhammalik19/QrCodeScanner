#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
from pyzbar import pyzbar
import shutil
import json

class QrCodeScanner():
    def __init__(self, path):
        self.path = path
        self.dir_list = os.listdir(path)
        self.qrCodeFolder = "./detected"
        self.undetected = "./undetected"
        self.createFolder()
        shutil.copy("ReNameErSoftware.exe",self.undetected)
        self.scan()

    def scan(self):
        for image in self.dir_list:
            self.moveFile( os.path.join(self.path,image) )
    
    def preProcess(self, image):
        img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        _, img = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
        return img
    def read_qr_code(self, filename):
        try:
            img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            img = self.preProcess(filename)
            qrCode = pyzbar.decode(img)
            if qrCode:
                qrCode = qrCode[0].data.decode('utf-8')
            else:
                qrCode = ''
            return qrCode
        except:
            return
    
    def createFolder(self):
        if os.path.exists(self.qrCodeFolder):
            shutil.rmtree(self.qrCodeFolder, ignore_errors=False)
        os.mkdir(self.qrCodeFolder)
    
        if os.path.exists(self.undetected):
            shutil.rmtree(self.undetected, ignore_errors=False)
        os.mkdir(self.undetected)
    
    def moveFile(self, image):
        qrCode = self.read_qr_code(image)
        if qrCode != '':
            #if qrCode is of json in formate
            if qrCode.startswith("{") and qrCode.endswith("}") and "gr_no" in qrCode :
                qrCode = json.loads(qrCode)
                qrCode = qrCode["gr_no"]
            elif qrCode.startswith("[") and qrCode.endswith("]") and "gr_no" in qrCode :
                qrCode = json.loads(qrCode)
                qrCode = qrCode[0]["gr_no"]
            elif qrCode.startswith("http"):
                qrCode = qrCode.split("/")[-1]
                 #cheack if qrCode is not a date
                if qrCode.isdigit(): #if qrCode is a date
                    qrCode = qrCode.split("_")[1]
            #el if qrCode is of string and conatins a sperator _ SPLIT fist part for qrcode
            elif "_" in qrCode:
                qrCode = qrCode.split("_")[0] 
                #cheack if qrCode is not a date
                if qrCode.isdigit(): #if qrCode is a date
                    qrCode = qrCode.split("_")[1]
            else:
                qrCode = qrCode

            extension = os.path.splitext(image)[1]
            dst_dir = self.qrCodeFolder + "/" + str(qrCode) + extension
        else:
            dst_dir = self.undetected + "/" + os.path.basename(image)
        try:
            print(f"Moving {image} To {dst_dir}")
            shutil.copy(image, dst_dir)
        except EnvironmentError:
            print("Unable to copy file.")

if __name__ == "__main__":
    path = "./read"
    QrCodeScanner(path)