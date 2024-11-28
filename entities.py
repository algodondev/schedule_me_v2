#Archivo con la definicion de las clases a utilizar 
#Clase evento
class Event:
    #Funcion constructura, recibe los parametros 
    def __init__(self, title, description, date, time):
        self.title = title #titulo del evento, texto
        self.description = description #descripcion del evento, texto
        self.date = date #la fecha
        self.time = time #el tiempo

#Clase dia 
class Day:
    #Funcion constructura 
    def __init__(self, day, date, events):
        self.day = day #Dia 
        self.date = date #Fecha
        self.events = events #lista de eventos 

    def __str__(self): #Funcion str
        return f"{self.day} - {self.date} - {self.events}" #Imprime los atributos de la instancia
