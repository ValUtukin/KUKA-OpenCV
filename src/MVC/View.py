from pubsub import pub
from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv
import src.pythonScripts.camera_actions as cam


class View:
    def __init__(self, parent):
        self.container = parent
        self.video_capture = cv.VideoCapture(0, cv.CAP_DSHOW)

    def setup(self):
        self.create_widgets()
        self.setup_layout()
        self.init_camera_first_frame()

    def create_widgets(self):
        self.camera_frame = Frame(self.container, bg='#09AD4B')
        self.camera_label = Label(self.camera_frame)

        self.camera_buttons_frame = Frame(self.container, height=365, width=200, bg='#36D5E7')
        self.check_camera_button = Button(self.camera_buttons_frame, text='Check Camera', command=self.check_camera)
        self.get_frame_button = Button(self.camera_buttons_frame, text='Grab frame', command=self.grab_frame)
        self.discard_frame_button = Button(self.camera_buttons_frame, text='Discard frame', command=self.discard_frame)

    def setup_layout(self):
        self.camera_frame.place(relx=0.01, rely=0.01)
        self.camera_label.pack(anchor="nw")
        self.camera_buttons_frame.place(relx=0.42, rely=0.01)
        self.check_camera_button.place(relx=0.05, rely=0.02)
        self.get_frame_button.place(relx=0.05, rely=0.12)
        self.discard_frame_button.place(relx=0.43, rely=0.12)

    def fit_image_into_label(self, image, rescale_flag=False, given_scale=0.5):
        if rescale_flag:
            img = cam.rescale_frame(image, scale=given_scale)
        else:
            img = image
        cvimage = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(cvimage)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

    def init_camera_first_frame(self):
        if self.video_capture.isOpened():
            initial_image = cam.rescale_frame(cv.imread("../../images/Camera_online.png"), scale=0.5)
        else:
            initial_image = cam.rescale_frame(cv.imread("../../images/Camera_offline.png"), scale=0.5)
        self.fit_image_into_label(initial_image)

    def check_camera(self):
        self.video_capture = cv.VideoCapture(0, cv.CAP_DSHOW)
        result = cam.grab_frame_from_camera(self.video_capture)
        if isinstance(result, str):
            if result == 'cannot open camera':
                initial_image = cam.rescale_frame(cv.imread("../../images/Camera_offline.png"), scale=0.5)
                self.fit_image_into_label(initial_image)
            elif result == 'no frame':
                print('no frame')
        else:
            initial_image = cam.rescale_frame(cv.imread("../../images/Camera_online.png"), scale=0.5)
            self.fit_image_into_label(initial_image)

    def grab_frame(self):
        capture = cv.VideoCapture(0, cv.CAP_DSHOW)
        cam.change_resolution(1280, 720, capture)
        img = cam.grab_frame_from_camera(capture)
        if isinstance(img, str):
            if img == 'cannot open camera':
                initial_image = cam.rescale_frame(cv.imread("../../images/Camera_offline.png"), scale=0.5)
                self.fit_image_into_label(initial_image)
            else:
                print(img)
        else:
            self.fit_image_into_label(img, rescale_flag=True, given_scale=0.3)

    def discard_frame(self):
        self.init_camera_first_frame()


if __name__ == '__main__':
    root = Tk()
    root['bg'] = '#0585e8'
    root.title('KUKA Client')
    root.geometry('1600x900')
    photo = PhotoImage(file="../../images/robotLogo.png")
    root.iconphoto(False, photo)
    root.resizable(width=False, height=True)

    view = View(root)
    view.setup()

    root.mainloop()
