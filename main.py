'''
ScheduleMe
'''
from tkinter import * #Interfaz grafica
from entities import * #Archivo de clases
import datetime #Libreria 
import calendar #Liberia

# Configurar la ventana principal de tkinter
root = Tk()
root.title("Schedule Me") #Titulo de la ventana 

#Lista con los nombres abreviados de los dias de la semana
days = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']

# Variables globales
current_date = datetime.date.today() #Fecha actual 
current_month = current_date.month #Mes actual
current_year = current_date.year #Año actual
month_days_instances = [] # Lista de instancias de dias del mes
created_events = [] #Lista de eventos creados

# -- Funciones para la navegacion del calendario --- # 
def previous_month():
    #Regresa al mes anterior
    #Tomar variables globales de mes, año y dias del mes
    global current_month, current_year, month_days_instances
    #Si es enero, retrocede al año anterior
    if current_month == 1:
        current_month = 12
        current_year -= 1
    else:
        current_month -= 1
    update_days() #Llamar a la funcion para actualizar los cambios

def next_month():
    #Cambiar al mes sigueinte
    #Tomar variables globales
    global current_month, current_year, month_days_instances
    #Si el mes es diciembre, avanza al año siguiente
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    update_days() 

# -- Función para actualizar los días del mes -- #
def update_days():
    #Actualiza la vista del calendario segun el mes y año del momento
    #Muestra los dias del mes, incluye dias del mes anterior y siguiente (para completar el cuadro)
    global month_days_instances
    #Limpiar los widget existentes, para luego poner los nuevos
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Obtener la fecha del primer día del mes
    first_day_of_month = datetime.date(current_year, current_month, 1) #Año, mes, dia del mes (primer dia)
    start_day_of_week = first_day_of_month.weekday()  # 0 = Monday, 6 = Sunday (por defecto)
    start_day_of_week = (start_day_of_week + 1) % 7  # Ajuste para que el domingo sea 0 (pasar a indexado en 1 y sacar modulo 7)

    # Obtener el número de días del mes
    #Calcular next_month_date, el primer dias dia del mes siguente
    if current_month == 12:
        #Si estamos en diciembre, usar el primer dia de enero
        next_month_date = datetime.date(current_year + 1, 1, 1)  # Enero del siguiente año
    else:
        #Si no, usar el primer dia del mes que sigue
        next_month_date = datetime.date(current_year, current_month + 1, 1)
    #Calcular los dias en el mes, hacer la resta entre el primer dia del mes siguiente menos el primer dia del mes actual
    days_in_month = (next_month_date - first_day_of_month).days

    #-- Encontrar los dias del mes previo y siguiente para rellenar la cuadricula -- 
    # Obtener el número de días del mes anterior usando calendar
    previous_month_date = current_date.replace(month=current_month - 1 if current_month > 1 else 12) #tomar el mes anterior
    days_in_previous_month = calendar.monthrange(previous_month_date.year, previous_month_date.month)[1]

    # Lista para almacenar las instancias de la clase Day
    month_days_instances.clear()

    # Crear un objeto 'Day' para cada día del mes actual
    for day in range(1, days_in_month + 1):
        day_date = datetime.date(current_year, current_month, day) #Tomar la fecha con año, mes y numero del dia
        day_obj = Day(day, day_date, [])  # Inicializamos 'events' como una lista vacía
        month_days_instances.append(day_obj) #Agregarlo a la lista

    # Mostrar el mes y el año 
    month_label.config(text=first_day_of_month.strftime('%B')) #Configurar label del mes
    year_label.config(text=str(current_year)) #Configurar label del año

    # Reorganizar los días del mes
    #LLevar contadores con las columnas y filas que se exploran 
    column_count = 0 #Columnas 
    row_count = 0  # Comenzamos desde la fila donde se muestran los días de la semana

    # Mostrar los días de la semana (cabecera)
    for day in days: #days son las abreviaturas de los dias de la semana
        #Configurar una fuente
        custom_font = ("Arial",25)
        #Si es el dia de la fecha actual, cambiar la fuente y agregar subrayado
        if current_date.weekday() == column_count-1:
            custom_font = ("Arial", 25, "underline")
        #Crear el lable con el texto del dia y agregarlo a la grid
        label = Label(right_frame, text=day, padx=15, pady=15, font=custom_font)
        label.grid(row=row_count, column=column_count, sticky="nswe")
        column_count += 1 #Avanzar a la siguiente columna

    #Avanzar una fila para iniciar a asignar los dias 
    row_count += 1
    column_count = 0 #regresar a columna cero

    # -- Mostrar días del mes anterior deshabilitados --
    previous_month_day = days_in_previous_month - start_day_of_week + 1 #Calcular cuantos dias previos existen
    for i in range(start_day_of_week):  # Espacios en blanco antes del primer día del mes
        #Crear el boton del dia, con el texto correspondiente 
        button = Button(right_frame, text=str(previous_month_day), font=("Arial", 14), padx=15, pady=15, bg="lightgray", state="disabled", bd=1, relief="solid")
        button.grid(row=row_count, column=column_count, sticky="nswe") #colocarlo en la grid
        column_count += 1 #avanzar a la siguiente columna
        previous_month_day += 1 #avanzar al siguiente dia

    # Revisar si hay eventos activos en el periodo 
    active_events = [] #lista vacio
    for event in created_events: #revisar en todos los eventos creados
        if event.date.month == current_month and event.date.year == current_year: #si tiene le mismo mes y dia
            active_events.append(event) #agregar a la lista

    # --- Colocar los días del mes ---
    for day_instance in month_days_instances:
        #Por cada dia en la lista de dias del mes
        #Colocar un fondo por defecto
        bg_color = "white"	
        #Si existe un evento ese dia, colocar un fondo de color verde 
        if day_instance.date in [event.date for event in active_events]:
            bg_color = "lightgreen"
        #Si el dia es la fecha actual, colocar un fondo celeste
        if day_instance.date == current_date:
            bg_color = "lightblue"
        #Crear un boton con el texto
        button = Button(right_frame, text=str(day_instance.day), bg=bg_color, font=("Arial", 14), padx=15, pady=15, bd=1, relief="solid", command=lambda day=day_instance: show_modal(day))
        button.grid(row=row_count, column=column_count, sticky="nswe") #Agregar el boton a la tabla
        column_count += 1 #Pasar a la siguiente columna

        # Cuando llegamos al final de la semana, pasamos a la siguiente fila
        if column_count == 7:
            column_count = 0 #regresar a la primera columna
            row_count += 1 #pasar a la siguiente fila
 
    # -- Dias del mes siguiente
    # Agregar los días que sobran del mes siguiente con botones deshabilitados
    next_month_day = 1
    for i in range(column_count, 7):  # Rellenar con botones deshabilitados si no se completó la semana
        button = Button(right_frame, text=str(next_month_day), font=("Arial", 14), bg="lightgray", padx=15, pady=15, state="disabled", bd=1, relief="solid")
        button.grid(row=row_count, column=i, sticky="nswe")
        next_month_day += 1

#Funcion para actualizar los eventos futuros
def update_upcoming_events(events):
    #Destruye los widget actuales
    for widget in upcoming_events.winfo_children():
        widget.destroy()

    #Ordena los eventos que existen segun las fechas
    events = sorted(events, key=lambda x: x.date)

    #Por cada evento, crea un label con su informacion y lo agrrega a la grid 
    for i, event in enumerate(events):
        label = Label(upcoming_events, text=f"{event.title}: {event.description} - {event.date} - {event.time}", font=("Arial", 14))
        label.grid(row=i, column=0, pady=10, padx=30)

    #Agrega upcoming events a la grid
    upcoming_events.grid(row=2, column=0, columnspan=4, pady=10)
    
# Función para mostrar el modal de eventos, ventana al seleccionar un dia
def show_modal(day_instance):
    global created_events
    
    # -- Funciones de los eventos -- #
    
    # Funcion para activar evento
    def activate_event_form():
        #Configurar las entradas y botones para recibir titulo y descripcion del evento
        event_title_entry.config(state="normal")
        event_description_entry.config(state="normal")
        event_save_button.config(state="normal")
        event_time_dropdown_entry.config(state="normal")

        add_event_button.config(state="disabled")
        
    # Funcion para desactivar evento 
    def deactivate_event_form():
        #Borrar las entradas de titulo y descripcion del evento
        event_title_entry.delete(0, END)
        event_description_entry.delete(0, END)

        #Deshabilitar las entradas 
        event_title_entry.config(state="disabled", text="")
        event_description_entry.config(state="disabled", text="")
        event_time_dropdown_entry.config(state="disabled")

        event_save_button.config(state="disabled")

        add_event_button.config(state="normal")
        
    #Funcion para mostrar eventos 
    def show_events(events):
        #Recorrer la lista de eventos 
        for i, event in enumerate(events):
            if event.date == day_instance.date:
                #Si existe un evento en la fecha de la instancia 
                #Crear label con titulo y descripcion del evento
                label = Label(events_frame, text=f"{event.title}: {event.description} - {event.time}", font=("Arial", 14))
                label.grid(row=i, column=0, pady=10, padx=30) #agregarlo a la grid
                #Crear el boton de delete
                #PENDIENTE DE CORRECION
                delete_button = Button(events_frame, text="Delete", font=("Arial", 14), bg="red", fg="white", command=lambda: delete_event(events, event, label, delete_button, events_frame))
                delete_button.grid(row=i, column=1, pady=10, padx=30) #agregar al lado del evento

    #Funcion para reiniciar el frame de eventos 
    def reset_events_frame(events, frame):
        #Borrar los widget actuales
        for widget in frame.winfo_children():
            widget.destroy()
        #Llamar a la funcion de mostrar eventos 
        show_events(events)

    #Funcion para guardar eventos
    def save_event(day_instance, title, description, time):
        global created_events
        #Crear la clase evento
        event = Event(title, description, day_instance.date, time)
        created_events.append(event) #agregar a la lista de eventos creados

        deactivate_event_form() #desactivar el form de eventos

        reset_events_frame(created_events, events_frame) #reiniciar el frame de eventos

    # Eliminar un evento
    # Pendiente de correcion**
    def delete_event(events, event, label_widget, button_widget, frame):
        
        label_widget.destroy()
        button_widget.destroy()

        events.remove(event)

        reset_events_frame(events, frame)

    # -- Codigo para la creacion de la ventana -- #
    # Crear la ventana modal
    events_modal = Toplevel(root)
    events_modal.title(f"Day {day_instance.day} details") #agregar el titulo

    # Protocolo para cerrar la ventana
    events_modal.protocol("WM_DELETE_WINDOW", lambda: close_modal(events_modal))

    # Bloquear interaccion con la ventana principal
    events_modal.grab_set()
    # Bloquear la modificacion del tamaño del modal
    events_modal.resizable(False, False)

    # Formatear la fecha
    title_text = day_instance.date.strftime('Events for %A, %B %d %Y')
    
    # Etiqueta con la fecha
    modal_title = Label(events_modal, text=title_text, font=("Arial", 18))
    modal_title.grid(row=0, column=0, pady=10, padx=40, columnspan=2) #agregar a grid

    # Mostrar los eventos del día
    events_frame = Frame(events_modal, width=300, height=200, pady=30, padx=50)
    events_frame.grid(row=1, column=0, pady=10, padx=40)

    show_events(created_events) #llamar a la funcion para mostrar eventos

    # Campos para agregar un nuevo evento
    #Crear el frame de campos
    fields_frame = Frame(events_modal)
    fields_frame.grid(row=1, column=1, pady=10, padx=40)

    #Titulo del evento
    #Label para titulo del evento
    event_title_label = Label(fields_frame, text="Event title", font=("Arial", 14))
    event_title_label.grid(row=0, column=0, pady=10, padx=40)
    #Entrada para titulo del evento
    event_title_entry = Entry(fields_frame, font=("Arial", 14), state="disabled")
    event_title_entry.grid(row=1, column=0, pady=10, padx=40)

    #Descripcion del evento
    #Label para descripcion
    event_description_label = Label(fields_frame, text="Event description", font=("Arial", 14))
    event_description_label.grid(row=2, column=0, pady=10, padx=40)
    #Entrada para la descripcion del evento
    event_description_entry = Entry(fields_frame, font=("Arial", 14), state="disabled")
    event_description_entry.grid(row=3, column=0, pady=10, padx=40)

    # Crear un menu dropdown con las horas disponibles para el evento
    # Generar las opciones para el dropdown (en formato HH:MM)
    hours = [f"{h:02}:{m:02}" for h in range(24) for m in [0, 15, 30, 45]]

    # Crear el dropdown con las horas
    selected_time = StringVar()
    selected_time.set(hours[24])  # Establecer un valor predeterminado

    #Crear el menu de opciones, configurar y colocar en la grid 
    event_time_dropdown_entry = OptionMenu(fields_frame, selected_time, *hours)
    event_time_dropdown_entry.config(width=8, font=("Arial", 10), state="disabled")
    event_time_dropdown_entry.grid(row=4, column=0, pady=10, padx=40)

    #Crear el boton de guardar el evento y agregarlo a la grid
    event_save_button = Button(fields_frame, text="Save", font=("Arial", 14), bg="green", fg="white", state="disabled", command=lambda: save_event(day_instance, event_title_entry.get(), event_description_entry.get(), selected_time.get()))
    event_save_button.grid(row=5, column=0, pady=10, padx=40)

    # Boton para agregar un nuevo evento, crear y colocar en grid 
    add_event_button = Button(events_modal, text="Add event", font=("Arial", 14), bg="blue", fg="white", command= activate_event_form)
    add_event_button.grid(row=2, column=0, pady=10, padx=40, columnspan=2)

# Funcion para cerrar el modal 
def close_modal(modal):
    modal.destroy()
    #Destruir el modal
    update_days() # Llamar a la funcion para actualizar dias 
    update_upcoming_events(created_events) #Actualizar los eventos proximos 


#Fin de las funciones de eventos, fecha y modal#

# Crear la interfaz principal
# Configurar los marcos izquierdo y derecho
left_frame = Frame(root, width=300, height=600)
left_frame.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

right_frame = Frame(root, width=300, height=600)
right_frame.grid(column=1, row=0, sticky="nswe", padx=30, pady=30)

# Colocar elementos del frame izquierdo
#Tendra el boton de mes previo, el mes, el año, el boton para el mes siguiente
#Abajo mostrara los eventos proximos

#Para acceder al mes anterior 
previous_month_button = Button(left_frame, text="<", font=("Arial", 20), bd=0, relief="flat", command=previous_month)
previous_month_button.grid(row=0, column=0, pady=(100, 0))
left_frame.grid_columnconfigure(0, weight=2)

#Label con el mes
month_label = Label(left_frame, text=current_month, font=("Arial", 50))
month_label.grid(row=0, column=1, pady=(100, 0))
left_frame.grid_columnconfigure(1, weight=2)

#Label con el año
year_label = Label(left_frame, text=str(current_year), font=("Arial", 20))
year_label.grid(row=0, column=2, pady=(100, 0))
left_frame.grid_columnconfigure(2, weight=2)

#Para acceder al mes siguiente 
next_month_button = Button(left_frame, text=">", font=("Arial", 20), bd=0, relief="flat", command=next_month)
next_month_button.grid(row=0, column=3, pady=(100, 0))
left_frame.grid_columnconfigure(3, weight=2)

# Mostrar eventos por venir, crear el label y frame
upcoming_events_label = Label(left_frame, text="Upcoming events", font=("Arial", 16))
upcoming_events_label.grid(row=1, column=0, columnspan=4, pady=(50, 10))
upcoming_events = Frame(left_frame, width=300, height=200)

update_upcoming_events(created_events) #llamar a la funcion 

# Del otro lado
# Configurar el calendario
update_days()

# Hacer la ventana responsiva
root.grid_rowconfigure(0, weight=1) 
root.grid_columnconfigure(0, weight=4, minsize=550)
root.grid_columnconfigure(1, weight=6) 
#Ajustarse la grid al tamaño de la ventana 

#Crear los espacios para colocar los dias
for i in range(7):  # 7 columnas para los días
    right_frame.grid_columnconfigure(i, weight=1, uniform="equal")
# Configurar las filas del grid derecho
for i in range(7):  # 7 filas para los días (máximo 7 filas)
    right_frame.grid_rowconfigure(i, weight=1, uniform="equal")

# Ejecutar el loop principal, que muestra la aplicacion
root.mainloop()

