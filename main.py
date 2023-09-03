from PIL import Image, ImageGrab
from pyautogui import alert, prompt
import pyautogui
from pynput import mouse
from gui_helper import GuiHelper
import os
from time import sleep
from threading import Thread
import img2pdf

GAP_TIME = 2

LEFT_TOP = "leftTop"
RIGHT_BOTTOM = "rightBottom"
NEXT_BUTTON = "nextButton"


class app:
    def __init__(self):

        self.pageCount = int(
            prompt(title="Number of pages", text="Enter the number of pages and click ok"))
        if self.pageCount == 0:
            alert("The number of pages cannot be 0", "Error")
            exit()
        alert("When you close this message, clicks will start.\nThe first click should be at the top left corner of the page\nThe second click is at the bottom right corner of the page\nThe third click should be the next button.", "Info")
        if not os.path.exists("Images"):
            try:
                os.mkdir("Images")
            except OSError as e:
                alert(
                    "An error occurred while creating the folder.\nPlease try again.", "Error")
                exit()

        self.data = {}

    def runAsync(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            self.listener = listener
            listener.join()

    def startProcessing(self):
        counter = 0
        try:
            while counter < self.pageCount:
                path = "Images/"+str(counter)+".jpeg"
                self.saveImage(path)
                self.nextPage()
                counter += 1
            self.convert_image_to_pdf()
            sleep(GAP_TIME)
            exit()
        except Exception as e:
            alert("An error occurred while saving the image.\nPlease try again.", "Error")
            print(e)
            exit()


    def saveImage(self, path):
        ImageGrab.grab().save(path)
        img = Image.open(path)

        leftTopX = self.data[LEFT_TOP][0]
        leftTopY = self.data[LEFT_TOP][1]
        rightBottomX = self.data[RIGHT_BOTTOM][0]
        rightBottomY = self.data[RIGHT_BOTTOM][1]

        width = rightBottomX - leftTopX
        height = rightBottomY - leftTopY

        box = (leftTopX, leftTopY, rightBottomX, rightBottomY)
        cropped_img = img.crop(box=box)
        cropped_img.save(path)

    def nextPage(self): 
        position = self.data[NEXT_BUTTON]
        print(position)
        Thread(target=pyautogui.click, args=(position[0],position[1])).start()     
        sleep(GAP_TIME) 

    def on_click(self, x, y, button, pressed):
        if pressed:
            if str(button) == "Button.left":
                if len(self.data) == 0:
                    self.data[LEFT_TOP] = (x, y)
                elif len(self.data) == 1:
                    self.data[RIGHT_BOTTOM] = (x, y)
                elif len(self.data) == 2:
                    self.data[NEXT_BUTTON] = (x, y)
                elif len(self.data) == 3:
                    self.listener.stop()
                    self.startProcessing()
                
    def convert_image_to_pdf(self):
        list = []
        if not os.path.exists("PDF"):
            try:
                os.mkdir("PDF")
            except OSError as e:
                alert(
                    "An error occurred while creating the folder.\nPlease try again.", "Error")
                exit()
        for i in range(self.pageCount):
            list.append("Images/"+str(i)+".jpeg")
        with open("PDF/output.pdf", "wb") as f:
            f.write(img2pdf.convert(list))

if __name__ == "__main__":
    app().runAsync()

