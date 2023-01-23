import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
import mysql.connector
#from py_mainform import mainform
from tkinter import filedialog
import os
import cv2
import PIL.Image #pip install pillow
import numpy as np
from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# set global variables
global filepath
global Key
global keypath
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

root = Tk()
mydb= mysql.connector.connect(host='localhost', user='root', password='', database='login_signup_db')
mycursor=mydb.cursor(buffered=True)
bgcolor = "#bdc3c7"
#root.resizable(False,False)
root.geometry('670x215')
root.title("Amazing App")
mainframe = tk.Frame(root)
mainframe.pack(fill='both', expand=1)


signup_frame = tk.Frame(mainframe)
signup_frame.pack(fill='both', expand=1)
signup_contentframe = tk.Frame(signup_frame,bg='#95a5a6')
signup_contentframe.pack(fill='both', expand=1)


root.columnconfigure(0, weight=1)
#input_frame= ttk.Frame(root,padding=(20,10,20,0))
#input_frame.grid(row=0,column=0)

name_label4 = tk.Label(signup_contentframe, text=" Sign Up", bg="dark turquoise",fg="White")
name_label4.config(font=("Segoe UI",16))
name_label4.grid(row=0,column=0, padx=(0,10))

name_label5 = tk.Label(signup_contentframe, text="User Mail: ",fg="black",bg='#95a5a6')
name_label5.config(font=("Segoe UI",12))
name_label5.grid(row=1,column=0,pady=5, sticky='e')
sup_name_entry = tk.Entry(signup_contentframe, width=15)
sup_name_entry.grid(row=1,column=1)
sup_name_entry .focus()
name_label6 = tk.Label(signup_contentframe, text="Password: ",fg="black",bg='#95a5a6')
name_label6.config(font=("Segoe UI",12))
name_label6.grid(row=2,column=0,pady=5, sticky='e')
sup_password_entry = tk.Entry(signup_contentframe, width=15, show='*')
sup_password_entry.grid(row=2,column=1)
name_label7 = tk.Label(signup_contentframe, text="Confirm Password: ",fg="black",bg='#95a5a6')
name_label7.config(font=("Segoe UI",12))
name_label7.grid(row=3,column=0,pady=5, sticky='e')
sup_conpassword_entry = tk.Entry(signup_contentframe,width=15, show='*')
sup_conpassword_entry.grid(row=3,column=1)

#----profile picture------#
name_label8 = tk.Label(signup_contentframe, text="Profile Picture: ",fg="black",bg='#95a5a6')
name_label8.config(font=("Segoe UI",12))
name_label8.grid(row=4,column=0, pady=5, sticky='e')
image_frame = tk.Frame(signup_contentframe)
image_frame.grid(row=4,column=1)
image_button = tk.Button(image_frame, text="Select Image")
image_button.grid(row=0, column=0)
imgpath_label=tk.Label(image_frame, text='Image Path')
imgpath_label.grid(row=0, column=1)
#----Train dataset-----#
def train_classifier():
    data_dir="C:/Users/Sadia/Desktop/Face recognizer4/data"
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

    faces = []
    ids = []

    for image in path:
        img = PIL.Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)

    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
    messagebox.showinfo('Result','your account has been created successfully!')
training_button=tk.Button(signup_contentframe,text="Sign Up",font=("Segoe UI",10), bg="dark blue",fg="White",command=train_classifier)
training_button.grid(row=5,column=1)


#----generate dataset function----#

def generate_dataset():
    if(sup_name_entry.get()=="" or sup_password_entry.get()=="" or sup_conpassword_entry.get()==""):
        messagebox.showinfo('Result','Please Complete Details')
    else:
        username = sup_name_entry.get().strip()
        password = sup_password_entry.get().strip()
        confirm_password = sup_conpassword_entry.get().strip()

        if check_username(username) == False:
            if password == confirm_password:
                mycursor.execute("SELECT* from users")
                myresult=mycursor.fetchall()
                imgpath = imgpath_label['text']
                id=1
                for x in myresult:
                    id+=1
                sql="insert into users(id, username, password, image_path) VALUES( %s, %s, %s, %s)"

                val=(id,sup_name_entry.get(), sup_password_entry.get(),imgpath)
                mycursor.execute(sql,val)
                mydb.commit()
                face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            # scaling factor = 1.3
            # minimum neighbor = 5

                    if faces == ():
                        return None
                    for (x, y, w, h) in faces:
                        cropped_face = img[y:y + h, x:x + w]
                    return cropped_face

                cap = cv2.VideoCapture(0)

                img_id = 0

                while True:
                    ret, frame = cap.read()
                    if face_cropped(frame) is not None:
                        img_id += 1
                        face = cv2.resize(face_cropped(frame), (200, 200))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = "data/user." + str(id) + "." + str(img_id) + ".jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

                        cv2.imshow("Cropped face", face)

                    if cv2.waitKey(1) == 13 or int(img_id) == 200:  # 13 is the ASCII character of Enter
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo('Result','Completed! Click Sign Up')
            else:
                messagebox.showwarning('Password', 'incorrect password confirmation')

        else:
            messagebox.showwarning('Duplicate Username', 'This Username Already Exists,try another one')

generate_button=tk.Button(signup_contentframe,text="Generate Dataset",font=("Segoe UI",10), bg="dark blue",fg="White",command=generate_dataset)
generate_button.grid(row=4,column=3)
#----register button---#
#signup_button = tk.Button(signup_contentframe, text="Sign Up",font=("Segoe UI",10), bg="dark blue",fg="White")
#signup_button.grid(row=5, column=1,pady=5, sticky='e')
go_login_label = tk.Label(signup_contentframe, text="Already have an account? Click Here",fg="black",bg='#95a5a6')
go_login_label.config(font=("Segoe UI",9))
go_login_label.grid(row=5,column=0,pady=5, sticky='e')
#---select image file---#
def select_image():
    filename = filedialog.askopenfilename(initialdir='/images', title="Select Profile Picture", filetypes=(("png images","*.png"),("jpg images","*.jpg")))
    imgpath_label['text'] = filename

image_button['command'] = select_image

#---go to login page from register page----#
def go_login():
    signup_frame.forget()
    loginframe.pack(fill="both", expand=1)


go_login_label.bind("<Button-1>", lambda page: go_login())


#---- username already exists?----#
def check_username(username):
    username = sup_name_entry.get().strip()
    vals = (username)
    select_query = "SELECT * FROM `users` WHERE `username` ='%s'"
    mycursor.execute(select_query, vals)
    user = mycursor.fetchone()
    if user is not None:
        return True
    else:
        return False



# ----Register a new user----#
#def signup():
   # username = sup_name_entry.get().strip()
   # password = sup_password_entry.get().strip()
   # confirm_password = sup_conpassword_entry.get().strip()
    #imgpath = imgpath_label['text']

    #if len(username) > 0 and len(password) > 0:
        #if check_username(username) == False:
            #if password == confirm_password:
                #vals = (id,username, password, imgpath)
                #insert_query = "INSERT INTO `users`( 'id',`username`, `password`,`image_path`) VALUES( %s, %s, %s, %s)"
                #c.execute(insert_query, vals)
                #connection.commit()
                #messagebox.showinfo('Sign Up', 'your account has been created successfully')
            #else:
                #messagebox.showwarning('Password', 'incorrect password confirmation')

        #else:
            #messagebox.showwarning('Duplicate Username', 'This Username Already Exists,try another one')
    #else:
        #messagebox.showwarning('Empty Fields', 'make sure to enter all the information')

#signup_button['command'] = signup


#------Login Page------#

loginframe = tk.Frame(mainframe)
loginframe.pack(fill='both', expand=1)
login_contentframe = tk.Frame(loginframe,bg='#95a5a6')
login_contentframe.pack(fill='both', expand=1)
#user_name = tk.StringVar()
#user_password = tk.StringVar()
#root.columnconfigure(0, weight=1)
#input_frame= ttk.Frame(root,padding=(20,10,20,0))
#input_frame.grid(row=0,column=0)

name_label1 = tk.Label(login_contentframe, text=" USER LOGIN", bg="dark turquoise",fg="White")
name_label1.config(font=("Segoe UI",24))
name_label1.grid(row=0,column=0, padx=(0,10))

name_label2 = tk.Label(login_contentframe, text="User Mail: ",fg="black",bg='#95a5a6')
name_label2.config(font=("Segoe UI",16))
name_label2.grid(row=1,column=0)
lg_user_name_entry = tk.Entry(login_contentframe, width=15)
lg_user_name_entry.focus()
lg_user_name_entry.grid(row=1,column=1)
name_label3 = tk.Label(login_contentframe, text="User Password: ",fg="black",bg='#95a5a6')
name_label3.config(font=("Segoe UI",16))
name_label3.grid(row=2,column=0)
name_label3 = tk.Label(login_contentframe, text=" ",fg="black",bg='#95a5a6')
name_label3.config(font=("Segoe UI",16))
name_label3.grid(row=6,column=0)
lg_user_password_entry = tk.Entry(login_contentframe, width=15, show='*')
lg_user_password_entry.grid(row=2,column=1)

#login_button = tk.Button(login_contentframe, text="Login",font=("Segoe UI",14), bg="dark blue",fg="White")
#login_button.grid(row=4, column=1,pady=5, sticky='e')
#go_signup_label = tk.Label(login_contentframe, text="Don't have an account? Click Here" , font=('Segoe UI',14),fg="red")
#go_signup_label.grid(row=4, column=0)
#def go_signup():
  #   loginframe.forget()

     #signup_frame.pack(fill="both", expand=1)


#go_signup_label.bind("<Button-1>", lambda page: go_signup())
quit_button = ttk.Button(login_contentframe, text="Cancel", command = root.destroy,padding=(20,10,20,10))
quit_button.grid(row=5,column=0)
#----make user login-----#
def login():
    username = lg_user_name_entry.get().strip()
    password = lg_user_password_entry.get().strip()
    vals = (username, password)
    select_query = "SELECT * FROM `users` WHERE `username` = %s and `password` = %s"
    mycursor.execute(select_query, vals)
    user = mycursor.fetchone()
    if user is not None:
        messagebox.showinfo('Test','Login successful!')
        #mainformwindow = tk.Toplevel()
        #app = mainform(mainformwindow)
        #root.withdraw() # hide the root
        #mainformwindow.protocol("WM_DELETE_WINDOW", close_win) # close the app

# ----Go to home page----#
        go_home_label = tk.Label(login_contentframe, text="Home Page", font=('Segoe UI', 14), fg="white", bg="dark blue")
        go_home_label.grid(row=5, column=1)

        def go_home():
            loginframe.forget()
            home_frame.pack(fill="both", expand=1)

        go_home_label.bind("<Button-1>", lambda page: go_home())
    else:
        messagebox.showwarning('Error','wrong username or password')



#login_button['command'] = login

#---Detect Face---#
def detect_face():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

            id, pred = clf.predict(gray_img[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))
            #mydb = mysql.connector.connect(host='localhost', user='root', password='', database='login_signup_db')
            #mycursor = mydb.cursor()

            mycursor.execute("select username from users where id="+str(id))
            s=mycursor.fetchone()
            s=''+''.join(s)

            if confidence > 80:
                cv2.putText(img,s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                login_button = tk.Button(login_contentframe, text="Login", font=("Segoe UI", 14), bg="dark blue",
                                         fg="White")
                login_button.grid(row=4, column=1, pady=5, sticky='e')
                login_button['command'] = login
            else:
                cv2.putText(img, "Unrecognized", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            coords=[x,y,w,h]
        return coords

    def recognize(img, clf, faceCascade):
        coords=draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        return img

    # loading classifier
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, img = video_capture.read()
        img = recognize(img, clf, faceCascade)
        cv2.imshow("face detection",img)

        if cv2.waitKey(1) == 13:
            break
    video_capture.release()
    cv2.destroyAllWindows()
detect_button=tk.Button(login_contentframe,text="Detect Face",font=("Segoe UI",14), bg="dark blue",fg="White",command=detect_face)
detect_button.grid(row=4,column=5)
#login_button['command'] = login

#----Encryption page----#
home_frame = tk.Frame(mainframe)
home_frame.pack(fill='both', expand=1)
home_contentframe = tk.Frame(home_frame,bg='#95a5a6')
home_contentframe.pack(fill='both', expand=1)
name_label9 = tk.Label(home_contentframe, text="Home", bg="dark turquoise",fg="White")
name_label9.config(font=("Segoe UI",24))
name_label9.grid(row=6,column=0, padx=(0,10))
#-----generate a key----#
# generates the key for encrypting/decrypting
def Generate():
    # prompts the user to either select a file to print the key to or create one to do so
    keypath = filedialog.askopenfilename()
    # generates key
    key = Fernet.generate_key()

    # writes the key to a file, but if you don't select a file it gives you an error and stops this function
    try:
        with open(keypath, "wb") as filekey:
            filekey.write(key)
    except FileNotFoundError:
        messagebox.showerror("Error", "No file was selected, try again")
        return
    messagebox.showinfo("", "Key generated successfully!")

# before encryption detect face----#
def e_detect_face():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
        coords = []
        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

            id, pred = clf.predict(gray_img[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))
            #mydb = mysql.connector.connect(host='localhost', user='root', password='', database='login_signup_db')
            #mycursor = mydb.cursor()

            mycursor.execute("select username from users where id="+str(id))
            s=mycursor.fetchone()
            s=''+''.join(s)

            if confidence > 80:
                cv2.putText(img,s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)

            else:
                cv2.putText(img, "Unrecognized", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            coords=[x,y,w,h]
        return coords

    def recognize(img, clf, faceCascade):
        coords=draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        return img

    # loading classifier
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, img = video_capture.read()
        img = recognize(img, clf, faceCascade)
        cv2.imshow("face detection",img)

        if cv2.waitKey(1) == 13:
            break
    video_capture.release()
    cv2.destroyAllWindows()


# function to encrypt files of your choosing

def Encrypt():
    messagebox.showinfo("", "select a key")
    # prompts the user to select a file with a key
    keypath = filedialog.askopenfilename()
    # open key file
    try:
        with open(keypath, "rb") as filekey:
            key = filekey.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "No file was selected, try again")
        return

    # if the file selected doesn't have a key in it, it stops the function and gives the user an error
    try:
        global fernet
        fernet = Fernet(key)
    except ValueError:
        messagebox.showerror("Error", "This is not a key file, try again")
        return

    messagebox.showinfo("", "Select one or more files to encrypt")
    # prompts the user to select a file to encrypt
    filepath = filedialog.askopenfilenames()
    # loops for each file in the list/array filepath and encrypts each file
    for x in filepath:
        # opens each file in filepath
        with open(x, "rb") as file:
            original = file.read()

        # encrypts the selected file
        global encrypted
        encrypted = fernet.encrypt(original)

        # opening the file in write mode and encrypts the data in it
        with open(x, "wb") as encrypted_file:
            encrypted_file.write(encrypted)
    # if the filepath is empty then it means no file was selected which means that an error is prompted
    if not filepath:
        messagebox.showerror("Error", "No file was selected, try again")
    else:
        messagebox.showinfo("", "Files encrypted successfully!")
def detect_face_and_encrypt():
    e_detect_face()
    Encrypt()

# function to decrypt files of your choosing
def Decrypt():
    messagebox.showinfo("", "select a key")
    # prompts the user to select a file with a key
    keypath = filedialog.askopenfilename()
    # open key file
    try:
        with open(keypath, "rb") as filekey:
            key = filekey.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "No file was selected, try again")
        return

    # if the file selected doesn't have a key in it, it stops the function and gives the user an error
    try:
        global fernet
        fernet = Fernet(key)
    except ValueError:
        messagebox.showerror("Error", "This is not a key file, try again")
        return

    messagebox.showinfo("", "Select one or more files to decrypt")
    # prompts the user to select a file to decrypt
    filepath = filedialog.askopenfilenames()
    # loops for each file in the list/array filepath and decrypts each file
    for x in filepath:
        # if no file is selected the function stops and it gives the user an error
        with open(x, "rb") as enc_file:
            encrypted = enc_file.read()

        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
        # opening the file in write mode and decrypts the file
        with open(x, "wb") as dec_file:
            dec_file.write(decrypted)
    # if the filepath is empty then it means no file was selected which means that an error is prompted
    if not filepath:
        messagebox.showerror("Error", "No file was selected, try again")
    else:
        messagebox.showinfo("", "Files decrypted successfully!")
#---1st detect face and then decrypt files----#
def detect_face_and_decrypt():
    e_detect_face()
    Decrypt()
name_label10 = tk.Label(home_contentframe, text="Generate a key",fg="black",bg='#95a5a6')
name_label10.config(font=("Segoe UI",12))
name_label10.grid(row=7, column=0)
generate_key_button = tk.Button(home_contentframe, text="Generate Key", command=Generate)
generate_key_button.grid(row=7, column=1)
name_label10 = tk.Label(home_contentframe, text="Choose a file to Encrypt: ",fg="black",bg='#95a5a6')
name_label10.config(font=("Segoe UI",12))
name_label10.grid(row=8, column=0)
efile_button = tk.Button(home_contentframe, text="Encrypt",command=detect_face_and_encrypt)
efile_button.grid(row=8, column=1)

def upload_file():
    file = filedialog.askdirectory()

    #fob=open(file,'r')
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder = '1K-wJJvT-F4Nsx1nNbbMluZeQNmkgiiMD'

    #directory = r'file'

    for f in os.listdir(file):
        filename = os.path.join(file, f)
        gfile = drive.CreateFile({'parents': [{'id': folder}], 'title': f})
        gfile.SetContentFile(filename)
        gfile.Upload()
        messagebox.showinfo("Google Drive", "File Uploaded Successfully!")
#efilepath_label=tk.Label(efile_frame, text="File Path")
#efilepath_label.grid(row=0, column=1)
name_label10 = tk.Label(home_contentframe, text="Save file in Google Drive:",fg="black",bg='#95a5a6')
name_label10.config(font=("Segoe UI",12))
name_label10.grid(row=8, column=2)
file_upload_button= tk.Button(home_contentframe, text="Upload File",command=lambda:upload_file())
file_upload_button.grid(row=8, column=3)
#---download a file from google drive---#
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
folder = '1K-wJJvT-F4Nsx1nNbbMluZeQNmkgiiMD'
v = StringVar()
name_label14 = tk.Label(home_contentframe, text="Enter Filename to Download:",fg="black",bg='#95a5a6')
name_label14.config(font=("Segoe UI",12))
name_label14.grid(row=9, column=0)
download_file_entry = Entry(home_contentframe, width=15, textvariable=v)
download_file_entry.grid(row=9,column=1)
def download_file():
    file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()
    for index, file in enumerate(file_list):
        if file['title']==v.get():
            file.GetContentFile(file['title'])
            messagebox.showinfo("Google Drive", "File Downloaded Successfully!")


name_label15 = tk.Label(home_contentframe, text="Download from Google Drive:",fg="black",bg='#95a5a6')
name_label15.config(font=("Segoe UI",12))
name_label15.grid(row=9, column=2)
file_download_button = Button(home_contentframe,text="Download", command=download_file)
file_download_button.grid(row=9,column=3)

#---decryption---#
name_label11 = tk.Label(home_contentframe, text="Choose a file to Decrypt: ",fg="black",bg='#95a5a6')
name_label11.config(font=("Segoe UI",12))
name_label11.grid(row=10, column=0)
efile_button = tk.Button(home_contentframe, text="Decrypt",command=detect_face_and_decrypt)
efile_button.grid(row=10, column=1)




#---view the list of saved files from google drive---#
def list_of_files():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder = '1K-wJJvT-F4Nsx1nNbbMluZeQNmkgiiMD'
    my_listbox = Listbox(home_contentframe)
    my_listbox.grid(row=11,column=3)

    file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed = false"}).GetList()
    for file in file_list:
        my_listbox.insert("end", file['title'])
name_label12 = tk.Label(home_contentframe, text="View the list of Saved Files: ",fg="black",bg='#95a5a6')
name_label12.config(font=("Segoe UI",12))
name_label12.grid(row=10, column=2)
view_list_button = tk.Button(home_contentframe, text="View List",command=list_of_files)
view_list_button.grid(row=10, column=3)

root.mainloop()