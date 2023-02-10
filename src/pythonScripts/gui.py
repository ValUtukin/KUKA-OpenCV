from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
import threading


# def button_connect():
#     start_indicate('Connected to the server!')
#     # return 'Connected to the server!'
#
#
# def button_disconnect():
#     start_indicate('Disconnected :(')
#     # return 'Disconnected :('


# def start_indicate(button_response):
#     flag = False
#     if button_response == 'Connected to the server!':
#         print('Everthing\'s fine')
#         label = Label(frame, text='Everthing\'s fine', background='green', font=('Arial', 12))
#         label.place(relx=0.25, rely=0.4, relheight=0.1, relwidth=0.5)
#     else:
#         print('Not good')
#         label = Label(frame, text='Not good', background='red', font=('Arial', 12))
#         label.place(relx=0.25, rely=0.4, relheight=0.1, relwidth=0.5)
#     root.update()


# def get_xyz():
#     X = float(x.get())
#     Y = float(y.get())
#     Z = float(z.get())
#     print(f'X = {X}, Y = {Y}, Z = {Z}')


def camera_buttons():
    pass



def grab_frame_from_camera():
    video_capture = cv.VideoCapture(0)
    ret, frame = video_capture.read()
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img = Image.fromarray(cvimage)

    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)


root = Tk()

root['bg'] = '#F5BF0C'
root.title('KUKA Client')
root.geometry('1080x920')
photo = PhotoImage(file="../../images/robot.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=False)

camera_thread = threading.Thread(target=camera_buttons)
camera_thread.start()

camera_frame = Frame(root, bg='yellow')
camera_frame.place(relx=0.01, rely=0.01, height=360, width=640)

camera_buttons_frame = Frame(root, bg='green')
camera_buttons_frame.place(relx=0.61, rely=0.01, height=360, width=150)

canny_button = BooleanVar()

start_camera_button = Button(camera_buttons_frame, text='Start', bg='white')
start_camera_button.place(relx=0.01, rely=0.01, relheight=0.1, relwidth=0.25)
start_camera_button.getboolean(True)

label = Label(camera_frame)
label.grid(row=0, column=0)
print(canny_button)
root.mainloop()
