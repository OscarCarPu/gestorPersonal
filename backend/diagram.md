# Gestor de Proyectos
### Proyecto
| Atributo|Tipo|Comentarios|
|-----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|datetime_creacion|S|valor fijo, now() NOT NULL|
|minutos_dedicados|N|suma minutos_dedicados hijos|
|estado|S|[nuevo, en curso, en pausa, en espera, cerrado] NOT NULL|
|descripcion|S||
|etiquetas|S|Array con etiquetas|

### Tiempo dedicado
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|tarea_id|N|Tarea.id NOT NULL|
|minutos|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|N||

### Tarea
| Atributo|Tipo|Comentarios|
|-----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|proyecto_id|N|Proyecto.id NOT NULL|
|padre_id|N|Tarea.id|
|minutos_estimados|N||
|minutos_dedicados|N|por defecto 0 NOT NULL|
|minutos_dedicados_total|N|suma minutos_dedicados hijos|
|prioridad|N|[0-5]|
|datetime_creacion|S|valor fijo, now() NOT NULL|
|datetime_fecha_limite|S||
|estado|S|[nuevo, en curso, en pausa, en espera, cerrado] NOT NULL|
|descripcion|S||

# Gestor de dinero
### Cuenta
| Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|cantidad|N|NOT NULL, defecto 0|

### Tipo Movimiento
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|nombre|S|NOT NULL|
|tipo_movimiento|S|NOT NULL [transferencia,ingreso,gasto]|

### Ingreso
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id|N|Cuenta.id NOT NULL|
|tipo_movimiento_id|N|TipoMovimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Gasto
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id|N|Cuenta.id NOT NULL|
|tipo_movimiento_id|N|TipoMovimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Transferencia
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cuenta_id_origen|N|Cuenta.id NOT NULL|
|cuenta_id_destino|N|Cuenta.id NOT NULL|
|tipo_movimiento_id|N|TipoMovimiento.id NOT NULL|
|cantidad|N|NOT NULL|
|datetime|S|NOT NULL, por defecto now()|
|descripcion|S||

### Presupuesto
|Atributo|Tipo|Comentarios|
|----|----|----|
|id|N|AUTOINCREMENT|
|cantidad|N|NOT NULL|
|descripcion|S||
|datetime_comienzo|S|por defecto now() NOT NULL|
|datetime_fin|S|NOT NULL|
|tipo_movimiento_id|N|TipoMovimiento.id NOT NULL|