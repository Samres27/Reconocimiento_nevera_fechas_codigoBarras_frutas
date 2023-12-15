# Importamos las dependencias
import easyocr
from dateutil.parser import parse
import cv2
import numpy as np
import os
from datetime import datetime
# Definimos los nombres de las capas de la red EAST que nos interesan.
class fechasOCR:
    
    
    
    def decode_predictions(self,scores, geometry, min_confidence=0.5):
        #este metodo nos permite crear los respectivos rectangulos verdes que identifican las partes con texto
        num_rows, num_cols = scores.shape[2:4]
        rectangles = []
        confidences = []

        # Iteramos sobre el número de filas
        for y in range(num_rows):
            # Extraemos las probabilidades y la data geométrica utilizada para potencialmente
            # derivar los rectángulos del texto detectado.
            scores_data = scores[0, 0, y]
            x_data_0 = geometry[0, 0, y]
            x_data_1 = geometry[0, 1, y]
            x_data_2 = geometry[0, 2, y]
            x_data_3 = geometry[0, 3, y]
            angles_data = geometry[0, 4, y]

            # Iteramos sobre las columnas
            for x in range(num_cols):
                # Extraemos el puntaje
                score = float(scores_data[x])

                # Si la detección es débil, la ignoramos.
                if score < min_confidence:
                    continue

                # Calculamos el desfase dado que los resultados de la red serán 4 veces más pequeños
                # que la imagen original.
                offset_x, offset_y = x * 4., y * 4.

                # Extraemos el ángulo de rotación y calculamos el seno y el coseno del mismo
                angle = angles_data[x]
                cosine = np.cos(angle)
                sine = np.sin(angle)

                # Derivamos el ancho y la altura del rectángulo
                height = x_data_0[x] + x_data_2[x]
                width = x_data_1[x] + x_data_3[x]

                # Usamos el desfase y el ángulo de rotación para comenzar el cálculo del rectángulo rotado.
                offset = ([
                    offset_x + (cosine * x_data_1[x]) + (sine * x_data_2[x]),
                    offset_y - (sine * x_data_1[x]) + (cosine * x_data_2[x])
                ])

                # Derivamos las esquinas del rectángulo
                top_left = (-sine * height) + offset[0], (-cosine * height) + offset[1]
                top_right = (-cosine * width) + offset[0], (sine * width) + offset[1]

                # Calculamos el centro del rectángulo
                center_x = .5 * (top_left[0] + top_right[0])
                center_y = .5 * (top_left[1] + top_right[1])

                box = ((center_x, center_y), (width, height), -1 * angle * 180. / np.pi)

                rectangles.append(box)
                confidences.append(score)

        return rectangles, confidences


    def __init__(self):
        EAST_OUTPUT_LAYER = [
        'feature_fusion/Conv_7/Sigmoid',
        'feature_fusion/concat_3'
        ]
        # cargamos el reader con el idioma español y especificando que vamos a usar cpu
        reader = easyocr.Reader(["es"], gpu=False)
        print('Cargando el detector EAST...')
        print('getcwd:      ', os.getcwd())
        east="./frozen_east_text_detection.pb"
        #para opencv vamos a usar un modelo ya entrenado por lo cula los cargamos para nuestra red
        network = cv2.dnn.readNet(east)
        min_confidence=0.5
        nms_threshold=0.4
        width=320
        height=320
        padding=0.1

        #fuente = 0 #camara laptop
        #fuente = 'http://192.168.0.2:8080/video'#app android
        fuente = 1 # app dorid cam client
        cap=cv2.VideoCapture(fuente) 


        while(1):
            # extraemos los frames de la camara 
            ok,image=cap.read()
            image=cv2.resize(image, (500, 400))
            if(cv2.waitKey(1)==ord('q')):
                break
                

            # Extraemos las dimensiones de la imagen
            original_height, original_width = image.shape[:2]
            # Fijamos las nuevas dimensiones y calculamos el ratio entre las dimensiones viejas y nuevas
            new_width, new_height = width,height
            ratio_width = original_width / float(new_width)
            ratio_height = original_height / float(new_height)

            
            # Convertimos la imagen en un blob y la pasamos por la red.
            blob = cv2.dnn.blobFromImage(image, 1., (new_width, new_height), (123.68, 116.78, 103.94), swapRB=True, crop=False)
            
            network.setInput(blob)
            scores, geometry = network.forward(EAST_OUTPUT_LAYER)
            # Llamamos al metodo para que nos de los rectangulos que necesitamos dibujar en la imagen
            rectangles, confidences = self.decode_predictions(scores, geometry, min_confidence)
            indices = cv2.dnn.NMSBoxesRotated(rectangles, confidences, min_confidence, nms_threshold)

            if len(indices) > 0:
                for i in indices.flatten():
                    box = cv2.boxPoints(rectangles[i])
                    box[:, 0] *= ratio_width
                    box[:, 1] *= ratio_height
                    box = np.int0(box)
                    
                    # Dibujamos el rectángulo rotado
                    cv2.polylines(image, [box], True, (0, 255, 0), 2)
            # Dibujamos el ractangulo del centro
            pts = np.array([[150, 150], [350, 150],
                        [350, 250], [150,250],
                        ],
                    np.int32)
            cv2.polylines(image, [pts], True, (0, 0, 0), 2)
            cv2.imshow('Resultado', image)
            
        #reconer con ocr

        cap.release()
        # Mostramos el resultado.

        #recortamos la secion que es esta dentro del rectangulo negro
        image=image[150:250,150:350]
        
        # Llamaos al metodo de easyOcr para que pueda extraer el contenido que tiene
        result = reader.readtext(image, paragraph=False,allowlist="enro, fbmazilyjugstpcvd/.-1234567890ENROFBMAZILYJUGSTPCVD")
        fechas=[]
        # Extraemos la fechas que encontro en el pedaso de imagen que tenemos
        for x in result:
            fcan=x[1]
            if(("/" in fcan) or ("." in fcan ) or ("-" in fcan) ):
                fechas.append(fcan)

        # imprimimos las fechas del producto para poder clasificar cual es la fecha de vencimiento
        if(len(fechas)==0):
            print("no se encontro fecha alguna")
        else:
            #con esta clasificacion estamos tomando en cuenta que el usuario puso la fecha de vencimiento en el rectangulo   
            for y in range(len(fechas)):
                try:
                    f1=parse(fechas[0])
                    f2=parse(fechas[y])
                    print("fecha"+" "+str(y)+ " :"+fechas[y])
                        
                    if f1<f2:
                        fechas[0]=fechas[y] 
                except:
                    print("la fecha %s no es valida para analizar"%(fechas[y]))
            print("el producto vence: " +fechas[0])
            
                
                

        cv2.imshow("alfinal",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
