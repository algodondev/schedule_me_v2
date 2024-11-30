ScheduleMe 
Una aplicación de calendario interactiva desarrollada en Python con Tkinter. 
Permite gestionar eventos de manera sencilla, organizar actividades y navegar por meses de forma intuitiva.

---

ScheduleMe es una herramienta diseñada para ayudarte a organizar tus días. Con su interfaz gráfica amigable, puedes:  
- Navegar entre meses para visualizar días anteriores y futuros.  
- Crear, editar y eliminar eventos fácilmente.  
- Visualizar eventos próximos en un panel lateral.  
- Resaltar el día actual y los días con eventos programados.

---

1. **Navegación por Meses**: Botones intuitivos para cambiar al mes anterior o siguiente.  
2. **Gestión de Eventos**:  
   - Agregar eventos con título, descripción y hora personalizada.  
   - Ver eventos programados para un día específico.  
   - Eliminar eventos con un solo clic.  
3. **Visualización Responsiva**:  
   - Distribución clara de los días del mes en una cuadrícula.  
   - Resaltado del día actual (fondo celeste) y días con eventos (fondo verde).  
4. **Panel de Próximos Eventos**: Lista ordenada de eventos futuros directamente visible en la interfaz.

---

#### **Requisitos**
- **Python 3.9 o superior.**
- Tkinter (incluido en Python por defecto).

---

#### **Guía de Instalación**
1. **Descarga el Proyecto**:  
   Clona este repositorio o descarga los archivos directamente.

2. **Ejecuta el Programa**:  
   Abre la terminal o línea de comandos y navega al directorio donde descargaste los archivos. Luego, escribe:  
   ```bash
   python main.py
   ```

3. **Disfruta de la Aplicación**:  
   La ventana de ScheduleMe se abrirá con la vista del mes actual. 

---

#### **Estructura del Proyecto**
1. **`main.py`**:  
   Archivo principal con la lógica de la aplicación e interfaz gráfica.  
2. **`entities.py`**:  
   Contiene las clases `Day` y `Event` que definen las entidades base del calendario.  

---

#### **Cómo Usar**
1. **Navegar entre meses**:  
   - Usa los botones `<` y `>` en la parte superior izquierda para moverte al mes anterior o siguiente.
2. **Crear eventos**:  
   - Haz clic en un día del calendario.  
   - Presiona "Add Event", completa los campos y presiona "Save".  
3. **Ver eventos próximos**:  
   - Los eventos futuros se mostrarán automáticamente en el panel izquierdo.  
4. **Eliminar eventos**:  
   - Abre un día con eventos, presiona el botón "Delete" junto al evento que deseas eliminar.

--- 

#### **Equipo**
**Diego Francisco Arévalo Miranda, Javier Ernesto Galdámez Gallardo, Christopher Alexander Marroquín Figueroa, Gabriela María Rodríguez Osorio**  
Creado para facilitar la organización diaria de estudiantes y profesionales.  
