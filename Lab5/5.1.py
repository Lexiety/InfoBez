import tkinter as tk
from tkinter import filedialog
from functools import partial

def calculate_parity_bit(data):
    count_ones = sum(1 for bit in data if bit == '1')
    parity_bit = '0' if count_ones % 2 == 0 else '1'
    return parity_bit

def check_parity(data):
    received_parity_bit = data[-1]
    calculated_parity_bit = calculate_parity_bit(data[:-1])
    return received_parity_bit == calculated_parity_bit

def check_input():
    data_sequence = generate_button_entry.get()
    is_correct = check_parity(data_sequence)
    if is_correct:
        input_label.config(text="Передача данных прошла успешно.")
    else:
        input_label.config(text="Произошла ошибка при передаче данных.")

root = tk.Tk()
root.title("Проверка передачи данных")

generate_button = tk.Label(root, text="12 бит сообщение +  1 бит проверки:")
generate_button.grid(row=1, column=0)
generate_button_entry = tk.Entry(root)
generate_button_entry.grid(row=1, column=1)

encrypt_button = tk.Button(root, text="Проверить",  command=check_input)
encrypt_button.grid(row=2, column=0, columnspan=2)

input_label = tk.Label(root, text="Вывод:")
input_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
