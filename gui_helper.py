from tkinter import *


class GuiHelper:
    @staticmethod
    def show(title: str, text: str):
        root = Tk()
        root.title(title)
        lb2 = Label(root, text=text)
        lb2.pack()
        btn = Button(root, text="Close", command=lambda: root.destroy())
        btn.pack()
        mainloop()


if __name__ == "__main__":
    GuiHelper.show("Title", "Text")
