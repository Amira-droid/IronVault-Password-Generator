#Please extract the zip folder before running, otherwise images won’t load.
# I am importing necessary libraries
#Library for generating random numbers and executing randomisation activities
import random
#Library for performing tasks involving string manipulation,adjustments and formatting etc
import string
# This library is for copying the password to clipboard
import pyperclip
# For creating a simple UI for user inputs alongwith 
import tkinter as tk
from tkinter import messagebox,ttk,PhotoImage
from idlelib.tooltip import Hovertip
# I have created a function that generated a password based on the inputs given by the user.
# I have provided options on the UI for the users to select from letters, digits and symbols
# I have also provided the option for users to avoid ambiguous characters
# It also handles exceptions when users provide incorrect inputs
def gen_password(length, use_letters, use_digits, use_symbols, avoid_ambiguous):
    characters = ''
    ambiguous={'0','1','l','I','o','O'}
    if use_letters:
        chars=string.ascii_letters
        if avoid_ambiguous:
            chars=''.join(c for c in chars if c not in ambiguous)
        characters+=chars
    if use_digits:
        chars=string.digits
        if avoid_ambiguous:
            chars=''.join(c for c in chars if c not in ambiguous)
        characters+=chars
    if use_symbols:
        chars=string.punctuation
        if avoid_ambiguous:
            chars=''.join(c for c in chars if c not in ambiguous)
        characters+=chars

    if not characters:
        return ''
    
    return ''.join(random.choice(characters) for _ in range(length))
 
# I have created a function that checks for the quality of the password based on its length
def check_quality(password):
    if len(password) < 8:
        return "Weak"
    elif len(password) < 12 or any(password.count(char) > 2 for char in set(password)):
        return "Medium"
    else:
        return "Strong"

# I have created a validation function which enables the "generate password" button on 2 conditions
# Condition 1 password length is between 1-100 characters
# Condition 2 the users select atleast one character type option
def to_validate(*args):
    length=entry_len.get()
    use_letters=letters_var.get()
    use_digits=digits_var.get()
    use_symbols=symbols_var.get()
    
    if length.isdigit() and 1<=int(length)<=100 and (use_letters or use_digits or use_symbols):
        button_gen.config(state="normal")
    else:
        button_gen.config(state="disabled")
        
# I have created a validation function for password generator
# It checks whether the input is a valid no or not
# The length of the password should be more than 4 characters
# It generate the password and update GUI widgets accordingly
def generate():
    try:
        
        length = int(entry_len.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for password length.")
        return
    
    if length<4:
        messagebox.showerror("Input Error", "Password must be at least 4 characters long.")
        return
    
    use_letters = letters_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    
    if not(use_letters or use_digits or use_symbols):
        messagebox.showerror("Selection Error","Please select at least one character type,")
        return
    
    avoid_ambiguous=avoid_amb_chr.get()
    password=gen_password(length, use_letters, use_digits, use_symbols, avoid_ambiguous)
    quality = check_quality(password)

    pass_entry.delete(0, tk.END)
    pass_entry.insert(0, password)
    label_quality.config(text=f"Quality: {quality}")
    
    if quality=="Weak":
        bar_strength.config(style="Weak.Horizontal.TProgressbar")
        bar_strength['value']=30
        lock_label.config(image=open_lock_img)
    elif quality=="Medium":
        bar_strength.config(style="Medium.Horizontal.TProgressbar")
        bar_strength['value']=60
        lock_label.config(image=open_lock_img)
    else:
        bar_strength.config(style="Strong.Horizontal.TProgressbar")
        bar_strength['value']=100
        to_animate()
    
    # This is to show the message on the UI that password has been copied to clipboard
    pyperclip.copy(password)
        
# I have created a function which initially hides the password and provides an option to unmask it
def togg_password():
    if show.get():
        pass_entry.config(show="")
    else:
        pass_entry.config(show="*")

# I have created this function to provide tips for an ideal password to the user
def tips():
    messagebox.showinfo("Password Tips",
                        "1. Use atleast 12 characters\n"
                        "2. Avoid using real words\n"
                        "3. Combine uppercase, lowercase, numbers and symbols\n"
                        "4. Don't reuse passwords")
    
# Have written the below code snippet to copy password to clipboard with a message on clicking the icon on the UI
def copy_to_clip():
    password=pass_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied","Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty","No password to copy!")
    
# This resets the UI for a fresh set of inputs
def reset():
    entry_len.delete(0, tk.END)
    pass_entry.delete(0,tk.END)
    letters_var.set(False)
    digits_var.set(False)
    symbols_var.set(False)
    avoid_amb_chr.set(False)
    show.set(False)
    pass_entry.config(show="*")
    bar_strength['value']=0
    label_quality.config(text="Quality:")
    
# I have created an animation function to switch between open and closed lock icon based on password quality
def to_animate(step=0):
    frames=[open_lock_img,closed_lock_img]
    if step<len(frames):
        lock_label.config(image=frames[step])
        app.after(150, to_animate, step+1)
    else:
        lock_label.config(image=closed_lock_img)

# I have created a function to provide a help guide for using the application   
def guide():
    guide_text=("How to Use the Password Generator:\n\n"
                "- Enter a password length between 1 and 100.\n"
                "- Select at least one charcter type: Letters, Digits or Symbols.\n"
                "- Optionally, check 'Avoid Ambiguous Characters' to exclude confusing characters like 0, O, I, 1 and l.\n"
                "- Click 'Generate Password' to create a password.\n"
                "- Password strength is based on length and character variety.\n"
                "- Use the 'Show Password' checkbox to toggle password visisbility.\n"
                "- Click the clipboard icon to copy the genrated password.\n"
                "- Use the Reset button to clear all inputs.\n\n"
                "If yout password is weak or medium, try increasing length or including more character types.")
    messagebox.showinfo("User Guide", guide_text)
    
    
# Initializing the application window
app = tk.Tk()

# This is to position the window on the screen
width_win=520
height_win=540
width_scr=app.winfo_screenwidth()
height_scr=app.winfo_screenheight()
x=(width_scr//2)-(width_win//2)
y=(height_scr//2)-(height_win//2)
app.geometry(f"{width_win}x{height_win}+{x}+{y}")

# Loading the images from the project folder
open_lock_img=PhotoImage(file="lock_open.png")
closed_lock_img=PhotoImage(file="lock_closed.png")
icon_clip=PhotoImage(file="clipboard.png")

# Customizing the style of password strength meter such as the colour based on password quality
style=ttk.Style(app)
style.theme_use('default')
style.configure("Weak.Horizontal.TProgressbar",troughcolor="#d3d3d3", background="red")
style.configure("Medium.Horizontal.TProgressbar",troughcolor="#d3d3d3", background="orange")
style.configure("Strong.Horizontal.TProgressbar",troughcolor="#d3d3d3", background="green")

# Below are the design settings
font_settings=("Segeo UI",10)
bg_color="#f0f0f0"
label_fg="#003366"
button_bg="#0059b3"
button_fg="white"
checkbox_fg="#003366"

# provisioning a Lock image to visually represent password strength (open = weak, closed = strong)
lock_label=tk.Label(app, image=open_lock_img, bg=bg_color)
lock_label.grid(row=9, column=0, columnspan=3, pady=10)

# Mouseover or hovering message about the open and closed status of the lock
Hovertip(lock_label,"Lock indicates password strength:\n🔓=Weak/Medium\n🔒=Strong")


# I have set UI backgroup and the responsiveness of the layout 
app.configure(bg=bg_color)
app.grid_columnconfigure(0,weight=1)
app.grid_rowconfigure(11, weight=1)
app.minsize(350,300)
app.title("Amira's Password Generator")


# creating UI frame for password length input
frame_len=tk.Frame(app,bg=bg_color, pady=10)
frame_len.grid(row=0, column=0, columnspan=3, sticky="w", padx=10)
tk.Label(frame_len,text="Password Length:", font=font_settings, fg=label_fg, bg=bg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_len=tk.Entry(frame_len, font=font_settings, width=10)
entry_len.grid(row=0, column=1, padx=5, pady=5)

# Creating frame for selection of character type
frame_opt=tk.LabelFrame(app,text="Include Characters", font=font_settings, fg=label_fg, bg=bg_color, padx=10, pady=10)
frame_opt.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=5)

# This is to set the default settings of the each character type input
letters_var=tk.BooleanVar(value=False)
digits_var=tk.BooleanVar(value=False)
symbols_var=tk.BooleanVar(value=False)

# This is to activate or disable the "generte password" button based on validation of user inputs
entry_len.bind("<KeyRelease>",to_validate)
letters_var.trace_add("write",to_validate)
digits_var.trace_add("write",to_validate)
symbols_var.trace_add("write",to_validate)

# creating Check buttons for character type
tk.Checkbutton(frame_opt, text="Letters", variable=letters_var, font=font_settings, fg=checkbox_fg, bg=bg_color, activebackground=bg_color).grid(row=0, column=0, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_opt, text="Digits", variable=digits_var, font=font_settings, fg=checkbox_fg, bg=bg_color, activebackground=bg_color).grid(row=0, column=1, padx=10, pady=5, sticky="w")
tk.Checkbutton(frame_opt, text="Symbols", variable=symbols_var, font=font_settings, fg=checkbox_fg, bg=bg_color, activebackground=bg_color).grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Creating an option to avoid ambiguous characters from the password
avoid_amb_chr=tk.BooleanVar(value=False)
avoid_amb_checkbox=tk.Checkbutton(frame_opt, text="Avoid Ambiguous Characters", variable=avoid_amb_chr, font=font_settings, fg=checkbox_fg, bg=bg_color, activebackground=bg_color)
avoid_amb_checkbox.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=5)

# Message on mouseover to avoid ambiguous characters
Hovertip(avoid_amb_checkbox,"Avoid characters like 0, O, I, l and 1 to avoid confusion!")


# Creating the button for password generation
button_gen=tk.Button(app,text="Generate Password",font=font_settings,bg=button_bg,fg=button_fg,activebackground="#004080",activeforeground="white",command=generate)
button_gen.grid(row=2,column=0, columnspan=3, pady=10, padx=10, sticky="w")
button_gen.config(state="disabled")
Hovertip(button_gen,"Enable by entering length and selecting character types")


# Frame generation for displaying generated password an copying button
frame_pass=tk.Frame(app,bg=bg_color, pady=5)
frame_pass.grid(row=3, column=0, columnspan=3, sticky="w", padx=10)

# Creating password entry field
tk.Label(frame_pass, text="Generated Password:", font=font_settings, fg=label_fg, bg=bg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
pass_entry=tk.Entry(frame_pass, font=font_settings, width=30, show="*")
pass_entry.grid(row=0, column=1, padx=(5,10), pady=5, sticky="w")


# Creating clipboard icon
button_copy=tk.Button(frame_pass, image=icon_clip, bg=bg_color, relief="flat", command=copy_to_clip)
button_copy.image=icon_clip
button_copy.grid(row=0, column=2, padx=(0,10), pady=5, sticky="e")
Hovertip(button_copy,"Copy password to clipboard")

# Created a checkbox for show or hide password
show=tk.BooleanVar()
show_checkb=tk.Checkbutton(app,text="Show Password",variable=show,font=font_settings,fg=checkbox_fg,bg=bg_color,activebackground=bg_color,command=togg_password)
show_checkb.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="w")

# Creation of label and progress bar for the user to easily understand password strength
label_quality=tk.Label(app,text="Quality:",font=font_settings,fg=label_fg,bg=bg_color)
label_quality.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="w")

bar_strength=ttk.Progressbar(app, length=300, mode="determinate", maximum=100, style="Weak.Horizontal.TProgressbar")
bar_strength.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

# I have created the button for displaying tips for a strong password
Suggestions_button=tk.Button(app,text="Tips for Creating Strong Passwords",font=font_settings,bg=button_bg,fg=button_fg,activebackground="#004080",activeforeground="white",command=tips)
Suggestions_button.grid(row=8, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

# Creating frames for reset and help buttons to make it easy for the user to use the application
frame_bott=tk.Frame(app, bg=bg_color)
frame_bott.grid(row=10, column=0, columnspan=3, padx=10, pady=(0,10), sticky="ew")

frame_bott.grid_columnconfigure(0,weight=2)
frame_bott.grid_columnconfigure(1, weight=1)

# Creation of reset button to prepare the application for reuse
reset_btn=tk.Button(frame_bott, text="Reset",font=font_settings,bg="#28a745",fg="white",activebackground="#1e7e34",activeforeground="white",command=reset)
reset_btn.grid(row=0, column=0, padx=(0,5), sticky="ew")

# Creation of help button to show user guide for facilitating the user
help_btn=tk.Button(frame_bott, text="Help?", font=font_settings, bg="#FFC107", fg="black", activebackground="#e6ac00", activeforeground="black", command=guide)
help_btn.grid(row=0, column=1, padx=(5,0), sticky="ew") 

# It automatically focus the cursor on the password length entry field as soon as the UI window opens
entry_len.focus()

# Starts the application main loop
app.mainloop()