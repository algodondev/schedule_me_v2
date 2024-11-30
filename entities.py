#Archivo con la definicion de las clases a utilizar 
#Clase evento
class Event:
    #Funcion constructura, recibe los parametros 
    def __init__(self, title, description, date, time, event_id):
        self.event_id = event_id #id del evento
        self.title = title #titulo del evento, texto
        self.description = description #descripcion del evento, texto
        self.date = date #la fecha
        self.time = time #el tiempo
    
    def __str__(self):
        return f"{self.event_id} - {self.title} - {self.date}"

#Clase dia 
class Day:
    #Funcion constructura 
    def __init__(self, day, date):
        self.day = day #Dia 
        self.date = date #Fecha

    def __str__(self): #Funcion str
        return f"{self.day} - {self.date}" #Imprime los atributos de la instancia
