from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

# set global variables
global filepath
global Key
global keypath


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
        messagebox.showerror("Error", "no file was selected, try again")
        return
    messagebox.showinfo("", "Key generated successfully!")


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
        messagebox.showerror("Error", "no file was selected, try again")
        return

    # if the file selected doesn't have a key in it, it stops the function and gives the user an error
    try:
        global fernet
        fernet = Fernet(key)
    except ValueError:
        messagebox.showerror("Error", "This is not a key file, try again")
        return

    messagebox.showinfo("", "select one or more files to encrypt")
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
        messagebox.showerror("Error", "no file was selected, try again")
    else:
        messagebox.showinfo("", "files encrypted successfully!")


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
        messagebox.showerror("Error", "no file was selected, try again")
        return

    # if the file selected doesn't have a key in it, it stops the function and gives the user an error
    try:
        global fernet
        fernet = Fernet(key)
    except ValueError:
        messagebox.showerror("Error", "This is not a key file, try again")
        return

    messagebox.showinfo("", "select one or more files to decrypt")
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
        messagebox.showerror("Error", "no file was selected, try again")
    else:
        messagebox.showinfo("", "files decrypted successfully!")


top = Tk()
# window size
top.geometry("400x300")
# buttons that run a function when pressed
B = Button(top, text="Generate Key", command=Generate)
B.place(x=50, y=50)
ebutton = Button(top, text="encrypt", command=Encrypt)
ebutton.place(x=50, y=150)
ebutton = Button(top, text="decrypt", command=Decrypt)
ebutton.place(x=200, y=150)
# loops gui window
top.mainloop()