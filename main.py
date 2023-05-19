import customtkinter as ctk
import pyttsx3
import PyPDF2
import tkinter

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")


def read_pdf(f_name):
    file_obj = PyPDF2.PdfReader(f_name)
    return "".join([file_obj.pages[x].extract_text() for x in range(len(file_obj.pages))])


def read_txt(f_name):
    with open(f_name) as file:
        return file.read()


def upload_pdf():
    voice_select()
    filetypes = [('Choose File', '*.pdf *.txt')]
    file_name = ctk.filedialog.askopenfilename(filetypes=filetypes)
    convert_to_audio(file_name)


def convert_to_audio(file_name):
    if file_name[-3:].lower() == 'pdf':
        content = read_pdf(file_name)
    elif file_name[-3:].lower() == 'txt':
        content = read_txt(file_name)
    else:
        feedback_label.configure(text="Wrong file type. Please upload PDF or TXT.", text_color="red")
        return
    file_name = file_name.split('/')[-1]
    tts(content, file_name)
    feedback_label.configure(text=f"Your text file\n{file_name}\nhas been converted to audio!", font=("Arial", 20),
                             justify='left', text_color='green')


def tts(content, file_name):
    engine = pyttsx3.init()
    voice_select()
    engine.setProperty('rate', 140)
    engine.save_to_file(content, f"{file_name.split('.')[0]}.mp3")
    engine.runAndWait()


def voice_select():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if radio_var.get() == 2:
        engine.setProperty('voice', voices[1].id)
    elif radio_var.get() == 1:
        engine.setProperty('voice', voices[0].id)


window = ctk.CTk()
window.title("PDF 2 Audio Converter")
window.geometry("600x400")

label = ctk.CTkLabel(window, text="Welcome to the PDF 2 Audio Converter!", text_color='gray80',
                     anchor='center', justify='center', font=("Arial", 25))
label.place(relx=0.14, rely=0.10)
upload_button = ctk.CTkButton(window, width=300, height=60, text="Upload PDF or TXT", font=("Arial", 25),
                              command=upload_pdf)
upload_button.place(relx=0.28, rely=0.4)

feedback_label = ctk.CTkLabel(window, text="", text_color='gray80', anchor='center', justify='center',
                              font=("Arial", 25))
feedback_label.place(relx=0.05, rely=0.7)

radio_var = tkinter.IntVar()
radiobutton_1 = ctk.CTkRadioButton(window, text="Male Voice", command=voice_select(), variable=radio_var, value=1,
                                   font=('Arial', 18))
radiobutton_2 = ctk.CTkRadioButton(window, text="Female Voice", command=voice_select(), variable=radio_var, value=2,
                                   font=('Arial', 18))
radiobutton_1.place(relx=0.28, rely=0.6)
radiobutton_2.place(relx=0.55, rely=0.6)

window.mainloop()