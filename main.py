# Implementación código Hamming

from random import seed, randint, choice, choices

# seed random number generator
seed(1)

DICTIONARY = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
SIZE = 1

# Busca las posiciones de los bits de paridad
def autocomplete(file):
	file = list(file)
	x = position = 0	
	while position < len(file):
		position = 2 ** x
		# Inserta el valor de paridad
		if position < len(file):
			file.insert(position-1, "*")
		else:
			break
		x += 1
	file = "".join(file)
	return file

# Calcula paridades individuales
def calculate_parities(file, salto, temp=""):
	original_file = file
	file = file[salto-1:]
	n = "N"*(salto-1)
	temp += n 
	n = "N"*salto
	nsalt = salto * 2
	while len(file) > 0:
		temp += file[:salto]
		file = file[nsalt:]
		temp += n		
	temp = temp[:len(original_file)]
	return temp

# Genera una fila por cada elemento de paridad
def get_rows(file):
	parity_rows = dict()
	total_rows = file.count("*")
	current_row = 0
	while total_rows > current_row:
		step = 2 ** current_row
		parity_rows[step] = calculate_parities(file, step) 
		current_row += 1
	return parity_rows

# Busca las filas en que las suma de sus bits sea impar
def search_errors(rows):
	wrong_rows = list()
	for key, content in rows.items():
		sum = 0
		for element in content:
			for char in element:
				if char != "*" and char != "N":
					sum += int(char)
		if sum % 2 != 0: 
			error = True
			wrong_rows.append(key)
		else:
			error = False
	return wrong_rows, error

# Busca los errores
def search_related_errors(wrong_rows_bits):
	related_columns = list()
	for index, element in enumerate(wrong_rows_bits):
		centinela = False
		for bit in element:
			try:
				int(bit)
				centinela = True
			except:
				centinela = False
				break
		if centinela:
			related_columns.append(index)
	return related_columns

# Busca las columnas relaciondas al error
def search_related_columns(rows, wrong_rows):
	length = len(list(rows.values())[0])
	wrong_rows_bits = []
	for i in range(length):
		bits = ""
		temp = list(wrong_rows)
		while len(temp) > 0:
			objective_row = temp.pop(0)
			for j in wrong_rows:
				if j == objective_row:
					bits += rows[j][i]
		wrong_rows_bits.append(bits)
	related_columns = search_related_errors(wrong_rows_bits)
	return related_columns

def clean_file(file):
	return file.replace("*", "")

# Decodifica un archivo
def decode_file(file):
	print("file", file)
	file_without_errors = ""
	for i in range(int(len(file)/7)):
		portion = file[i*7:i*7+7]
		autocompleted_string = autocomplete(portion)
		original_autocompleted_string = autocompleted_string
		while True:  # Hasta que no haya errores en la palabra binaria
			rows = get_rows(autocompleted_string)
			(wrong_files, error) = search_errors(rows)
			if not error:
				break       
			related_columns = search_related_columns(rows, wrong_files)
			for i in related_columns:
				print(i)
				temp_file = original_autocompleted_string
				if autocompleted_string[i] == "0":
					autocompleted_string = temp_file[:i] + "1" + temp_file[i+1:]
					break
				else:
					autocompleted_string = temp_file[:i] + "0" + temp_file[i+1:]
					break
		file_without_errors += clean_file(autocompleted_string)
	print(file_without_errors)
	return file_without_errors

# Genera un archivo de texto con caracteres al azar
def generate_file():
    new_file = ""
    while(len(new_file) < SIZE):
        new_file += choice(DICTIONARY)
    return new_file
    
# Genera los archivos de text0 con caracteres al azar
def generate_random_files(quantity):
    words = []
    for i in range(quantity):
        words.append(generate_file())
    return words

# Codifica un archivo
def file_to_bin(file):
    return "".join(f"{ord(i):08b}" for i in file)

# Codifica los archivos
def files_to_bin(files):
    bin_files = []
    for file in files:
        bin_files.append(file_to_bin(file))
    return bin_files

# Codifica un archivo a hamming
def encode_file(file):
    # Los bits de paridad irán en las posiciones 1, 2 y 4
    encoded_file = ""
    for i in range(int(len(file)/4)):
        encoded_portion = ""
        portion = file[i*4:i*4+4]
        for i in range(3):
            if i == 0:
                ones = 0
                if (portion[0] == "1"):
                    ones += 1
                if (portion[1] == "1"):
                    ones += 1
                if (portion[3] == "1"):
                    ones += 1
                if ones % 2 == 0:
                    encoded_portion += "0"
                else:
                    encoded_portion += "1"
            if i == 1:
                ones = 0
                if (portion[0] == "1"):
                    ones += 1
                if (portion[2] == "1"):
                    ones += 1
                if (portion[3] == "1"):
                    ones += 1
                if ones % 2 == 0:
                    encoded_portion += "0"
                else:
                    encoded_portion += "1"
                encoded_portion += portion[0]
            if i == 2:
                ones = 0
                if (portion[1] == "1"):
                    ones += 1
                if (portion[2] == "1"):
                    ones += 1
                if (portion[3] == "1"):
                    ones += 1
                if ones % 2 == 0:
                    encoded_portion += "0"
                else:
                    encoded_portion += "1"
                encoded_portion += portion[1]
                encoded_portion += portion[2]
                encoded_portion += portion[3]
        encoded_file += encoded_portion
    return encoded_file

# Codifica los binarios a hamming
def encode_files(files):
    encoded_files = []
    for file in files:
        encoded_files.append(encode_file(file))
    return encoded_files

# Genera errores aleatoriamente en un archivo
def generate_errors(file, prob):
    file_with_errors = ""
    for char in file:
        # 1 significa que generará un error en la posición
        has_error = choices([0, 1], [1-prob, prob], k=1)[0]
        if has_error:
            if char == "0":
                file_with_errors += "1"
            else:
                file_with_errors += "0"
        else:
            file_with_errors += char
    return file_with_errors

# Genera errores aleatoriamente
def massive_generate_errors(files, prob):
    files_with_errors = []
    for file in files:
        files_with_errors.append(generate_errors(file, prob))
    return files_with_errors

# Decodifica los archivos
def decode_files(files):
	for file in files:
		decode_file(file)

if __name__ == "__main__":
    files = generate_random_files(2)
    bin_files = files_to_bin(files)
    # Se utilizará hamming (7,4), es decir, que de cada 7 bits del mensaje, 4 serán de datos y 3 de paridad 
    encoded_files = encode_files(bin_files)
    files_with_errors = massive_generate_errors(encoded_files, 0.1)
    decoded_files = decode_files(files_with_errors)
