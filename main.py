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
created_events = []

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

    # Check if day has events
    active_events = []
    for event in created_events:
        if event.date.month == current_month and event.date.year == current_year:
            active_events.append(event)

    # Colocar los días del mes
    for day_instance in month_days_instances:

        bg_color = "white"	
        if day_instance.date in [event.date for event in active_events]:
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
        button = Button(right_frame, text=str(next_month_day), font=("Arial", 14), bg="lightgray", padx=15, pady=15, state="disabled")
        button.grid(row=row_count, column=i, sticky="nswe")
        next_month_day += 1

def update_upcoming_events(events):
    for widget in upcoming_events.winfo_children():
        widget.destroy()

    events = sorted(events, key=lambda x: x.date)

    for i, event in enumerate(events):
        label = Label(upcoming_events, text=f"{event.title}: {event.description} - {event.date} - {event.time}", font=("Arial", 14))
        label.grid(row=i, column=0, pady=10, padx=30)

    upcoming_events.grid(row=2, column=0, columnspan=4, pady=10)
# Función para mostrar el modal de eventos
def show_modal(day_instance):
    global created_events

    # Events functions
    def activate_event_form():
        event_title_entry.config(state="normal")
        event_description_entry.config(state="normal")
        event_save_button.config(state="normal")
        event_time_dropdown_entry.config(state="normal")

        add_event_button.config(state="disabled")

    def deactivate_event_form():
        event_title_entry.delete(0, END)
        event_description_entry.delete(0, END)

        event_title_entry.config(state="disabled", text="")
        event_description_entry.config(state="disabled", text="")
        event_time_dropdown_entry.config(state="disabled")

        event_save_button.config(state="disabled")

        add_event_button.config(state="normal")

    def show_events(events):
        for i, event in enumerate(events):

            if event.date == day_instance.date:
                label = Label(events_frame, text=f"{event.title}: {event.description} - {event.time}", font=("Arial", 14))
                label.grid(row=i, column=0, pady=10, padx=30)

                delete_button = Button(events_frame, text="Delete", font=("Arial", 14), bg="red", fg="white", command=lambda: delete_event(events, event, label, delete_button, events_frame))
                delete_button.grid(row=i, column=1, pady=10, padx=30)

    def reset_events_frame(events, frame):
        
        for widget in frame.winfo_children():
            widget.destroy()
        
        show_events(events)

    def save_event(day_instance, title, description, time):
        global created_events
        
        event = Event(title, description, day_instance.date, time)
        created_events.append(event)

        deactivate_event_form()

        reset_events_frame(created_events, events_frame)

    # Eliminar evento
    def delete_event(events, event, label_widget, button_widget, frame):
        
        label_widget.destroy()
        button_widget.destroy()

        events.remove(event)

        reset_events_frame(events, frame)

    # Crear la ventana modal
    events_modal = Toplevel(root)
    events_modal.title(f"Day {day_instance.day} details")

    events_modal.protocol("WM_DELETE_WINDOW", lambda: close_modal(events_modal))

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
    events_frame = Frame(events_modal, width=300, height=200, pady=30, padx=50)
    events_frame.grid(row=1, column=0, pady=10, padx=40)

    show_events(created_events)

    # Campos para agregar un nuevo evento
    fields_frame = Frame(events_modal)
    fields_frame.grid(row=1, column=1, pady=10, padx=40)

    event_title_label = Label(fields_frame, text="Event title", font=("Arial", 14))
    event_title_label.grid(row=0, column=0, pady=10, padx=40)
    event_title_entry = Entry(fields_frame, font=("Arial", 14), state="disabled")
    event_title_entry.grid(row=1, column=0, pady=10, padx=40)

    event_description_label = Label(fields_frame, text="Event description", font=("Arial", 14))
    event_description_label.grid(row=2, column=0, pady=10, padx=40)
    event_description_entry = Entry(fields_frame, font=("Arial", 14), state="disabled")
    event_description_entry.grid(row=3, column=0, pady=10, padx=40)

    # Generar las opciones para el dropdown (en formato HH:MM)
    hours = [f"{h:02}:{m:02}" for h in range(24) for m in [0, 15, 30, 45]]

    # Crear el dropdown con las horas
    selected_time = StringVar()
    selected_time.set(hours[24])  # Establecer un valor predeterminado

    event_time_dropdown_entry = OptionMenu(fields_frame, selected_time, *hours)
    event_time_dropdown_entry.config(width=8, font=("Arial", 10), state="disabled")
    event_time_dropdown_entry.grid(row=4, column=0, pady=10, padx=40)

    event_save_button = Button(fields_frame, text="Save", font=("Arial", 14), bg="green", fg="white", state="disabled", command=lambda: save_event(day_instance, event_title_entry.get(), event_description_entry.get(), selected_time.get()))
    event_save_button.grid(row=5, column=0, pady=10, padx=40)

    # Boton para agregar un nuevo evento
    add_event_button = Button(events_modal, text="Add event", font=("Arial", 14), bg="blue", fg="white", command= activate_event_form)
    add_event_button.grid(row=2, column=0, pady=10, padx=40, columnspan=2)

def close_modal(modal):
    modal.destroy()

    update_days()
    update_upcoming_events(created_events)
    
# Crear la interfaz
left_frame = Frame(root, width=300, height=600)
left_frame.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

right_frame = Frame(root, width=300, height=600)
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

# Mostrar eventos por venir
upcoming_events_label = Label(left_frame, text="Events:", font=("Arial", 16))
upcoming_events_label.grid(row=1, column=0, columnspan=4, pady=(50, 10))

upcoming_events = Frame(left_frame, width=300, height=200)

# Mostrar los eventos por venir
update_upcoming_events(created_events)

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
