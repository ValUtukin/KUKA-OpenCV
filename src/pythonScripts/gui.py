from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
import threading


def button_connect():
    start_indicate('Connected to the server!')
    # return 'Connected to the server!'


def button_disconnect():
    start_indicate('Disconnected :(')
    # return 'Disconnected :('


def start_indicate(button_response):
    flag = False
    if button_response == 'Connected to the server!':
        print('Everthing\'s fine')
        label = Label(frame, text='Everthing\'s fine', background='green', font=('Arial', 12))
        label.place(relx=0.25, rely=0.4, relheight=0.1, relwidth=0.5)
    else:
        print('Not good')
        label = Label(frame, text='Not good', background='red', font=('Arial', 12))
        label.place(relx=0.25, rely=0.4, relheight=0.1, relwidth=0.5)
    root.update()


def get_xyz():
    X = float(x.get())
    Y = float(y.get())
    Z = float(z.get())
    print(f'X = {X}, Y = {Y}, Z = {Z}')


def create_camera_thread():
    camera_thread.start()


def grab_frame_from_camera():
    video_capture = cv.VideoCapture(0)
    ret, frame = video_capture.read()
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img = Image.fromarray(cvimage)

    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)


def stop_live_video():
    global stop_flag
    stop_flag = True
    camera_thread.join()


def live_video_stream():
    global stop_flag
    video_capture = cv.VideoCapture(0)
    while not stop_flag:
        ret, img = video_capture.read()
        cvimage = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = Image.fromarray(cvimage)

        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)


root = Tk()

root['bg'] = '#ffffff'
root.title('KUKA Client')
root.geometry('1080x920')
photo = PhotoImage(file="../../images/robot.png")
root.iconphoto(False, photo)
root.resizable(width=False, height=True)

stop_flag = False
# oval = canvas.create_oval(300, 300, 400, 400)

camera_frame = Frame(root, bg='yellow')
camera_frame.place(relx=0.05, y=330, height=485, width=645)

label = Label(camera_frame)
label.grid(row=0, column=0)

start_camera_button = Button(root, text='Start', bg='white', command=create_camera_thread)
start_camera_button.place(relx=0.05, y=820, relheight=0.05, relwidth=0.1)

camera_thread = threading.Thread(target=live_video_stream)

stop_camera_button = Button(root, text='Stop', bg='white', command=stop_live_video)
stop_camera_button.place(relx=0.2, y=820, relheight=0.05, relwidth=0.1)

frame = Frame(root, bg='#407DED')
frame.place(relx=0.05, rely=0.05, relheight=0.3, relwidth=0.5)

title = Label(frame, text='Start from here!', background='#0033FF', font=('Arial', 12, 'bold'))
title.pack()

btn_connect = Button(frame, text='Connect', bg='green', command=button_connect)
btn_connect.place(relx=0.1, rely=0.25, relheight=0.15, relwidth=0.2)

btn_disconnect = Button(frame, text='DisConnect', bg='red', command=button_disconnect)
btn_disconnect.place(relx=0.68, rely=0.25, relheight=0.15, relwidth=0.22)

Label(frame, text='X', background='#407DED', font=('Arial', 12)).place(relx=0.05, rely=0.6, relheight=0.1)
x = Entry(frame, width=7)
x.place(relx=0.1, rely=0.6, relheight=0.1)

Label(frame, text='Y', background='#407DED', font=('Arial', 12)).place(relx=0.25, rely=0.6, relheight=0.1)
y = Entry(frame, width=7)
y.place(relx=0.3, rely=0.6, relheight=0.1)

Label(frame, text='Z', background='#407DED', font=('Arial', 12)).place(relx=0.45, rely=0.6, relheight=0.1)
z = Entry(frame, width=7)
z.place(relx=0.5, rely=0.6, relheight=0.1)

submit_button = Button(frame, text='Send', command=get_xyz)
submit_button.place(relx=0.65, rely=0.6, relheight=0.1)

# label.after(20, grab_frame_from_camera)

# grab_frame_from_camera()
root.mainloop()
