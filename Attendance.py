import tkinter.ttk as ttk
import csv
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *

root = Tk()
root.config(bg="#3f77d1")
# root.geometry("1200x800")
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.resizable(width=False, height=False)



def move(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


title_bar = Frame(root, bg="#d1c23f", relief='raised')
title_bar.pack(side=TOP, fill=BOTH)
title_bar.bind('<B1-Motion>', move)
title = Label(title_bar, text="TRUE ATTENDANCE REGISTER", bg="#ebeae8", fg='lime')
title.pack(side=LEFT)
close_button = Button(title_bar, text='   X   ', command=root.destroy, bg='#ebeae8', fg='lime').pack(side=RIGHT)


def myClick():
    path = 'AttendenceImages'
    Employee = []
    classemploy = []
    mylist = os.listdir(path)
    # print(mylist)
    for cls in mylist:
        cur = cv2.imread(f'{path}/{cls}')
        Employee.append(cur)
        classemploy.append(os.path.splitext(cls)[0])
        # print(classemploy)

    def encoding(Employee):
        enco = []
        for em in Employee:
            em = cv2.cvtColor(em, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(em)[0]
            enco.append(encode)
        return enco

    def attendance(name):
        with open('AttendenceList.csv', 'r+') as f:
            myData = f.readlines()
            emplyeelist = []
            for l in myData:
                entry = l.split(',')
                emplyeelist.append(entry[0])
            if name not in emplyeelist:
                now = datetime.now()
                dstr = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dstr}')

    encodelistknown = encoding(Employee)
    print("Encoding Complete")
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        facecurLoc = face_recognition.face_locations(imgs)
        encodecur = face_recognition.face_encodings(imgs, facecurLoc)
        for encodeface, faceloc in zip(encodecur, facecurLoc):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)
            matchIndex = np.argmin(facedis)
            if (matches[matchIndex]):
                name = classemploy[matchIndex].upper()
                y1, x2, y2, x1 = faceloc
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name)
            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break


img=PhotoImage(file='logooo.png')
Label(root,image=img).place(relx=0.5,rely=0.15,anchor=CENTER)
mybutton = Button(text="CLICK ME TO START THE APPLICATION", font='Helvetica,32', padx=25, pady=25, bg="#d1c23f",fg='black', bd=2, command=myClick)
mybutton.place(relx=0.5, rely=0.32, anchor=CENTER)

label = Label(root, text="NOTE- Hit q on your keyboard to close the Camera", font='Helvetica,32', bg="#d1c23f",fg='black', bd=2)
label.place(relx=0.5, rely=0.45, anchor=CENTER)

TableMargin = Frame(root, width=25,bg="#3f77d1")
TableMargin.place(relx=0.37,rely=0.53)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Name", "Time"), height=50, selectmode="extended", yscrollcommand=scrollbary.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Time', text="Time", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.pack()

with open('AttendenceList.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        first = row['Name']
        last = row['Time']
        tree.insert("", 0, values=(first, last))

root.mainloop()
