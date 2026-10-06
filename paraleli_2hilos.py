import time
import cv2
import numpy as np
from concurrent.futures import ProcessPoolExecutor

# Función para convertir un frame a blanco y negro
def convertir_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def main():
    # 1. Rutas de los archivos
    input_video_path = 'vib.webm'
    output_video_path = 'video_2hilos.mp4'

    # Abrir el video original
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error al abrir el video de entrada.")
        return

    # Obtener propiedades del video
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Objeto para guardar el nuevo video en blanco y negro
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    # Parámetros de paralelismo
    chunk_size = 100   # número de frames por fragmento
    num_nucleos = 2    # usar solo 2 núcleos

    start_time = time.time()
    frame_count = 0

    print("Procesando video en paralelo... Presiona 'q' para salir.")

    while True:
        frames = []
        for _ in range(chunk_size):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        if not frames:
            break

        # Procesar fragmento en paralelo
        with ProcessPoolExecutor(max_workers=num_nucleos) as executor:
            resultados = list(executor.map(convertir_frame, frames))

        # Guardar resultados
        for gray_frame in resultados:
            out.write(gray_frame)
            cv2.imshow('Video en Blanco y Negro', gray_frame)
            frame_count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n¡Video generado exitosamente!")
    print(f"Archivo guardado como: {output_video_path}")
    print(f"Fotogramas procesados: {frame_count}")
    print(f"Tiempo total: {total_time:.2f} segundos ({total_time / 60:.2f} minutos)")

if __name__ == "__main__":
    main()
