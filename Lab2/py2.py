import tkinter as tk
from tkinter import filedialog
import random
from functools import partial
import math

public_key = None
private_key = None

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    d = 0
    x1, x2, y1, y2 = 0, 1, 1, 0
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2 - temp1 * x1
        y = y2 - temp1 * y1
        
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi == 1:
        d = y2 + phi

    return d

def generate_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = multiplicative_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher_blocks = []
    for char in plaintext:
        mi = ord(char)
        ci = pow(mi, key, n)
        cipher_blocks.append(ci)
    return cipher_blocks

def decrypt(pk, ciphertext):
    key, n = pk
    plain_blocks = []
    for char in ciphertext:
        mi = pow(char, key, n)
        plain_blocks.append(chr(mi))
    return ''.join(plain_blocks)

def browse_file(label):
    filename = filedialog.askopenfilename()
    label.config(text="Selected file: " + filename)
    return filename

def encrypt_file(public_key, input_file, output_file):
    with open(input_file, 'r',encoding='utf-8') as file:
        plaintext = file.read()
    encrypted_text = encrypt(public_key, plaintext)

    with open(output_file, 'w',encoding='utf-8') as file:
        for char in encrypted_text:
            file.write(str(char) + '\n')

    print("Encryption completed.")

def decrypt_file(private_key, input_file, output_file):
    with open(input_file, 'r',encoding='utf-8') as file:
        encrypted_text = [int(line.strip()) for line in file]

    decrypted_text = decrypt(private_key, encrypted_text)

    with open(output_file, 'w',encoding='utf-8') as file:
        file.write(decrypted_text)

    print("Decryption completed.")

def generate_key_pair(p_entry, q_entry):
    global public_key, private_key  
    p = int(p_entry.get())
    q = int(q_entry.get())
    public_key, private_key = generate_keypair(p, q)
    public_key_label.config(text="Public Key: " + str(public_key))
    private_key_label.config(text="Private Key: " + str(private_key))

def encrypt_selected_file():
    global public_key  
    if public_key is None:
        print("Public key is not generated yet.")
        return
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    encrypt_file(public_key, input_file, output_file)

def decrypt_selected_file():
    global private_key 
    if private_key is None:
        print("Private key is not generated yet.")
        return
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    decrypt_file(private_key, input_file, output_file)



root = tk.Tk()
root.title("RSA File Encryption")

p_label = tk.Label(root, text="Enter p:")
p_label.grid(row=0, column=0)
p_entry = tk.Entry(root)
p_entry.grid(row=0, column=1)

q_label = tk.Label(root, text="Enter q:")
q_label.grid(row=1, column=0)
q_entry = tk.Entry(root)
q_entry.grid(row=1, column=1)

generate_button = tk.Button(root, text="Generate Key Pair", command=partial(generate_key_pair, p_entry, q_entry))
generate_button.grid(row=2, column=0, columnspan=2)

public_key_label = tk.Label(root, text="Public Key: ")
public_key_label.grid(row=3, column=0, columnspan=2)

private_key_label = tk.Label(root, text="Private Key: ")
private_key_label.grid(row=4, column=0, columnspan=2)

input_label = tk.Label(root, text="Select input file:")
input_label.grid(row=5, column=0, columnspan=2)

output_label = tk.Label(root, text="Select output file:")
output_label.grid(row=6, column=0, columnspan=2)

encrypt_button = tk.Button(root, text="Encrypt File", command=lambda: encrypt_selected_file())  
encrypt_button.grid(row=7, column=0, columnspan=2)

decrypt_button = tk.Button(root, text="Decrypt File", command=lambda: decrypt_selected_file())  
decrypt_button.grid(row=8, column=0, columnspan=2)

root.mainloop()
