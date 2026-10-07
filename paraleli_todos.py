import time
import cv2
import numpy as np
import os
from concurrent.futures import ProcessPoolExecutor

# Función top-level para procesar cada frame
def convertir_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def main():
    input_video_path = 'vib.webm'
    output_video_path = 'video_todos.mp4'

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print("Error al abrir el video de entrada.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=False)

    # Forzamos exactamente 8 núcleos
    num_nucleos = 8  

    chunk_size = 100
    start_time = time.time()
    frame_count = 0

    print(f"Procesando video en paralelo con {num_nucleos} núcleos... Presiona 'q' para salir.")

    # Mantenemos el pool abierto para reutilizar los 8 procesos sin la sobrecarga de crearlos en cada ciclo
    with ProcessPoolExecutor(max_workers=num_nucleos) as executor:
        stop_processing = False

        while True:
            frames = []
            for _ in range(chunk_size):
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)

            if not frames:
                break

            # Mapeo en paralelo sobre los 8 trabajadores
            resultados = list(executor.map(convertir_frame, frames))

            for gray_frame in resultados:
                out.write(gray_frame)
                cv2.imshow('Video en Blanco y Negro', gray_frame)
                frame_count += 1
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop_processing = True
                    break

            if stop_processing:
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
