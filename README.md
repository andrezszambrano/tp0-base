# TP0: Docker + Comunicaciones + Concurrencia

Nota: todos los comandos hay que ejecutarlo en la carpeta root del repositorio.

## Parte 1: Introducción a Docker
En esta primera parte del trabajo práctico se plantean una serie de ejercicios que sirven para introducir las herramientas básicas de Docker que se utilizarán a lo largo de la materia. El entendimiento de las mismas será crucial para el desarrollo de los próximos TPs.

### Ejercicio N°1:
Modificar la definición del DockerCompose para agregar un nuevo cliente al proyecto.

### Ejercicio N°1.1:
Para ejecutar el script: python create-compose-yaml-n-clients.py N, siendo N >= 1

### Ejercicio N°2:
Al ejecutar make docker-compose-up, los contenedores van a poder acceder a su correspondiente archivo de configuración sin necesidad de configuración extra.

Si se quiere modificar un archivo de configuración pero sin tener que pasar por el proceso del build, se puede ejecutar el comando:  
make docker-compose-up-without-build.

### Ejercicio N°3:
Para ejecutar el test, traerse lo que está en la rama ej.3 y ejecutar el comando:  
make docker-compose-test. Se deberá ver en pantalla el mensaje "test passed".

### Ejercicio N°4:
Nota: el cliente ahora está en python, así que para configurarlo hay que modificar el archivo config.ini en la carpeta del cliente.  

Para verificar que ambos programas finalizan de forma _graceful_:  
Traerse la rama ej.4 y ejecutar:
make docker-compose-up
make docker-compose-stop
make docker-compose-log
En los que se verá un mensaje "action: sigterm detected, {client||server} shutdowned | result: success" de acuerdo al proceso que finalizó.

## Parte 2: Repaso de Comunicaciones

Nota: por una cuestión de modelado que se realizó previamente al uso de las funciones load_bets y store_bets (ya que no sabía que ya habían provisto una clase Bet), el parseo de los datos (por ej. la fecha de nacimiento) que en el código dado por la catedra lo realiza la propia Bet, pasa a ser responsabilidad del que crea la Bet, por lo que se termina realizando afuera del constructor del mismo. 

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
Traerse la rama ej.7 y ejecutar un make docker-compose-up. Se deberá ver por pantalla la cantidad de ganadores por cada agencia

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
Traerse la rama ej.8 y ejecutar un make docker-compose-up. Se deberá ver por pantalla la cantidad de ganadores por cada agencia como en el inciso anterior.

client5  | 2023-03-30 05:08:13 INFO     action: consulta_ganadores | result: success | cant_ganadores: $0
client3  | 2023-03-30 05:08:13 INFO     action: consulta_ganadores | result: success | cant_ganadores: $3
client4  | 2023-03-30 05:08:14 INFO     action: consulta_ganadores | result: success | cant_ganadores: $2
client2  | 2023-03-30 05:08:14 INFO     action: consulta_ganadores | result: success | cant_ganadores: $3
client1  | 2023-03-30 05:08:15 INFO     action: consulta_ganadores | result: success | cant_ganadores: $2

##### Concurrencia  
Hay tres tipos de procesos:  
1. El principal, que se encarga de crear los otros procesos y finalizar los otros procesos. Solo hay uno.
2. El aceptador, que se encarga de aceptar nuevos sockets y pasarselo al proceso principal a través de una cola. Solo hay uno.
3. El manejador de cliente, que se encarga de hacer las peticiones del cliente. Hay uno por socket inicializado, es decir, uno por cliente, en este caso cinco. Una vez terminado, el manejador le avisa al proceso principal a través de una cola que su proceso terminó.

Para sincronizar que todos los manejadores de cliente esperen a que todos sus compañeros hayan terminado se utiliza una barrera. Cuando el cliente le pida a su manejador que le pase la lista de ganadores, va y espera en la barrera. Cuando todos los procesos estén esperando en la misma, significa que ya todos terminaron y ya se puede regresar la información acordemente. La barrera espera cinco clientes y no es configurable, al menos en primera instancia, ya que el enunciado deja claro que solo son cinco agencias. 

Además, Hay un monitor al que todos los manejadores de cliente van a tener acceso, el de la base de datos. Para escribir en la misma hay que tomar un lock. Como para el momento en el que las agencias cargan los ganadores de la base de datos ya no hay ninguna escribiendo información, no es necesario usar el lock.

##### Protocolo
Dado el nuevo modelo, el protocolo cambió mínimamente para acomodar el modelo. Como una vez aceptado un socket se crea un nuevo proceso que va a almacenar el mismo, no es necesario que el cliente se vuelva a conectar cada vez que quiere enviar un paquete. Por lo tanto, el cliente al conectarse va a enviar su número de agencia, y ya no es necesario volverlo a enviar para el resto de los mensajes.

También el cliente ya no se hace pooling para obtener los ganadores. Ahora, el cliente le pide al servidor que mande los ganadores, y el servidor lo va a mandar eventualmente (dependiendo de cuándo terminen las otras agencias).

##### Falencias del sistema
Si el sistema (clientes + proceso de los servidores) termina de forma natural, se liberan todos los recursos acordemente. Sin embargo, por falta de tiempo el sistema no aguanta sigterms ni en el cliente ni en el servidor. 
Tampoco están contemplado el caso en el cliente el caso en el que se cae la conexión y que hay que volver a conectarse al servidor, y que el servidor no libera el proceso del cliente caido (la única forma de liberarlo es que el proceso termine sin ningún error).
