print("Welcome to the File Reader Program")
print("You can read this file as a test: input.txt")
filename = input("Enter the file name to read: ")

try:
    with open(filename, "r") as file:
        data = file.read()
        print(data)
    
    with open("newfile.txt", "w") as new_file:
        new_file.write(data)
        print("Data has been written to newfile.txt")
        
except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    
finally:
    try:
        file.close()
        
    except NameError:
        pass
    print("File operation completed.")