import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Simple GUI")
root.geometry("300x150")

# Create a label
label = tk.Label(root, text="Enter something:")
label.pack(pady=10)

# Create an entry widget
entry = tk.Entry(root)
entry.pack(pady=5)

# Function to update label
def update_label():
    user_input = entry.get()
    label.config(text=f"You entered: {user_input}")

# Create a button
button = tk.Button(root, text="Submit", command=update_label)
button.pack(pady=10)

# Run the application
root.mainloop()
