############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

# Constants
HAAR_CASCADE_PATH = "haarcascade_frontalface_default.xml"
TRAINING_IMAGE_LABEL_PATH = "TrainingImageLabel/"
STUDENT_DETAILS_PATH = "StudentDetails/"
TRAINING_IMAGE_PATH = "TrainingImage/"
ATTENDANCE_PATH = "Attendance/"

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def contact():
    mess._show(title='Contact us', message="Please contact us on : 'shubhamkumar8180323@gmail.com' ")

def check_haarcascadefile():
    if not os.path.isfile(HAAR_CASCADE_PATH):
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def save_pass():
    assure_path_exists(TRAINING_IMAGE_LABEL_PATH)
    password_file = os.path.join(TRAINING_IMAGE_LABEL_PATH, "psd.txt")
    
    if os.path.isfile(password_file):
        with open(password_file, "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            return
        with open(password_file, "w") as tf:
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    
    if op == key:
        if newp == nnewp:
            with open(password_file, "w") as txf:
                txf.write(newp)
            mess._show(title='Password Changed', message='Password changed successfully!!')
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="white")
    
    lbl4 = tk.Label(master, text='    Enter Old Password', bg='white', font=('comic', 12, ' bold '))
    lbl4.place(x=10, y=10)
    
    global old
    old = tk.Entry(master, width=25, fg="black", relief='solid', font=('comic', 12, ' bold '), show='*')
    old.place(x=180, y=10)
    
    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('comic', 12, ' bold '))
    lbl5.place(x=10, y=45)
    
    global new
    new = tk.Entry(master, width=25, fg="black", relief='solid', font=('comic', 12, ' bold '), show='*')
    new.place(x=180, y=45)
    
    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('comic', 12, ' bold '))
    lbl6.place(x=10, y=80)
    
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid', font=('comic', 12, ' bold '), show='*')
    nnew.place(x=180, y=80)
    
    cancel = tk.Button(master, text="Cancel", command=master.destroy, fg="black", bg="red", height=1, width=25, activebackground="white", font=('comic', 10, ' bold '))
    cancel.place(x=200, y=120)
    
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#00fcca", height=1, width=25, activebackground="white", font=('comic', 10, ' bold '))
    save1.place(x=10, y=120)
    
    master.mainloop()

def psw():
    assure_path_exists(TRAINING_IMAGE_LABEL_PATH)
    password_file = os.path.join(TRAINING_IMAGE_LABEL_PATH, "psd.txt")
    
    if os.path.isfile(password_file):
        with open(password_file, "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            return
        with open(password_file, "w") as tf:
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return

    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def TakeImages():
    check_haarcascadefile()
    assure_path_exists(STUDENT_DETAILS_PATH)
    assure_path_exists(TRAINING_IMAGE_PATH)
    
    serial = 0
    csv_file_path = os.path.join(STUDENT_DETAILS_PATH, "StudentDetails.csv")
    
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial += 1
        serial = (serial // 2)
    else:
        with open(csv_file_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(['SERIAL NO.', '', 'ID', '', 'NAME'])
            serial = 1

    Id = txt.get()
    name = txt2.get()
    
    if name.isalpha() or ' ' in name:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            mess._show(title='Camera Error', message='Could not open camera.')
            return
        
        detector = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
        sampleNum = 0
        
        while True:
            ret, img = cam.read()
            if not ret:
                mess._show(title='Camera Error', message='Failed to capture image.')
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite(os.path.join(TRAINING_IMAGE_PATH, f"{name}.{serial}.{Id}.{sampleNum}.jpg"), gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum > 100:
                break
        
        cam.release()
        cv2.destroyAllWindows()
        res = f"Images Taken for ID : {Id}"
        row = [serial, '', Id, '', name]
        
        with open(csv_file_path, 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        
        message1.configure(text=res)
    else:
        res = "Enter Correct name"
        message.configure(text=res)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists(TRAINING_IMAGE_LABEL_PATH)
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    detector = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    faces, ID = getImagesAndLabels(TRAINING_IMAGE_PATH)
    
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    
    recognizer.save(os.path.join(TRAINING_IMAGE_LABEL_PATH, "Trainner.yml"))
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    
    return faces, Ids

def TrackImages():
    check_haarcascadefile()
    assure_path_exists(ATTENDANCE_PATH)
    assure_path_exists(STUDENT_DETAILS_PATH)
    
    for k in tv.get_children():
        tv.delete(k)
    
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    trainer_file_path = os.path.join(TRAINING_IMAGE_LABEL_PATH, "Trainner.yml")
    
    if os.path.isfile(trainer_file_path):
        recognizer.read(trainer_file_path)
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    
    faceCascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    
    if os.path.isfile(os.path.join(STUDENT_DETAILS_PATH, "StudentDetails.csv")):
        df = pd.read_csv(os.path.join(STUDENT_DETAILS_PATH, "StudentDetails.csv"))
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break
    
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    attendance_file_path = os.path.join(ATTENDANCE_PATH, f"Attendance_{date}.csv")
    
    if os.path.isfile(attendance_file_path):
        with open(attendance_file_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
    else:
        with open(attendance_file_path, 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
    
    with open(attendance_file_path, 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i += 1
            if i > 1:
                if i % 2 != 0:
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    
    cam.release()
    cv2.destroyAllWindows()

######################################## USED STUFFS ############################################
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True, False)
window.title("Attendance System")
window.configure(background='#2d420a')

frame1 = tk.Frame(window, bg="#c79cff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#c79cff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance Monitoring System", fg="white", bg="#2d420a", width=55, height=1, font=('comic', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year + "  |  ", fg="#ff61e5", bg="#2d420a", width=55, height=1, font=('comic', 22, ' bold '))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="#ff61e5", bg="#2d420a", width=55, height=1, font=('comic', 22, ' bold '))
clock.pack(fill='both', expand=1)
tick()

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black", bg="#00fcca", font=('comic', 17, ' bold '))
head2.grid(row=0, column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black", bg="#00fcca", font=('comic', 17, ' bold '))
head1.place(x=0, y=0)

lbl = tk.Label(frame2, text="Enter ID", width=20, height=1, fg="black", bg="#c79cff", font=('comic', 17, ' bold '))
lbl.place(x=80, y=55)

txt = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name", width=20, fg="black", bg="#c79cff", font=('comic', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile", bg="#c79cff", fg="black", width=39, height=1, activebackground="#3ffc00", font=('comic', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="", bg="#c79cff", fg="black", width=39, height=1, activebackground="#3ffc00", font=('comic', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance", width=20, fg="black", bg="#c79cff", height=1, font=('comic', 17, ' bold '))
lbl3.place(x=100, y=115)

res = 0
exists = os.path.isfile(os.path.join(STUDENT_DETAILS_PATH, "StudentDetails.csv"))
if exists:
    with open(os.path.join(STUDENT_DETAILS_PATH, "StudentDetails.csv"), 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res += 1
    res = (res // 2) - 1
else:
    res = 0
message.configure(text='Total Registrations till now  : ' + str(res))

##################### MENUBAR #################################

menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Change Password', command=change_pass)
filemenu.add_command(label='Contact Us', command=contact)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Help', font=('comic', 29, ' bold '), menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=82)
tv.column('name', width=130)
tv.column('date', width=133)
tv.column('time', width=133)
tv.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4)
tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

###################### SCROLLBAR ################################

scroll = ttk.Scrollbar(frame1, orient='vertical', command=tv.yview)
scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear, fg="black", bg="#ff7221", width=11, activebackground="white", font=('comic', 11, ' bold '))
clearButton.place(x=335, y=86)

clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg="black", bg="#ff7221", width=11, activebackground="white", font=('comic', 11, ' bold '))
clearButton2.place(x=335, y=172)

takeImg = tk.Button(frame2, text="Take Images", command=TakeImages, fg="white", bg="#6d00fc", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
takeImg.place(x=30, y=300)

trainImg = tk.Button(frame2, text="Save Profile", command=psw, fg="white", bg="#6d00fc", width=34, height=1, activebackground="white", font=('comic', 15, ' bold '))
trainImg.place(x=30, y=380)

trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages, fg="black", bg="#3ffc00", width=35, height=1, activebackground="white", font=('comic', 15, ' bold '))
trackImg.place(x=30, y=50)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy, fg="black", bg="#eb4600", width=35, height=1, activebackground="white", font=('comic', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
window.mainloop()