import tkinter as tk
from tkinter import filedialog
from functools import partial

def encrypt_block(block, key):
    encrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(len(block))])
    return encrypted_block

def decrypt_block(block, key):
    decrypted_block = bytes([block[i] ^ key[i % len(key)] for i in range(len(block))])
    return decrypted_block

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            block = f_in.read(4)
            if not block:
                break
            block += b'\x00' * (4 - len(block))
            encrypted_block = encrypt_block(block, key)
            f_out.write(encrypted_block)
    print("Encryption completed.")

def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            block = f_in.read(4)
            if not block:
                break
            decrypted_block = decrypt_block(block, key)
            f_out.write(decrypted_block)
    print("Decryption completed.")

def browse_file(label):
    filename = filedialog.askopenfilename()
    label.config(text="Selected file: " + filename)
    return filename

def encrypt_selected_file():
    key = generate_button_entry.get().encode() 
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    encrypt_file(input_file, output_file, key)

def decrypt_selected_file():
    key = generate_button_entry.get().encode()  
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    decrypt_file(input_file, output_file, key)

root = tk.Tk()
root.title("File Encryption")

generate_button = tk.Label(root, text="Enter Key:")
generate_button.grid(row=1, column=0)
generate_button_entry = tk.Entry(root)
generate_button_entry.grid(row=1, column=1)


input_label = tk.Label(root, text="Select input file:")
input_label.grid(row=5, column=0, columnspan=2)

output_label = tk.Label(root, text="Select output file:")
output_label.grid(row=6, column=0, columnspan=2)

encrypt_button = tk.Button(root, text="Encrypt File",  command=encrypt_selected_file)
encrypt_button.grid(row=7, column=0, columnspan=2)

decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_selected_file)
decrypt_button.grid(row=8, column=0, columnspan=2)

root.mainloop()
