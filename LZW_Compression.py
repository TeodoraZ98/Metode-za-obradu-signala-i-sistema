from tkinter import *
from tkinter import filedialog
import PIL.Image
import os
import base64
import time
import PyPDF2 as PyPDF2

file_path = None


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Izaberite fajl", filetypes=(("All Files", "*.*"),
                                                                              ("Text Files", "*.txt"),
                                                                              ("PDF Files", "*.pdf"),
                                                                              ("Pictures", "*.png"),
                                                                              ("Pictures", "*.jpeg")))

    file_size = os.path.getsize(file_path)
    label_text = f"{file_path}    File Size:{file_size} bytes"
    Label(root, text=label_text).pack()
    # text,pdf,picture?
    if file_path.endswith(".txt"):
        file_opened = open(file_path, "r+")
        read_file = file_opened.read()
        my_text.insert(END, read_file)
        file_opened.close()
    elif file_path.endswith(".pdf"):
        os.system(file_path)
    else:
        my_image = PIL.Image.open(file_path, mode='r')  # moram preko PIL... nece ImageTk...
        my_image.show()


def save_txt():
    lzw_results = []
    converted_image = ''
    global file_path

    Label(root, text="Files have been created at directory above, Result:").pack()

    file_name_lzw = file_path[:-4] + 'Encoded.txt'
    file_name_restored = file_path[:-4] + 'Decoded' + file_path[-4:]

    if file_path.endswith(".txt"):
        lzw_results = lzw(my_text.get(1.0, END))

    else:
        with open(file_path, "rb") as image2string:
            converted_image_b = base64.b64encode(image2string.read())
            converted_image = str(converted_image_b)
        lzw_results = lzw(converted_image)

    # lzw_results = [compressed,restore,start,end]
    # saving lzw file
    with open(file_name_lzw, 'w') as fw:
        for i in lzw_results[0]:
            fw.write(str(i) + ' ')

    # saving restored file
    if file_path.endswith(".txt"):
        with open(file_name_restored, 'w+') as fw:
            for i in lzw_results[1]:
                fw.write(str(i))
    elif file_path.endswith(".pdf"):
        decoded_data = base64.b64decode(converted_image_b)
        img_file = open(file_name_restored, 'wb')
        img_file.write(decoded_data)
        img_file.close()

        text = Text(root, width=80, height=30)
        text.pack(pady=20)

        pdf_file = PyPDF2.PdfFileReader(file_name_restored)
        # Select a Page to read
        page = pdf_file.getPage(0)
        # Get the content of the Page
        content = page.extractText()
        # Add the content to TextBox
        text.insert(1.0, content)

    else:
        decoded_data = base64.b64decode(converted_image_b)
        img_file = open(file_name_restored, 'wb')
        img_file.write(decoded_data)
        img_file.close()

        img = PhotoImage(file=file_name_restored)
        label1 = Label(root, image=img)
        label1.image = img
        label1.pack(pady=20)

    label_text = f"Total Time: {lzw_results[3] - lzw_results[2]} sec"
    Label(root, text=label_text).pack()


######################### LZW ##########################
def lzw_encode(txt):
    compressed = []
    dict_size = 256
    dictionary = list(chr(x) for x in range(dict_size))

    s = txt[0]
    for i in range(1, len(txt)):
        c = txt[i]
        if s + c in dictionary:
            s = s + c
        else:
            dictionary.append(s + c)
            compressed.append(dictionary.index(s))
            s = c

    compressed.append(dictionary.index(s))
    return compressed


def lzw_decode(compressed):
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))

    s = ''
    restore = ''

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        else:
            entry = s + s[0]

        restore += entry

        if s != '':
            dictionary[dict_size] = s + entry[0]
            dict_size += 1

        s = entry
    return restore


def lzw(data):
    start = time.time()
    compressed = lzw_encode(data)
    restore = lzw_decode(compressed)
    end = time.time()

    # print('\n\nInput: ' + input)
    print('Encode: ')
    # print(compressed)
    # print('Decode: ' + restore)

    print('String Length: ' + str(len(data)))
    print('Encoded array Length: ' + str(len(compressed))) # nece da treba za exe

    print('isto je? :  ' + str(data == restore))

    print(f"Total Time: {end - start} sec")

    return [compressed, restore, start, end]


######################################################

if __name__ == "__main__":
    root = Tk()  # instance
    root.title('LZW Compression - Authors: A.M & T.Z')
    root.geometry("950x950")  # screen size

    #background_image = PhotoImage(file='bg_image.png')  # promeni u relative path i vrv nece radi za exe
    #background_label = Label(root, image=background_image)
    #background_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(root, text="Text Editor:").pack(pady=10)
    # text box
    my_text = Text(root, width=40, height=10, font=("Helvetica", 16))
    my_text.pack(pady=5)  # packuj on screen

    open_button = Button(root, text="Open Text, Pictures or PDF files", command=open_file)
    open_button.pack(pady=20)

    save_button = Button(root, text="Encode and Decode a file", command=save_txt)
    save_button.pack(pady=20)

    root.mainloop()
