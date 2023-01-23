from tkinter import*
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
root = Tk()
root.title('Google Drive')
root.geometry("400x400")
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
folder = '1K-wJJvT-F4Nsx1nNbbMluZeQNmkgiiMD'

#---for uploading file in google drive--#
#directory = "C:/Users/Sadia/PycharmProjects/pythonProject/data"

#for f in os.listdir(directory):
    #filename = os.path.join(directory,f)
    #gfile = drive.CreateFile({'parents': [{'id': folder}], 'title': f})
    #gfile.SetContentFile(filename)
    #gfile.Upload()


#---write something in a file of google drive---#

#file1 = drive.CreateFile({'parents':[{'id': folder}], 'title' : 'hello.txt'})
#file1.SetContentString('Hello world!')
#file1.Upload()
#---listbox---#
#my_listbox = Listbox(root)
#my_listbox.pack(pady=15)
#---view the list of files---#
#file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed = false"}).GetList()
#for file in file_list:
    #print(file['title'])
    #my_listbox.insert("end",file['title'])
#global var
#name_label3 = Label(root, text="User Password: ",fg="black",bg='#95a5a6')
#name_label3.config(font=("Segoe UI",16))
#name_label3.pack()

v = StringVar()
lg_user_password_entry = Entry(root, width=15, textvariable=v)
lg_user_password_entry.pack()
#print(v)
def download_file():
	print(v.get())
	file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
	for index, file in enumerate(file_list):
		if file['title']==v.get():
#print(index+1, 'file downloaded : ', file['title'])
			file.GetContentFile(file['title'])
			print(index+1, 'file downloaded:',file['title'])
			#messagebox.showinfo("Google Drive", "File Uploaded Successfully!")
my_button = Button(root,text="Download", command=download_file)
my_button.pack(pady=10)


root.mainloop()



#---add list of items---#

