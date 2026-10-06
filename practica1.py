import time
import cv2
import numpy as np
from PIL import Image

# 1. Rutas de los archivos
input_video_path = 'vib.webm'
output_video_path = 'video_secuencial.mp4'

# Abrir el video original
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print("Error al abrir el video de entrada.")
    exit()

# Obtener propiedades del video
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Objeto para guardar el nuevo video en blanco y negro
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

# Medir tiempo inicial
start_time = time.time()
frame_count = 0

print("Procesando video... Presiona 'q' para salir.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Conversión de BGR a RGB para Pillow
    color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)

    # Convertir a blanco y negro con Pillow
    pil_gray = pil_image.convert('L')

    # Convertir de vuelta a NumPy para OpenCV
    gray_frame = np.array(pil_gray)

    # Guardar el fotograma en el archivo de salida
    out.write(gray_frame)

    # MOSTRAR EL VIDEO EN BLANCO Y NEGRO EN PANTALLA
    cv2.imshow('Video en Blanco y Negro', gray_frame)

    frame_count += 1

    # Permite cerrar la ventana si presionas la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar memoria y cerrar ventanas
cap.release()
out.release()
cv2.destroyAllWindows()

# Medir tiempo final
end_time = time.time()
total_time = end_time - start_time

print(f"\n¡Video generado exitosamente!")
print(f"Archivo guardado como: {output_video_path}")
print(f"Fotogramas procesados: {frame_count}")
print(f"Tiempo total: {total_time:.2f} segundos ({total_time / 60:.2f} minutos)")