from tkinter import *
from entities import *

root = Tk()
root.title("Schedule Me")

days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

column_count = 0
row_count = 0

left_frame = Frame(root, width=300, height=600, bd=1, relief="solid")
left_frame.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

right_frame = Frame(root, width=300, height=600, bg="red")
right_frame.grid(column=1, row=0, sticky="nswe", padx=30, pady=30)

# Colocar informacion en el frame izquierdo

month_label = Label(left_frame, text="September", font=("Arial", 50))
month_label.grid(row=0, column=0, pady=(100, 0))
left_frame.grid_columnconfigure(0, weight=2)

year_label = Label(left_frame, text="2021", font=("Arial", 20))
year_label.grid(row=0, column=1, pady=(100, 0))
left_frame.grid_columnconfigure(1, weight=1)

message_label = Label(left_frame, text="Eventos proximos", font=("Arial", 25, "underline"))
message_label.grid(row=1, column=0, columnspan=2, pady=20)

space_label = Label(left_frame, text=" ", font=("Arial", 25))
space_label.grid(row=2, column=0, columnspan=2)

incoming_events_frame = Frame(left_frame, width=300, height=300)
incoming_events_frame.grid(row=3, column=0, columnspan=2)

events_label_text = "hola" 
events_label = Label(incoming_events_frame, text=events_label_text, font=("Arial", 20))
events_label.grid(row=0, column=0, sticky="nswe")
incoming_events_frame.rowconfigure(0, weight=1)

# Configurar las columnas y filas del frame derecho para que se expandan proporcionalmente
for i in range(7): 
    right_frame.grid_columnconfigure(i, weight=1)

for i in range(8): 
    right_frame.grid_rowconfigure(i, weight=1)

for i in range(56):

    if row_count == 0:
        label = Label(right_frame, text=days[column_count], padx=15, pady=15, font=("Arial", 25))
        label.grid(row=row_count, column=column_count, sticky="nswe")
    else:
        if i < 10:
            button = Button(right_frame, text=str(i), font=("Arial", 14), padx=18, pady=15, bd=1, relief="solid")
        else:
            button = Button(right_frame, text=str(i), font=("Arial", 14), padx=15, pady=15, bd=1, relief="solid")

        button.grid(row=row_count, column=column_count, sticky="nswe")
    column_count += 1
    if column_count == 7:
        column_count = 0
        row_count += 1            

 # Hacer la ventana responsiva
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=6)

root.mainloop()

