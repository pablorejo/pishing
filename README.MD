# PISHING CON CHAT GPT
Este programa genera correos electronicos usando chat-gpt de forma personalizada pudiendo especificar el nombre y la funcion de la empresa para que te donen dinero en una determinada url previamente especificada
Ademas también podemos generar correos electronicos de manera masiva para enviar estos mismos correos

## Configuracion
La configuracion se hace en la parte de [variable.py](variables.py)

### Correo
Para la configuración de correo es necesario especificar el correo que va a enviar los mensajes
```python
# Correo desde el que vamos a enviar los mensajes
CORREO_EMISOR = "tu-correo@lo-que-sea"
```

Ademas debemos configurar el servidor SMPT que ira cambiando segun si usamos gmail o algun otro servicion:

Ejemplo para usar gmail
```python 
# Configuracion del servidor SMTP
EMAIL_SMPT = "smtp.gmail.com" 
PUERTO_SMPT = '587'
```

## Modelo de chat-gpt que vamos a usar
Por ahora solo lo he probado con estos y el que mejor funciona es gpt-4
```python
# Modelo que vamos a usar en el chat
Modelos_de_chat = {1:"gpt-3.5-turbo" , 2:"gpt-4"}
MODELO_DEL_CHAT = Modelos_de_chat[2]
```

## Objetivos y nombre de la empresa
Para la configuracion del nombre de la empresa los objetivos de esta hay dos maneras principales

### Generar automaticamente con chat-gpt
```python
GENERAR_OBJETIVOS = True
```

Y donde podemos especificar el numero distinto de empresas que se van a crear:
```python
# Numero de empresas a generar
NUMERO_DE_EMPRESAS = 3
```

### Configurar manualmente una empresa
```python
# En caso de que queramos que sea con un objetivo en concreto
NOMBRE_EMPRESA = "Perros sin casa"
IMAGEN_EMPRESA = "https://imgmedia.larepublica.pe/640x371/larepublica/original/2022/07/27/62e168ce1c95403984781dba.webp"
OBJETIVO_EMPRESA = "Eres una organizacion que busca ayudar a los perros callejeros"
```

## Imagenes que se envian
Las imagenes son creadas con dalle de open-ai
Y podemos configurar el numero de imagenes creadas así como la carpeta donde se guardará
```python
# Numero de imagenes maximo en caso de generar automaticamente las empresas
NUMERO_DE_IMAGENES = 1
# Carpeta donde se guardaran las imagenes
CARPETA_IMAGENES = "imagenes/"
```

## Generacion de correos
Si se establece como a True se enviaran a correos generados automaticamente. 
```python
GENERAR_CORREOS = False # En caso de querer generar los correos aleatoriamente
```
**Cuiadado con enta funcionalidad**: Este programa es solo un ejemplo no mandeis correos a gente que no conoceis :\(


### Configuracion de correos
Aquí podemos especificar como generar las direcciones de correos electrónicos 
- El numero de direcciones de correo electronico
- Las terminaciones distintas por las que van a terminar los correos electronicos
- Si queremos guardar el resultado en un fichero llamado correos_2.txt
- Numero maximo de nombres y apellidos que va a generar el chat. Esto es mejor que no lo toqueis pues así funciona bien

```python
NUMERO_DE_CORREOS = 1000000 # Es aproximado al alza es decir nunca va ser menor que este numero 
TERMINACIONES_CORREOS = ["hotmail.com","yahoo.com","outlook.com","yahoo.co.uk","gmail.com"]
GUARDAR_EN_FICHERO = True
NUMERO_MAX_GENERADO_CHAT = 50 # Esta opcion sera la que diga el numero maximo de nombres y apellidos que el chat puede generar.
```