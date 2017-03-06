import Tkinter as tk

root = tk.Tk()
bkgcolor='#D84315'
root.configure(background=bkgcolor)

label=tk.Label(root,text="Gesture Recognition Project",font=('arial black',12),fg="white",width=90,height=3,bg="purple")
label.pack()

frame1 = tk.Frame(root,bg=bkgcolor)
frame1.pack(padx=205,pady=25)

bframe1 = tk.Frame(root,bg=bkgcolor)
bframe1.pack(side=tk.BOTTOM,padx=205)

photo1 = tk.PhotoImage(file="1.png")
photo2 = tk.PhotoImage(file="2.png")
photo3 = tk.PhotoImage(file="3.png")
photo4 = tk.PhotoImage(file="4.png")
# create the image button, image is above (top) the optional text
button1 = tk.Button(frame1, width=255, height=255, image=photo1,text="Cat and Mouse Game",fg="black",bg="white")
button1.pack(side=tk.LEFT)
button1.image = photo1

button2 = tk.Button(frame1, width=255, height=255, image=photo3,text="Slide Presenter",fg="purple",bg="white")
button2.pack(side=tk.LEFT,padx=25)
button2.image = photo1

button3 = tk.Button(bframe1, width=255, height=255, image=photo2,text="Scroller",fg="green",bg="white")
button3.pack(side=tk.LEFT)
button3.image = photo1

button4 = tk.Button(bframe1, width=255, height=255, image=photo4,text="Drawing Board",fg="blue",bg="white")
button4.pack(side=tk.LEFT,padx=25)
button4.image = photo1


# start the event loop
root.mainloop()
