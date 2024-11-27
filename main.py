from tkinter import *
from entities import *
import datetime
import calendar  

root = Tk()
root.title("Schedule Me")

days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

# Obtener la fecha actual
current_date = datetime.date.today()
current_day = current_date.strftime('%A')  # El nombre del día completo (e.g., "Sunday", "Monday")
current_month = current_date.strftime('%B')  # Nombre del mes (e.g., "September")
current_year = current_date.year

# Obtener la distribución de los días del mes (comenzando en domingo)
first_day_of_month = datetime.date(current_year, current_date.month, 1)
start_day_of_week = first_day_of_month.weekday()  # 0 = Monday, 6 = Sunday (en Python)
start_day_of_week = (start_day_of_week + 1) % 7  # Ajuste para que el domingo sea 0

# Obtener el número de días del mes
days_in_month = (datetime.date(current_year, current_date.month + 1, 1) - first_day_of_month).days

# Obtener el número de días del mes anterior usando calendar
previous_month = current_date.replace(month=current_date.month - 1 if current_date.month > 1 else 12)
days_in_previous_month = calendar.monthrange(previous_month.year, previous_month.month)[1]

# Lista para almacenar las instancias de Day
month_days_instances = []

# Crear un objeto 'Day' para cada día del mes actual
for day in range(1, days_in_month + 1):
    day_date = datetime.date(current_year, current_date.month, day)
    day_obj = Day(day, day_date, [])  # Inicializamos 'events' como una lista vacía
    month_days_instances.append(day_obj)

left_frame = Frame(root, width=300, height=600, bd=1, relief="solid")
left_frame.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

right_frame = Frame(root, width=300, height=600, bg="red")
right_frame.grid(column=1, row=0, sticky="nswe", padx=30, pady=30)

# Colocar informacion en el frame izquierdo
month_label = Label(left_frame, text=current_month, font=("Arial", 50))
month_label.grid(row=0, column=0, pady=(100, 0))
left_frame.grid_columnconfigure(0, weight=2)

year_label = Label(left_frame, text=str(current_year), font=("Arial", 20))
year_label.grid(row=0, column=1, pady=(100, 0))
left_frame.grid_columnconfigure(1, weight=1)

message_label = Label(left_frame, text="Eventos proximos", font=("Arial", 25, "underline"))
message_label.grid(row=1, column=0, columnspan=2, pady=20)

space_label = Label(left_frame, text=" ", font=("Arial", 25))
space_label.grid(row=2, column=0, columnspan=2)

incoming_events_frame = Frame(left_frame, width=300, height=300)
incoming_events_frame.grid(row=3, column=0, columnspan=2)

# Eventos que estan por llegar
events_label_text = "hola" 
events_label = Label(incoming_events_frame, text=events_label_text, font=("Arial", 20), wraplength=200, anchor="w")
events_label.grid(row=0, column=0, sticky="nswe")
incoming_events_frame.rowconfigure(0, weight=1)

# Configurar las columnas y filas del frame derecho para que se expandan proporcionalmente
for i in range(7): 
    right_frame.grid_columnconfigure(i, weight=1)

for i in range(7): 
    right_frame.grid_rowconfigure(i, weight=1)

# Mostrar los días de la semana
column_count = 0
row_count = 0

for index, day in enumerate(days):
    label = Label(right_frame, text=day, padx=15, pady=15, font=("Arial", 25))
    label.grid(row=row_count, column=column_count, sticky="nswe")
    column_count += 1

row_count += 1
column_count = 0

# Mostrar días del mes anterior deshabilitados
previous_month_day = days_in_previous_month - start_day_of_week + 1  # Empezamos con el último día del mes anterior
for i in range(start_day_of_week):  # Espacios en blanco antes del primer día del mes
    button = Button(right_frame, text=str(previous_month_day), font=("Arial", 14), padx=15, pady=15, bg="lightgray", state="disabled", bd=1, relief="solid")
    button.grid(row=row_count, column=column_count, sticky="nswe")
    column_count += 1
    previous_month_day += 1

# Colocar los días del mes
for day_instance in month_days_instances:
    button = Button(right_frame, text=str(day_instance.day), font=("Arial", 14), padx=15, pady=15, bd=1, relief="solid")
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

# Hacer la ventana responsiva
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=6)

root.mainloop()
