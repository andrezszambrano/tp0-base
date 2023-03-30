# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker
En esta primera parte del trabajo práctico se plantean una serie de ejercicios que sirven para introducir las herramientas básicas de Docker que se utilizarán a lo largo de la materia. El entendimiento de las mismas será crucial para el desarrollo de los próximos TPs.

### Ejercicio N°1:
Modificar la definición del DockerCompose para agregar un nuevo cliente al proyecto.

### Ejercicio N°1.1:
Definir un script (en el lenguaje deseado) que permita crear una definición de DockerCompose con una cantidad configurable de clientes.

### Ejercicio N°2:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera un nuevo build de las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (`config.ini` y `config.yaml`, dependiendo de la aplicación) debe ser inyectada en el container y persistida afuera de la imagen (hint: `docker volumes`).

### Ejercicio N°3:
Crear un script que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. Dado que el servidor es un EchoServer, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado. Netcat no debe ser instalado en la máquina _host_ y no se puede exponer puertos del servidor para realizar la comunicación (hint: `docker network`).

### Ejercicio N°4:
Modificar servidor y cliente para que ambos sistemas terminen de forma _graceful_ al recibir la signal SIGTERM. Terminar la aplicación de forma _graceful_ implica que todos los _file descriptors_ (entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag `-t` utilizado en el comando `docker compose down`).

## Parte 2: Repaso de Comunicaciones

Las secciones de repaso del trabajo práctico plantean un caso de uso denominado **Lotería Nacional**. Para la resolución de las mismas deberá utilizarse como base al código fuente provisto en la primera parte, con las modificaciones agregadas en el ejercicio 4.

### Ejercicio N°5:
Para ejecutar, traerse la rama ej.5 y ejecutar un make docker-compose-up. Se deberá ver por pantalla el log 2023-03-30 03:59:35 INFO     action: apuesta_enviada | result: success | dni: $30904465 | numero: $12345.

##### Protocolo
Para el ejercicio 5 solo fue necesario generar dos tipos de mensaje: el realizar apuesta, que manda el cliente al servidor, y el de confirmación que manda el servidor al cliente. Al ser el primero de estos bastante abarcativo, se creó el código base para mandar bytes que pueden representar carácteres, strings, números y fechas, que se usa en los siguientes ejercicios.

El protocolo para mandar una apuesta es el siguiente:  
B + número_agencia (1 byte) + largo_string (1 byte) + nombre + largo_string (1 byte) + apellido + documento (4 bytes) + largo_fecha (1 byte) + fecha (formato "%Y-%m-%d") + número_apuesta (4 bytes). Si se supone que un nombre y apellido promedio tiene menos de 10 y 15 carácteres respectivamente, poniéndose en ese peor caso y teniendo en cuenta que una fecha en ese formato ocupa 10 bytes, el tamaño total del paquete será de 48 bytes.

### Ejercicio N°6:
Traerse la rama ej.6 y ejecutar un make docker-compose-up. Se deberá ver por pantalla el 
log 2023-03-30 03:59:35 INFO     action: apuesta_enviada | result: success | dni: $30904465 | numero: $12345.
Para ajustar el tamaño del batch, ir al volumen de configuración del cliente y cambiar el número al acorde. Recordar que el tamaño de un paquete debe ser de menos de 8kB, si se usa como referencia los 48 bytes por apuesta que se mencionó el inciso anterior, el tamaño máximo de un batch es de 170 apuestas.

##### Protocolo
Para este ejercicio se modificó el protocolo levemente: Ahora se manda una lista de apuestas (el batch). Por cada apuesta se envía la información como en el protocolo anterior, solo que en vez de mandar el número de agencia siempre, se manda al principio del batch para ahorrar potencialmente hasta 170 bytes por paquete (uno por apuesta). Cuando se termina de mandar todas las apuestas de un batch, se manda un carácter para que el servidor sepa que ya no debe esperar más apuestas.


### Ejercicio N°7:
Traerse la rama ej.7 y ejecutar un make docker-compose-up. Se deberá ver por pantalla la cantidad de ganadores por cada agencia/
client5  | 2023-03-30 05:08:13 INFO     action: consulta_ganadores | result: success | cant_ganadores: $0
client3  | 2023-03-30 05:08:13 INFO     action: consulta_ganadores | result: success | cant_ganadores: $3
client4  | 2023-03-30 05:08:14 INFO     action: consulta_ganadores | result: success | cant_ganadores: $2
client2  | 2023-03-30 05:08:14 INFO     action: consulta_ganadores | result: success | cant_ganadores: $3
client1  | 2023-03-30 05:08:15 INFO     action: consulta_ganadores | result: success | cant_ganadores: $2

##### Protocolo
Para este ejercicio se añadieron unos mensajes adicionalmente a los que ya estaban. Después de mandar todos los batches, el cliente le envia al servidor que ya terminó de procesar, para esto le envía un carácter (Z) y el número de la agencia a la que representa. El servidor la procesa y le retorna un OK.
Ahora bien, los clientes también le preguntan al servidor por la cantidad de ganadores. Para esto, le envía un carácter (W) y el número de la agencia. Para responder esto, el servidor tiene dos posibilidades: que no todas las agencias hayan terminado, por lo que responde con un carácter (F) por lo que el cliente sabe que tiene que preguntar más tarde, o la otra es que todas sí hayan terminado y el servidor le retorne la lista de documentos, cada uno ocupando un byte. Cabe recalcar que como la lista va a ser pequeña, este paquete nunca va a superar los 8Kb.


## Parte 3: Repaso de Concurrencia

### Ejercicio N°8:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo.
En este ejercicio es importante considerar los mecanismos de sincronización a utilizar para el correcto funcionamiento de la persistencia.

En caso de que el alumno implemente el servidor Python utilizando _multithreading_,  deberán tenerse en cuenta las [limitaciones propias del lenguaje](https://wiki.python.org/moin/GlobalInterpreterLock).

## Consideraciones Generales
Se espera que los alumnos realicen un _fork_ del presente repositorio para el desarrollo de los ejercicios.
El _fork_ deberá contar con una sección de README que indique como ejecutar cada ejercicio.
La Parte 2 requiere una sección donde se explique el protocolo de comunicación implementado.
La Parte 3 requiere una sección que expliquen los mecanismos de sincronización utilizados.

Finalmente, se pide a los alumnos leer atentamente y **tener en cuenta** los criterios de corrección provistos [en el campus](https://campusgrado.fi.uba.ar/mod/page/view.php?id=73393).
