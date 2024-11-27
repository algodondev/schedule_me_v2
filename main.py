from tkinter import *
from entities import *
import datetime
import calendar

root = Tk()
root.title("Schedule Me")

days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

# Variables globales
current_date = datetime.date.today()
current_month = current_date.month
current_year = current_date.year
month_days_instances = []

# Funciones para cambiar el mes
def previous_month():
    global current_month, current_year, month_days_instances
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    update_days()

def next_month():
    global current_month, current_year, month_days_instances
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    update_days()

# Función para actualizar los días del mes
def update_days():
    global month_days_instances
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Obtener la fecha del primer día del mes
    first_day_of_month = datetime.date(current_year, current_month, 1)
    start_day_of_week = first_day_of_month.weekday()  # 0 = Monday, 6 = Sunday
    start_day_of_week = (start_day_of_week + 1) % 7  # Ajuste para que el domingo sea 0

    # Obtener el número de días del mes
    if current_month == 12:
        next_month_date = datetime.date(current_year + 1, 1, 1)  # Enero del siguiente año
    else:
        next_month_date = datetime.date(current_year, current_month + 1, 1)

    days_in_month = (next_month_date - first_day_of_month).days

    # Obtener el número de días del mes anterior usando calendar
    previous_month_date = current_date.replace(month=current_month - 1 if current_month > 1 else 12)
    days_in_previous_month = calendar.monthrange(previous_month_date.year, previous_month_date.month)[1]

    # Lista para almacenar las instancias de Day
    month_days_instances.clear()

    # Crear un objeto 'Day' para cada día del mes actual
    for day in range(1, days_in_month + 1):
        day_date = datetime.date(current_year, current_month, day)
        day_obj = Day(day, day_date, [])  # Inicializamos 'events' como una lista vacía
        month_days_instances.append(day_obj)

    # Mostrar el mes y el año
    month_label.config(text=first_day_of_month.strftime('%B'))
    year_label.config(text=str(current_year))

    # Reorganizar los días del mes
    column_count = 0
    row_count = 0  # Comenzamos desde la fila donde se muestran los días de la semana

    # Mostrar los días de la semana (cabecera)
    for day in days:

        custom_font = ("Arial",25)

        if current_date.weekday() == column_count-1:
            custom_font = ("Arial", 25, "underline")

        label = Label(right_frame, text=day, padx=15, pady=15, font=custom_font)
        label.grid(row=row_count, column=column_count, sticky="nswe")
        column_count += 1

    row_count += 1
    column_count = 0

    # Mostrar días del mes anterior deshabilitados
    previous_month_day = days_in_previous_month - start_day_of_week + 1
    for i in range(start_day_of_week):  # Espacios en blanco antes del primer día del mes
        button = Button(right_frame, text=str(previous_month_day), font=("Arial", 14), padx=15, pady=15, bg="lightgray", state="disabled", bd=1, relief="solid")
        button.grid(row=row_count, column=column_count, sticky="nswe")
        column_count += 1
        previous_month_day += 1

    # Colocar los días del mes
    for day_instance in month_days_instances:

        bg_color = "white"	
        if len(day_instance.events) > 0:
            bg_color = "lightgreen"
        
        if day_instance.date == current_date:
            bg_color = "lightblue"

        button = Button(right_frame, text=str(day_instance.day), bg=bg_color, font=("Arial", 14), padx=15, pady=15, bd=1, relief="solid", command=lambda day=day_instance: show_modal(day))
        button.grid(row=row_count, column=column_count, sticky="nswe")
        column_count += 1

        # Cuando llegamos al final de la semana, pasamos a la siguiente fila
        if column_count == 7:
            column_count = 0
            row_count += 1

    # Agregar los días que sobran del mes siguiente con botones deshabilitados
    next_month_day = 1
    for i in range(column_count, 7):  # Rellenar con botones deshabilitados si no se completó la semana
        button = Button(right_frame, text=str(next_month_day), font=("Arial", 14), bg="lightgray", padx=15, pady=15, state="disabled", bd=1, relief="solid")
        button.grid(row=row_count, column=i, sticky="nswe")
        next_month_day += 1

# Función para mostrar el modal con la fecha completa
def show_modal(day_instance):
    # Crear la ventana emergente (modal)
    events_modal = Toplevel(root)
    events_modal.title(f"Day {day_instance.day} details")

    # Bloquear interaccion con la ventana principal
    events_modal.grab_set()
    # Bloquear la modificacion del tamaño del modal
    events_modal.resizable(False, False)

    # Formatear la fecha
    title_text = day_instance.date.strftime('Events for %A, %B %d %Y')
    
    # Etiqueta con la fecha
    modal_title = Label(events_modal, text=title_text, font=("Arial", 18))
    modal_title.grid(row=0, column=0, pady=10, padx=40, columnspan=2)

    # Mostrar los eventos del día
    events_frame = Frame(events_modal, width=300, height=200, bd=1, relief="solid", pady=30, padx=50)
    events_frame.grid(row=1, column=0, pady=10, padx=40)

    for i in range(4):
        label = Label(events_frame, text=f"Event {i}", font=("Arial", 14))
        label.grid(row=i, column=0, pady=10, padx=30)

        delete_button = Button(events_frame, text="Delete", font=("Arial", 14), bg="red", fg="white")
        delete_button.grid(row=i, column=1, pady=10, padx=30)

    # Campos para agregar un nuevo evento
    fields_frame = Frame(events_modal)
    fields_frame.grid(row=1, column=1, pady=10, padx=40)

    event_title_label = Label(fields_frame, text="Event title", font=("Arial", 14))
    event_title_label.grid(row=0, column=0, pady=10, padx=40)
    event_title_entry = Entry(fields_frame, font=("Arial", 14))
    event_title_entry.grid(row=1, column=0, pady=10, padx=40)

    event_description_label = Label(fields_frame, text="Event description", font=("Arial", 14))
    event_description_label.grid(row=2, column=0, pady=10, padx=40)
    event_description_entry = Entry(fields_frame, font=("Arial", 14))
    event_description_entry.grid(row=3, column=0, pady=10, padx=40)

    event_save_button = Button(fields_frame, text="Save", font=("Arial", 14), bg="green", fg="white")
    event_save_button.grid(row=4, column=0, pady=10, padx=40)

    # Boton para agregar un nuevo evento
    add_event_button = Button(events_modal, text="Add event", font=("Arial", 14), bg="blue", fg="white")
    add_event_button.grid(row=2, column=0, pady=10, padx=40, columnspan=2)

    
# Crear la interfaz
left_frame = Frame(root, width=300, height=600, bd=1, relief="solid")
left_frame.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

right_frame = Frame(root, width=300, height=600, bg="pink")
right_frame.grid(column=1, row=0, sticky="nswe", padx=30, pady=30)

# Colocar elementos en el frame izquierda
previous_month_button = Button(left_frame, text="<", font=("Arial", 20), bd=0, relief="flat", command=previous_month)
previous_month_button.grid(row=0, column=0, pady=(100, 0))
left_frame.grid_columnconfigure(0, weight=2)

month_label = Label(left_frame, text=current_month, font=("Arial", 50))
month_label.grid(row=0, column=1, pady=(100, 0))
left_frame.grid_columnconfigure(1, weight=2)

year_label = Label(left_frame, text=str(current_year), font=("Arial", 20))
year_label.grid(row=0, column=2, pady=(100, 0))
left_frame.grid_columnconfigure(2, weight=2)

next_month_button = Button(left_frame, text=">", font=("Arial", 20), bd=0, relief="flat", command=next_month)
next_month_button.grid(row=0, column=3, pady=(100, 0))
left_frame.grid_columnconfigure(3, weight=2)

# Configurar el calendario
update_days()

# Hacer la ventana responsiva
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4, minsize=550)
root.grid_columnconfigure(1, weight=6)

# Hacer que el grid de los días sea responsivo
for i in range(7):  # 7 columnas para los días
    right_frame.grid_columnconfigure(i, weight=1, uniform="equal")

# Configurar las filas del grid derecho
for i in range(7):  # 7 filas para los días (máximo 7 filas)
    right_frame.grid_rowconfigure(i, weight=1, uniform="equal")

root.mainloop()
