import tkinter as tk
from tkinter import filedialog
from functools import partial
import random

def is_primitive_root(g, p):
    powers = set()
    for i in range(1, p):
        power = pow(g, i, p)
        if power in powers:
            return False
        powers.add(power)
    return True

def generate_primitive_root(p):
    primitive_roots = []
    for g in range(2, p):
        if is_primitive_root(g, p):
            primitive_roots.append(g)
    return random.choice(primitive_roots)

def generate_keys(bits):
    p = bits
    g = generate_primitive_root(p)
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    public_key = (p, g, h)
    private_key = x
    return public_key, private_key

def encrypt_text(public_key, text):
    p, g, h = public_key
    y = random.randint(2, p - 2)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    c2 = [(ord(char) * s) % p for char in text]
    return c1, c2

def decrypt_text(private_key, public_key, ciphertext):
    p, _, _ = public_key
    c1, c2 = ciphertext
    s = pow(c1, private_key, p)
    decrypted = [chr((char * pow(s, p-2, p)) % p) for char in c2]
    return ''.join(decrypted)

def browse_file(label):
    filename = filedialog.askopenfilename()
    label.config(text="Selected file: " + filename)
    return filename

def encrypt_file(public_key, input_file, output_file):
    with open(input_file, 'r',encoding='utf-8') as file:
        plaintext = file.read()

    encrypted_text = encrypt_text(public_key, plaintext)

    with open(output_file, 'w',encoding='utf-8') as file:
        file.write(str(encrypted_text[0]) + '\n')
        file.write(' '.join(map(str, encrypted_text[1])))

    print("Encryption completed.")

def decrypt_file(private_key, public_key, input_file, output_file):
    with open(input_file, 'r',encoding='utf-8') as file:
        lines = file.readlines()
        c1 = int(lines[0])
        c2 = list(map(int, lines[1].split()))

    ciphertext = (c1, c2)

    decrypted_text = decrypt_text(private_key, public_key, ciphertext)

    with open(output_file, 'w',encoding='utf-8') as file:
        file.write(decrypted_text)

    print("Decryption completed.")

    
def generate_key_pair(p_entry):
    global public_key, private_key  
    p = int(p_entry.get())
    public_key, private_key = generate_keys(p)
    public_key_label.config(text="Public Key: " + str(public_key))
    private_key_label.config(text="Private Key: " + str(private_key))

def encrypt_selected_file():
    global public_key  
    if public_key is None:
        print("Public key not generated")
        return
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    encrypt_file(public_key, input_file, output_file)

def decrypt_selected_file():
    global private_key  
    if private_key is None:
        print("Private key not generated ")
        return
    input_file = browse_file(input_label)
    output_file = browse_file(output_label)
    decrypt_file(private_key, public_key, input_file, output_file)


root = tk.Tk()
root.title("File Encryption")

p_label = tk.Label(root, text="Enter p:")
p_label.grid(row=0, column=0)
p_entry = tk.Entry(root)
p_entry.grid(row=0, column=1)

generate_button = tk.Button(root, text="Generate Key", command=partial(generate_key_pair, p_entry))
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
