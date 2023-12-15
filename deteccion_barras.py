import cv2
from pyzbar import pyzbar

def scanner_barras():
    # PARA VIDEO EN TIEMPO REAL CON CAMARA WEB
    #captura = cv2.VideoCapture(0)

    # PARA CAMARA DEL CELULAR O CAMARA NORMAL
    # PARA CONEXION CON UNA RED
    #url_camara = 'http://192.168.20.2:4747/video'

    # PARA CONEXION POR CABLE USB AL DISPOSITIVO
    #url_camara = 'http://192.168.20.2:8080/video'
    # PARA DROID CLIENT
    url_camara = 1
    captura = cv2.VideoCapture(url_camara)

    # Definir el tamaño de la ventana
    tamanio_ventana = (960, 540)
    # Se define en nombre de la ventana donde se vera lo que capte la camara asi como decimos que sea de tamaño normal
    cv2.namedWindow('Camara Movil', cv2.WINDOW_NORMAL)
    # Ajustamos el tamaño de la ventana con nuestro tamaño deseado que definimos anteriormente
    cv2.resizeWindow('Camara Movil', *tamanio_ventana)


    # Verificar si la cámara se abrió correctamente
    if not captura.isOpened():
        print("La captura de video ha fallado")

    # Bucle principal para la captura de video
    while captura.isOpened():
        # ret es el valor de retorno de los fotogramas de forma exitosa
        # frame es el cuadro de video que se esta leyendo o tambien conocido como fotograma
        ret, frame = captura.read()

        # Verificar si se pudo leer el fotograma correctamente
        if ret == True:
            # Decodificar códigos de barras en el fotograma
            codigos_barras = pyzbar.decode(frame)

            # Iterar sobre todos los códigos de barras detectados en el fotograma
            for codigo_barra in codigos_barras:
                # Obtener las coordenadas del rectángulo que encierra el código de barras
                (x, y, w, h) = codigo_barra.rect

                # Dibujar un rectángulo alrededor del código de barras en el fotograma
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Obtener los datos y el tipo de código de barras decodificado
                codigo_barra_data = codigo_barra.data.decode("utf-8")
                codigo_barra_type = codigo_barra.type

                # Crear un texto con la información del código de barras y dibujarlo en el fotograma
                texto_codigo = "{} ({})".format(codigo_barra_data, codigo_barra_type)
                cv2.putText(frame, texto_codigo, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Imprimir información sobre el código de barras encontrado en la consola
                print("[INFORMACION] Estandar {} codigo: {}".format(codigo_barra_type, codigo_barra_data))

            # Mostrar el fotograma con los códigos de barras detectados en una ventana
            cv2.imshow('Camara Movil', frame)

            # Esperar una tecla para salir del bucle (presiona 'esc' para salir)
            if cv2.waitKey(25) == 27:
                break
        else:
            # Salir del bucle si no se pudo leer el fotograma
            break

    # Liberar los recursos (cerrar la conexión con la cámara)
    captura.release()

    # Cerrar todas las ventanas abiertas
    cv2.destroyAllWindows()
