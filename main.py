from PIL import Image, ImageGrab
from pyautogui import alert, prompt
from pynput import mouse
from gui_helper import GuiHelper
import os
from time import sleep

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
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def startProcessing(self):
        path = "Images/"+str(self.pageCount)+".jpeg"
        counter = 0
        while counter < self.pageCount:
            self.saveImage(path)
            self.nextPage()
            counter += 1

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
        mouse.position = self.data[NEXT_BUTTON]
        mouse.click(button="left")
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
                    GuiHelper.show(
                        title="Info", text=f"Starting the save process.\nFolder to save: {os.getcwd()}/Images")
                    self.startProcessing()
                    self.listener.stop()


if __name__ == "__main__":
    app().runAsync()
