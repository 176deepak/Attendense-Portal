# required modules
import os
from datetime import datetime
import csv
import numpy as np
import pandas as pd
import cv2
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import face_recognition as fr


# back button
def Back(frame):
    frame.destroy()


# comparision face encodings
def FaceEncoding(face_snap, frame):

    EncodedFaces = []
    path = "Images\\PersonsFace\\"

    for images in os.listdir("Images\\PersonsFace"):
        load_snap = fr.load_image_file(path+images)
        face_loc = fr.face_locations(img=load_snap)
        face_encoding = fr.face_encodings(
            face_image=load_snap, known_face_locations=face_loc)[0]
        EncodedFaces.append(face_encoding)

    curr_date_time = datetime.now()
    curr_date_time = curr_date_time.strftime("%d/%m/%Y %H:%M:%S")

    df = pd.read_csv("data-csv\\face_recordes.csv")
    face_names = list(df.iloc[:, 0].values)
    face_names.sort()

    image_path = "Images\\temp-faces\\temp.jpg"
    cv2.imwrite(image_path, face_snap)

    load_img = fr.load_image_file(image_path)
    face_loc = fr.face_locations(img=load_img)

    if len(face_loc) == 0:
        messagebox.showerror("Recognition Error",
                             "Please try again\nFace is not captured.")
        return

    face_encoding = fr.face_encodings(
        face_image=load_snap, known_face_locations=face_loc)[0]
    res = fr.compare_faces(EncodedFaces, face_encoding)

    os.remove("Images\\temp-faces\\temp.jpg")

    index = np.nonzero(res)[0]
    name = face_names[index[0]]
    data = [[name, curr_date_time]]
    file = open('data-csv\\attendense_data.csv', 'a+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(data)

    messagebox.showinfo("Operation Successful",
                        "Attendance has been successfully marked.")
    Back(frame=frame)


# mark attendense button
def MarkAttendense():

    frame = Frame(root, width=500, height=500, background="#120E0E")
    frame.place(relx=0, rely=0)

    back_img = PhotoImage(file="Images\\app-images\\Back.png")
    Button(frame, image=back_img, highlightthickness=0, bd=0, cursor="hand2",
           activebackground="#120E0E", command=lambda: Back(frame=frame)).place(relx=0.01, rely=0.9)
    Button(frame, text="Mark", cursor="hand2", background="#233DFF", fg="#FFFFFF", width=25,
           highlightthickness=0, bd=0, command=lambda: FaceEncoding(face_snap=snap, frame=frame)).place(relx=0.5, rely=0.9)

    while True:
        _, image = LiveStreaming.read()
        snap = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = ImageTk.PhotoImage(image=Image.fromarray(image))
        MarkFrame = Label(frame, image=image)
        MarkFrame.image = image
        MarkFrame.place(height=420, width=490, x=5, y=5)
        MarkFrame.update()


# adding face into database
def AddFace(face_snap, etr, frame):

    name = etr.get()

    image_path = "Images\\PersonsFace\\"+name+".jpg"
    cv2.imwrite(image_path, face_snap)

    load_img = fr.load_image_file(image_path)
    face_loc = fr.face_locations(img=load_img)

    if len(face_loc) == 0 or name == "":
        messagebox.showerror(
            "Error", "Please try again\nEither name is empty or face is not captured")
        return

    face_encoding = fr.face_encodings(
        face_image=face_snap, known_face_locations=face_loc)[0]
    face_data = {"Name": [name], "Faces": [face_encoding]}
    df = pd.DataFrame(face_data)
    df.to_csv("data-csv\\face_recordes.csv",
              mode='a', index=False, header=False)

    messagebox.showinfo("Operation Successful", "Member added successfully")
    Back(frame=frame)


# add button for add new members
def AddMember():

    name = StringVar()

    frame = Frame(root, width=500, height=500, background="#120E0E")
    frame.place(relx=0, rely=0.001)

    entry = Entry(frame, textvariable=name)
    entry.insert(0, "Enter your name")
    entry.place(width=150, relx=0.1, rely=0.9)

    backImg = PhotoImage(file="Images\\app-images\\Back.png")
    Button(frame, image=backImg, highlightthickness=0, bd=0, cursor="hand2",
           activebackground="#120E0E", command=lambda: Back(frame=frame)).place(relx=0.01, rely=0.9)
    Button(frame, text="Add", cursor="hand2", background="#233DFF", fg="#FFFFFF", width=25,
           highlightthickness=0, bd=0, command=lambda: AddFace(face_snap=snap, etr=entry, frame=frame)).place(relx=0.5, rely=0.9)

    while True:
        _, image = LiveStreaming.read()
        snap = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        image = ImageTk.PhotoImage(image=Image.fromarray(image))
        MarkFrame = Label(frame, image=image)
        MarkFrame.image = image
        MarkFrame.place(height=420, width=490, x=5, y=5)
        MarkFrame.update()


# main root of app
if __name__ == "__main__":

    snap = None
    LiveStreaming = cv2.VideoCapture(0)

    # main or root window
    root = Tk()
    icon = PhotoImage(file="Images\\app-images\\face-id.png")
    root.iconphoto(False, icon)
    root.title("Attendense App")
    root.configure(background="#120E0E")
    root.resizable(False, False)
    root.geometry("500x500")

    Label(root, text="Online Attendense System using\n Face Recognition", font=(
        "Garamond", 23, 'bold'), background="#120E0E", foreground="#FFFFFF").place(relx=0.06, rely=0.25)

    # mark-attendense button & add-member button
    Button(root, text="Mark Attendense", background="#233DFF", borderwidth=3.5, fg="#FFFFFF",
           cursor="hand2", command=MarkAttendense).place(width=120, relx=0.3, rely=0.7, anchor='center')
    Button(root, text="Add Member", background="#233DFF", borderwidth=3.5, fg="#FFFFFF",
           cursor="hand2", command=AddMember).place(width=120, relx=0.7, rely=0.7, anchor='center')

    root.mainloop()
