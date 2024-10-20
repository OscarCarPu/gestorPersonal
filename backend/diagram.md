# Gestor de Proyectos
### Proyecto - proyecto
| Atributo|Tipo|Comentarios|
|-----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|datetime_creacion|S|valor fijo, now() NOT NULL|
|minutos_dedicados|N|suma minutos_dedicados hijos|
|estado|S|[nuevo, en curso, en pausa, en espera, cerrado] NOT NULL|
|descripcion|S||
|etiquetas|S|Array con etiquetas|

### Tiempo dedicado - tiempo_dedicado
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|tarea_id|N|tarea.id NOT NULL|
|minutos|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|N||

### Tarea - tarea
| Atributo|Tipo|Comentarios|
|-----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|proyecto_id|N|proyecto.id NOT NULL|
|padre_id|N|parea.id|
|minutos_estimados|N||
|minutos_dedicados|N|por defecto 0 NOT NULL|
|minutos_dedicados_total|N|suma minutos_dedicados hijos|
|prioridad|N|[0-5]|
|datetime_creacion|S|valor fijo, now() NOT NULL|
|datetime_finalizada|S||
|datetime_fecha_limite|S||
|estado|S|[nuevo, en curso, en pausa, en espera, cerrado] NOT NULL|
|descripcion|S||

### Recado - recado
| Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|tarea_id|N|tarea.id NOT NULL|
|datetime_creacion|S|valor fijo, now() NOT NULL|
|prioridad|N|[0-5]|
|datetime_finalizada|S||
|estado|S|[nuevo, en curso, en pausa, en espera, completado] NOT NULL|
|descripcion|S||

# Calendario y Horario
### Evento - evento
|Atributo|Tipo|Comentario|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|descripcion|S||
|datetime_inicio|S|NOT NULL|
|datetime_fin|S|NOT NULL|
|datetime_creacion|S|now()|
|tarea_id|N|tarea.id NOT NULL|

### Horario - horario
|Attributo|Tipo|Comentario|
|----|----|----|
|id|N|AUTOINCREMENT|
|tarea_id|N|tarea.id NOT NULL|
|time_inicio|S|NOT NULL|
|time_fin|S|NOT NULL|
|datetime_creacion|S|now()|
|date_inicio|S|NOT NULL|
|date_fin|S|NOT NULL|
|dias|S|array con dias semana 0-6 NOT NULL, puede ir vacio si no se repite|

# Gestor de dinero
### Cuenta - cuenta
| Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|cantidad|N|NOT NULL, defecto 0|

### Tipo Movimiento - tipo_movimiento
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|tipo_movimiento|S|NOT NULL [transferencia,ingreso,gasto]|

### Ingreso - ingreso
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id|N|cuenta.id NOT NULL|
|tipo_movimiento_id|N|tipo_movimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Gasto - gasto
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id|N|cuenta.id NOT NULL|
|tipo_movimiento_id|N|tipo_movimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Transferencia - transferencia
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id_origen|N|cuenta.id NOT NULL|
|cuenta_id_destino|N|cuenta.id NOT NULL|
|tipo_movimiento_id|N|tipo_movimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Presupuesto - presupuesto
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cantidad|N|NOT NULL|
|descripcion|S||
|datetime_comienzo|S|por defecto now() NOT NULL|
|datetime_fin|S|NOT NULL|
|tipo_movimiento_id|N|tipo_movimiento.id NOT NULL