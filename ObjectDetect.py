import torch
import cv2
import numpy as np

# Cargar modelo ONNX
model = torch.hub.load('ultralytics/yolov5', 'custom', 
                       path='yolov5l6.pt', force_reload=True)  

colors = {
  "Red": [(90, 150), 0.4, 0.8], 
  "Pink": [(15, 20), 0.4, 0.7],
  "Orange": [(25, 28), 0.5, 0.8],
  "Yellow": [(60, 90), 1, 0.5],  
  "Green": [(60, 90), 1, 0.7] ,  
  "Blue": [(20, 30), 0.5, 0.8],
}

# Mapeo de clases
classes = model.names

def rgb_to_hsv(rgb):
  return cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

# Estimar color por tono   
def estimate_color(hsv,name):

    h,s,v = cv2.split(hsv)

    h_mean = h.mean()
    s_mean = s.mean() 
    v_mean = v.mean()   
    
    for name, ranges in colors.items():
        h_min, h_max = ranges[0]
        s_min, v_min = ranges[1], ranges[2]
        
        if h_min < h_mean < h_max and s_mean > s_min and v_mean > v_min:
            return name
    

    return "Unknown"
def video():
    # Inicializar video
    cap = cv2.VideoCapture(0) 
    cap.set(3, 1280)
    cap.set(4, 820)


    # Convertir a HSV

    while True:

    # Leer frame
        ret, frame = cap.read()

    # Redimensionar frame al tamaño de entrada del modelo
    

    # Realizar detección
        detections = model(frame)

    # Iterar sobre detecciones
        for detection in detections.xyxy[0]:
            class_id = int(detection[5])  
            class_name = classes[class_id]

            # Coordenadas de la bbox
            x1, y1, x2, y2 = map(int, detection[:4])

            # Extraer región
            bbox = frame[y1:y2, x1:x2]

            # Convertir a HSV
            hsv = rgb_to_hsv(bbox)

            # Estimar color
            color = estimate_color(hsv,class_name)
            
            if class_name == 'banana':
                if color != "Yellow":
                    color = "Mal estado"
                    text = f"{class_name} - {color}"
                    #print("Color de banana diferente a amarillo")  
                else:
                    color = "Buen estado"
                    text = f"{class_name} - {color}"

            if class_name == 'apple':
                if color != "Red":
                    color = "Mal estado"
                    text = f"{class_name} - {color}"
                    #print("Color de banana diferente a amarillo")  
                else:
                    color = "Buen estado"
                    text = f"{class_name} - {color}"

            if class_name == 'broccoli':
                if color == "Red" :
                    color = "Mal estado"
                    text = f"{class_name} - {color}"
                    #print("Color de banana diferente a amarillo")  
                else:
                    color = "Buen estado"
                    text = f"{class_name} - {color}"
            #print(color)
            
            # Clase    
            class_id = int(detection[5])  
            class_name = classes[class_id]

            # Confianza
            confidence = detection[4]

            # Dibujar bbox
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

    # Dibujar bbox y texto
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,255), 2)
        text = f"{class_name} - {color}"  
        cv2.putText(frame, text, (x1,y1),cv2.FONT_HERSHEY_PLAIN,1.5,(0,0,255),2)

        # Mostrar resultado  
        cv2.imshow('Detecciones', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # Liberar recursos
    cap.release()  
    cv2.destroyAllWindows()