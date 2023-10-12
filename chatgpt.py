import sys, requests, math, re, time
import openai
import variables

from unidecode import unidecode

openai.api_key = variables.CLAVE_API
directorio = variables.CARPETA_IMAGENES
def CrearLogo(nombre_empresa, numero):
    print(f"\nCreando logo para la empresa: {nombre_empresa}")

    crear_logo = f"Crea un logo para una empresa llamada {nombre_empresa}"
    crear_imagen = f"Crea una imagen relacionada con este tema {nombre_empresa} sin que aparezcan lestras"
    if (numero > 0):
        prompt = crear_imagen
    else:
        prompt = crear_logo

    response = openai.Image.create(
        prompt= prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    print("Logo creado\n")

    # URL de la imagen que deseas descargar
    url = image_url

    # Realiza una solicitud GET para obtener la imagen
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtén el contenido de la imagen
        imagen_data = response.content

        # Guarda la imagen en un archivo local
        with open(f"{directorio}nombre_de_la_imagen_{numero}.jpg", "wb") as f:
            f.write(imagen_data)

        print("Imagen descargada exitosamente.")
    else:
        print("No se pudo descargar la imagen. Código de estado:", response.status_code)


    return image_url

def CrearLogos(nombre_empresa,n_imagenes):
    for n in range(0,n_imagenes):
        CrearLogo(nombre_empresa,n)

def ObtenerNombreCorreo(correo):
    print(f"Obteniendo nombre del correo {correo}")
    nombre = str(correo).split("@")[0]

    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": "Eres máquina capaz de parsear nombre de manera legible, ejm: pablopiorejoiglesias -> Pablo Pío Rejo Iglesias"},
            {"role": "user", "content": f"Parsea este nombre {nombre} y muestrame solomente el nombre parseado sin ningun otro mensaeje"},
        ]
        
    )
    respuesta = response['choices'][0]['message']['content']
    print(f"Nombre Obtenido: {respuesta}")
    return respuesta

def ObtenerAsunto(objetivo=variables.OBJETIVO_EMPRESA):
    print(f"Obteniendo el asunto para el correo electrónico")

    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": objetivo},
            {"role": "user", "content": "Dime un asunto para poner de asunto en un correo electronico para que donen dinero a mi organizacion , muestrame solo el asunto sin nada mas"},
        ]
    )
    respuesta = response['choices'][0]['message']['content']


    asuntos = ["Asunto: ","Asunto:","asunto: ","asunto:","Asunto ","Asunto"]
    for asunto in asuntos:
        if (asunto in respuesta):
            respuesta = str(respuesta).replace(asunto,"")


    print(f"El asunto obtenido ha sido: {respuesta}")
    return respuesta

def CrearCorreo(
    correo,
    # Load your API key from an environment variable or secret management service
    nombre_empresa = variables.NOMBRE_EMPRESA,
    nombre_person = variables.NOMBRE_PERSONA_EMPRESA,
    url = variables.URL_DONACION,
    numero_de_lineas_max = variables.NUMERO_DE_LINEAS_MAX,
    numero_de_lineas_min = variables.NUMERO_DE_LINEAS_MIN,
    objetivo_empresa = variables.OBJETIVO_EMPRESA):

    CrearLogos(nombre_empresa,variables.NUMERO_DE_IMAGENES)


    nombre_cliente = ObtenerNombreCorreo(correo)

    contenido = f"""Crea una plantilla html para un correo electrónico para que la gente te done dinero, tienes que usar estos nombres
    nombre de empresa: {nombre_empresa}
    nombre de la persona que manda el correo: {nombre_person}
    nombre del cliente: {nombre_cliente}
    url para donar dinero: {url}
    Hazlo con un minimo de {numero_de_lineas_min} lineas y un maximo de {numero_de_lineas_max} lineas"""

    decorador = """Incluye de manera que queden bonito el html estas imagenes en el orden que tu crear conveniente
    """
    if (variables.NUMERO_DE_IMAGENES == 1):
        contenido += f"{decorador}Incluye esta imagen: <img src=\"cid:imagen_adjunta_0\" width=\"300\" height=\"300\" alt=\"Texto alternativo\">\n"
    elif (variables.NUMERO_DE_IMAGENES > 1):
        contenido += "Incluye estas imagenes:\n"
        for n in range(0,variables.NUMERO_DE_IMAGENES):
            contenido += f"{decorador}\t<img src=\"cid:imagen_adjunta_{n}\" width=\"300\" height=\"300\" alt=\"Texto alternativo\">\"\n"

    if (not variables.GENERAR_OBJETIVOS):
        contenido += "url para donar dinero: {url}"

    print("Creando Correo")
    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": objetivo_empresa},
            {"role": "user", "content": contenido},
        ]
        
    )
    respuesta = response['choices'][0]['message']['content']
    respuesta = "<" + str(respuesta).split("<",maxsplit=1)[1]
    print ("Correo creado")
    return respuesta

def GenerarNombresYObjetivos():
    print("Generando nombres de empresas y objetivos")
    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": "Eres máquina que solo da la respuesta sin nada mas"},
            {"role": "user", "content": f"""Dime {variables.NUMERO_DE_EMPRESAS} nombres de empresas para una organizacion sin animo de lucro que busca recaudar fondos y a su lado su objetivo:
Ponmelos de esta forma:
1. NOMBRE_EMPRESA_A - OBJETIVO_EMPRESA_A
2. NOMBRE_EMPRESA_B - OBJETIVO_EMPRESA_B"""},
        ]
        
    )
    respuesta = response['choices'][0]['message']['content']

    respuesta = "1. " + str(respuesta).split("1. ",maxsplit=1)[1]
    lista = respuesta.split("\n")

    nombres_y_objetivo = []
    for nombre_objetivo in lista:
        nombre_objetivo = nombre_objetivo.split(". ",maxsplit=1)[1]
        nombre = nombre_objetivo.split(" - ")[0]
        objetivo = nombre_objetivo.split(" - ")[1]
        nombres_y_objetivo.append((nombre,objetivo))

    print("Nombres de empresas y objetivos generados\n\n")


    return nombres_y_objetivo

def GenerarCorreos():
    tiempo_inicio_GenerarCorreos = time.time()
    print("\nGenerando correos...")
    
    rango = 0
    barras = False

    n_maximo = math.pow(variables.NUMERO_MAX_GENERADO_CHAT,3)

    if (variables.NUMERO_DE_CORREOS <= n_maximo*len(variables.TERMINACIONES_CORREOS)):
        numero_de_nombres_y_apellidos = math.ceil(math.pow(variables.NUMERO_DE_CORREOS/len(variables.TERMINACIONES_CORREOS), 1/3))
    elif (variables.NUMERO_DE_CORREOS > n_maximo*len(variables.TERMINACIONES_CORREOS) and variables.NUMERO_DE_CORREOS <= 125000*len(variables.TERMINACIONES_CORREOS)*4):
        numero_de_nombres_y_apellidos = math.ceil(math.pow(variables.NUMERO_DE_CORREOS/len(variables.TERMINACIONES_CORREOS)*4, 1/3))
        barras = True
    else:
        numero_de_nombres_y_apellidos = 50
        barras = True
        rango = math.ceil(variables.NUMERO_DE_CORREOS/(n_maximo*len(variables.TERMINACIONES_CORREOS))) - 4


    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": "Eres máquina que solo da la respuesta sin nada mas"},
            {"role": "user", "content": f"""Dime {numero_de_nombres_y_apellidos} nombres tipicos de españa para poner a mi hijo de esta forma:
             1. NOMBRE_1
             2. NOMBRE_2
             3. NOMBRE_3
"""},
        ]
        
    )
    respuesta = response['choices'][0]['message']['content']

    respuesta = str(respuesta).split("1. ",maxsplit=1)[1]
    nombres = str(respuesta).split("\n")
    nombres_2 = []
    for nombre in nombres:
        nombre = unidecode(nombre.strip())
        nombre = re.sub(r'[^a-zA-Z]', '', nombre)
        nombres_2.append(nombre)
    nombres = nombres_2



    response = openai.ChatCompletion.create(
    model= variables.MODELO_DEL_CHAT,
    messages=[
            {"role": "system", "content": "Eres máquina que solo da la respuesta sin nada mas"},
            {"role": "user", "content": f"""Dime {numero_de_nombres_y_apellidos} apellidos tipicos de españa para poner a mi hijo de esta forma:
            1. APELLIDO_1
            2. APELLIDO_2
            3. APELLIDO_3
"""},
        ]
        
    )
    respuesta = response['choices'][0]['message']['content']

    respuesta = str(respuesta).split("1. ",maxsplit=1)[1]
    apellidos = str(respuesta).split("\n")
    apellidos_2 = []
    for apellido in apellidos:
        apellido = unidecode(apellido.strip())
        apellido = re.sub(r'[^a-zA-Z]', '', apellido)
        apellidos_2.append(apellido)
    apellidos = apellidos_2


    correos = []
    for terminacion in variables.TERMINACIONES_CORREOS:
        for apellido_1 in apellidos:
            for apellido_2 in apellidos:
                for nombre in nombres:
                    correos.append(f"{str(nombre).lower()}{str(apellido_1).lower()}{str(apellido_2).lower()}@{terminacion}".strip())

                    if (barras):
                        correos.append(f"{str(nombre).lower()}_{str(apellido_1).lower()}_{str(apellido_2).lower()}@{terminacion}".strip())
                        correos.append(f"{str(nombre).lower()}_{str(apellido_1).lower()}{str(apellido_2).lower()}@{terminacion}".strip())
                        correos.append(f"{str(nombre).lower()}{str(apellido_1).lower()}_{str(apellido_2).lower()}@{terminacion}".strip())

                    if rango > 0:
                        for n in range(1,rango+1):
                            correos.append(f"{str(nombre).lower()}{str(apellido_1).lower()}{str(apellido_2).lower()}{n}@{terminacion}".strip())

                    

    
    tiempo_fin_GenerarCorreos = time.time()
    tiempo_total = tiempo_fin_GenerarCorreos - tiempo_inicio_GenerarCorreos

    print(f"Se han generado {len(correos)} en {tiempo_total:.2f} segundos") 

    if (variables.GUARDAR_EN_FICHERO):
        GuardarCorreos(correos)

    return correos

def GuardarCorreos(correos):
    with open('correos_2.txt', 'w') as archivo:
        for correo in correos:
            archivo.write(correo + "\n")
        archivo.close()

if __name__ == "__main__":
    GenerarCorreos()