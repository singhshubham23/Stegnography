from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb  # pip install stegano

root = Tk()
root.title("Steganography - Hide a Secret Message")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.config(bg="#2f4155")

filename = ""  # Global variable for selected file
def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(
                                              ("PNG File", "*.png"),
                                              ("JPG File", "*.jpg"),
                                              ("All Files", "*.*")))
    if filename:
        img = Image.open(filename)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img)
        lbl.image = img

def Hide():
    global secret
    if filename:
        message = text1.get(1.0, END).strip()
        if message:
            secret = lsb.hide(filename, message)
            text1.delete(1.0, END)  # Reset text box after hiding message
            print("Message hidden successfully!")
        else:
            print("No message entered.")
    else:
        print("No image selected.")

def Show():
    if filename:
        try:
            clear_message = lsb.reveal(filename)
            if clear_message:
                text1.delete(1.0, END)
                text1.insert(END, clear_message)
            else:
                print("No hidden message found.")
        except Exception as e:
            print("Error revealing message:", e)
    else:
        print("No image selected.")

def save():
    if 'secret' in globals():
        save_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                                 filetypes=[("PNG File", "*.png"), ("All Files", "*.*")])
        if save_path:
            secret.save(save_path)
            print("Image saved successfully!")
    else:
        print("No hidden image to save.")

# Icon
image_icon = PhotoImage(file="logo.jpg")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)
Label(root, text="Cyber Project", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# First Frame (Image Display)
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame (Text Input)
frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Roboto 14", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=10, y=10, width=320, height=260)

scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=10, height=260)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame (Image Controls)
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Select and Save Image", bg="#2f4155", fg="Yellow").place(x=20, y=5)

# Fourth Frame (Steganography Controls)
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Hide & Reveal Message", bg="#2f4155", fg="Yellow").place(x=20, y=5)

root.mainloop()
