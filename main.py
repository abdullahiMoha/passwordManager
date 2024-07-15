from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
	entry_password.delete(0, END)
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
			   'v',
			   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
			   'R',
			   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	letters = [choice(letters) for _ in range(randint(8, 10))]
	symbols = [choice(symbols) for _ in range(randint(2, 4))]
	numbers = [choice(numbers) for _ in range(randint(2, 4))]

	password_list = letters + symbols + numbers  # Combining ths lists to make one password list
	shuffle(password_list)  # mixing the password characters
	password = "".join(password_list)  # converting list into string
	entry_password.insert(0, password)  # populating the password to the password filed
	pyperclip.copy(password)  # copying the generated password tothe clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_to_file(data_obj):
	with open("data.json", "w") as file:
		json.dump(data_obj, file, indent = 4)


def save():
	password = entry_password.get()
	email = entry_email.get()
	website = entry_website.get()
	new_dict = {
		website: {
			"email": email,
			"password": password
		}
	}  # This is for saving data into json format
	if len(password) == 0 or len(website) == 0:
		messagebox.showwarning("Warning", "You can not leave some filed empty")
	else:
		try:
			with open("data.json", "r") as file:
				# Reading the data
				data = json.load(file)
		except FileNotFoundError:
			write_to_file(new_dict)  # Calling the function to create the new file and write the data to it
			clear_fields()
		else:
			# Updating what is in data{}-adding new ones to it
			data.update(new_dict)
			write_to_file(data)  # Calling the function to save (write) the updated data to the file
			clear_fields()
		finally:
			clear_fields()


def find_password():
	website = entry_website.get()
	if len(website) != 0:
		try:
			with open("data.json", "r") as file:
				data = json.load(file)
		except FileNotFoundError:
			messagebox.showwarning("Warning", "No data file found")
		else:
			if website in data:
				password = data[website]["password"]
				email = data[website]["email"]
				messagebox.showinfo(title = website, message = f"Email: {email}\nPassword: {password}\n")
				clear_fields()
			else:
				# clear_fields()
				messagebox.showwarning("Warning", f"No detail for {website} exists")
	else:
		entry_website.focus()
		messagebox.showwarning(title = "Warning", message = f"The website fild can not be empty")


def clear_fields():
	entry_password.delete(0, END)
	entry_email.delete(0, END)
	entry_email.insert(0, "abdullahi@gmail.com")
	# entry_email.delete(0, END)
	entry_website.delete(0, END)
	entry_website.focus()


# ---------------------------- UI SETUP ------------------------------- #
# Creating the window screen
window = Tk()
window.title("Password Manager")
window.config(padx = 50, pady = 50)

# Creating canvas and other UI elements
canvas = Canvas(width = 200, height = 200)
logo = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = logo)
canvas.grid(row = 0, column = 1)

# labels
lbl_website = ttk.Label(text = "Website:")
lbl_website.grid(row = 1, column = 0)
lbl_email = Label(text = "Email/Username:")
lbl_email.grid(row = 2, column = 0)
lbl_password = Label(text = "Password:")
lbl_password.grid(row = 3, column = 0)

# entries
entry_website = ttk.Entry(width = 35)
entry_website.grid(row = 1, column = 1, sticky = "ew")
entry_website.focus()

entry_email = ttk.Entry(width = 35)
entry_email.grid(row = 2, column = 1, columnspan = 2, sticky = "ew", pady = 3)
entry_email.insert(0, "abdullahi@gmail.com")

entry_password = ttk.Entry(width = 21)
entry_password.grid(row = 3, column = 1, sticky = "ew")

# buttons
btn_search = ttk.Button(text = "Search", command = find_password)
btn_search.grid(row = 1, column = 2, sticky = "ew")
btn_generate = ttk.Button(text = "Generate Password", command = generate_password)
btn_generate.grid(row = 3, column = 2, sticky = "ew")

btn_add = ttk.Button(text = "Add ", width = 18, command = save)
btn_add.grid(row = 4, column = 1, sticky = "ew")

btn_clear = ttk.Button(text = "Clear", width = 18, command = clear_fields)
btn_clear.grid(row = 4, column = 2, sticky = "ew")

window.mainloop()
