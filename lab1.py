from random import seed, randint, choice
import pdb
import time

# seed random number generator
seed(1)

DICTIONARY = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
MAX_SIZE = 25

def rle(file):
    file_length = len(file)
    codified_file = ""
    current_file_letter = file[0]
    current_file_position = 1
    current_file_count = 1
    while True:
        if file_length == 1:
            codified_file += str(current_file_count) + current_file_letter
            break
        if file[current_file_position] != current_file_letter:
            codified_file += str(current_file_count) + current_file_letter
            current_file_letter = file[current_file_position]
            current_file_count = 1
        else:
            current_file_count += 1
        if current_file_position == file_length - 1:
            codified_file += str(current_file_count) + current_file_letter
            break
        current_file_position += 1
    return codified_file

def random_size():
    return randint(1, MAX_SIZE)

def generate_file(size = 20, repetitive = False):
    file = ""
    while len(file) < size:
        new_char = choice(DICTIONARY)
        file += new_char
        if repetitive:
            file += randint(0, size - len(file)) * new_char
    return file

def generate_files(option):
    files = []
    for i in range(30):
        file = generate_file(20 if option == 1 else random_size(), option == 1)
        files.append(file)
    return files

def compress_files(files):
    compressed_files = []
    for file in files:
        compressed_files.append([file, rle(file)])
    return compressed_files

def compress(option):
    files = generate_files(option)
    compressed_files = compress_files(files)
    return compressed_files

def compare_info(files):
    table_data = {}
    for i, file in enumerate(files):
        original, compressed = file
        table_data[i+1] = [original, compressed, len(original), len(compressed), len(original)/len(compressed)]
    print ("{:<6} {:<45} {:<65} {:<15} {:<20} {:<30}".format('Nº','Original','Comprimida','Tamaño original','Tamaño comprimida','Relación de compresión'))
    for k, v in table_data.items():
        original, compressed, original_length, compressed_length, compression_ratio = v
        print ("{:<6} {:<45} {:<65} {:<15} {:<20} {:<30}".format(k, original, compressed, original_length, compressed_length, compression_ratio))    

def elapsed_time(start = 0, end = 0):
    elapsed = 1000*(end - start)
    print("Tiempo transcurrido: ", elapsed, " segundos")

if __name__ == "__main__":
    while True:
        print("Opciones disponibles:")
        print("\t1: textos aleatorios de 20 caracteres")
        print("\t2: textos contenido aleatorio")
        print("\t3: salir")
        try:
            selected_option = int(input("Seleccione opción: "))
            if selected_option == 1:
                start = time.time()
                files = compress(1)
                end = time.time()
                compare_info(files)
                elapsed_time(start, end)
                break
            elif selected_option == 2:
                start = time.time()
                files = compress(2)
                end = time.time()
                compare_info(files)
                elapsed_time(start, end)
                break
            elif selected_option == 3:
                break
            raise 
        except:
            print("Opción incorrecta")