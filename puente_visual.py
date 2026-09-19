import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import pydirectinput
import time

print("Buscando la ventana de Euro Truck Simulator 2...")

try:
    lista_ventanas = gw.getWindowsWithTitle('Euro Truck Simulator 2')
    ventana = lista_ventanas.pop(0)
    print("¡Ventana de ETS2 detectada con éxito!")
except IndexError:
    print("ERROR: No se encontró el juego abierto. Abre ETS2 en modo ventana y vuelve a correr el script.")
    exit()

pydirectinput.PAUSE = 0.005

print("Presiona la tecla 'Q' dentro de la ventana de video para cerrar el script.")

# --- VARIABLES DE ESTADO ---
acelerando = False
frenando = False

# 2. Bucle de Conducción Progresiva Inteligente
while True:
    x, y, ancho, alto = ventana.left, ventana.top, ventana.width, ventana.height
    captura = pyautogui.screenshot(region=(x, y, ancho, alto))
    frame = cv2.cvtColor(np.array(captura), cv2.COLOR_RGB2BGR)
    
    # Visión de Enfoque Medio (Subimos un poco el techo al 60% para ver más lejos)
    alto_inicio = int(alto * 0.60)
    alto_fin = int(alto * 0.85)
    ancho_inicio = int(ancho * 0.28)
    ancho_fin = int(ancho * 0.72)
    
    asfalto = frame[alto_inicio:alto_fin, ancho_inicio:ancho_fin]
    gris = cv2.cvtColor(asfalto, cv2.COLOR_BGR2GRAY)
    
    # Filtro Adaptativo Numérico Nativo (Antibugs)
    binario = cv2.adaptiveThreshold(
        gris, 255, 1, 
        cv2.THRESH_BINARY_INV, 11, 2
    )
    
    alto_img, ancho_img = binario.shape
    centro_pantalla = ancho_img // 2
    
    # --- CREACIÓN DE LAS DOS ZONAS DE CONTROL FRONTALES ---
    # 1. CAJA CERCANA (Freno de Emergencia - Parte inferior del túnel)
    caja_cercana_ini = int(alto_img * 0.70)
    caja_ancho_ini = int(centro_pantalla - (ancho_img * 0.15))
    caja_ancho_fin = int(centro_pantalla + (ancho_img * 0.15))
    zona_cercana = binario[caja_cercana_ini:, caja_ancho_ini:caja_ancho_fin]
    
    # 2. CAJA LEJANA (Evasión Anticipada - Parte superior del túnel)
    caja_lejana_ini = int(alto_img * 0.35)
    caja_lejana_fin = int(alto_img * 0.70)
    zona_lejana = binario[caja_lejana_ini:caja_lejana_fin, caja_ancho_ini:caja_ancho_fin]
    
    # Medimos la densidad de asfalto en ambas zonas
    asfalto_cercano = (np.sum(zona_cercana == 255) / zona_cercana.size) * 100 if zona_cercana.size > 0 else 100
    asfalto_lejano = (np.sum(zona_lejana == 255) / zona_lejana.size) * 100 if zona_lejana.size > 0 else 100
    
    # Ojos Izquierdo y Derecho para la dirección normal
    ojo_izquierdo = binario[:, :centro_pantalla]
    ojo_derecho = binario[:, centro_pantalla:]
    asfalto_izq = np.sum(ojo_izquierdo == 255)
    asfalto_der = np.sum(ojo_derecho == 255)
    total_asfalto = asfalto_izq + asfalto_der
    
    # --- SISTEMA MOTOR DE REACCION GRADUAL ---
    
    # CRITERIO 1: PELIGRO INMINENTE (Objeto muy cerca) -> FRENO TOTAL + ESCAPE
    if asfalto_cercano < 45.0 or total_asfalto < 1500:
        if acelerando:
            pydirectinput.keyUp('w')
            acelerando = False
            
        print(f"🚨 FRENADO DE EMERGENCIA INMINENTE ({asfalto_cercano:.1f}% asfalto cerca) 🚨")
        pydirectinput.keyDown('s')
        time.sleep(1.2)
        pydirectinput.keyUp('s')
        
        # Maniobra de escape quieto
        if asfalto_izq > asfalto_der:
            pydirectinput.keyDown('a')
            time.sleep(1.0)
            pydirectinput.keyUp('a')
        else:
            pydirectinput.keyDown('d')
            time.sleep(1.0)
            pydirectinput.keyUp('d')
            
        # Impulso de salida
        pydirectinput.keyDown('w')
        time.sleep(1.5)
        pydirectinput.keyUp('w')
        
        # FIX CRÍTICO: Reseteamos las banderas para forzar la aceleración del modo normal
        acelerando = False
        frenando = False
        print("   ✅ Maniobra completada. Reiniciando aceleración autónoma...")
        
    # CRITERIO 2: OBSTÁCULO LEJANO -> EVASIÓN ANTICIPADA (Gira suave sin frenar)
    elif asfalto_lejano < 65.0:
        print(f"👀 Obstáculo detectado a lo lejos ({asfalto_lejano:.1f}% asfalto lejos). Esquivando...")
        # Desaceleramos un poco soltando la 'W' momentáneamente para tomar la curva con seguridad
        if acelerando:
            pydirectinput.keyUp('w')
            acelerando = False
            
        if asfalto_izq > asfalto_der:
            print("   ← Anticipación: Abriendo rumbo a la izquierda...")
            pydirectinput.press('a')
        else:
            print("   Anticipación: Abriendo rumbo a la derecha... →")
            pydirectinput.press('d')
            
    # CRITERIO 3: RUTA COMPLETAMENTE LIMPIA -> CRUCERO A FONDO
    else:
        if frenando:
            pydirectinput.keyUp('s')
            frenando = False
            
        if not acelerando:
            pydirectinput.keyDown('w')
            acelerando = True
            print("▲ AUTOPISTA TOTALMENTE LIBRE - Crucero autónomo a fondo ▲")
            
        # Dirección reactiva normal de carril
        diferencia = asfalto_izq - asfalto_der
        tolerancia_bordes = 150 # Se sube un poco la tolerancia para que no sea tan nervioso en rectas
        
        if diferencia > tolerancia_bordes:
            print(f"   ← Alineando Izquierda | Dif: {diferencia}")
            pydirectinput.press('a')
        elif diferencia < -tolerancia_bordes:
            print(f"   Alineando Derecha → | Dif: {diferencia}")
            pydirectinput.press('d')
        else:
            print("   • Centrado perfecto •")

    # Se dibujan las dos cajas en pantalla (Gris claro para lejana, Gris oscuro para cercana)
    cv2.rectangle(binario, (caja_ancho_ini, caja_lejana_ini), (caja_ancho_fin, caja_lejana_fin), 100, 2)
    cv2.rectangle(binario, (caja_ancho_ini, caja_cercana_ini), (caja_ancho_fin, alto_img), 180, 2)
    cv2.line(binario, (centro_pantalla, 0), (centro_pantalla, alto_img), 125, 2)
    cv2.imshow('Ojos de la Mosca - Modo Pavimento Seguro', binario)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pydirectinput.keyUp('w')
pydirectinput.keyUp('s')
cv2.destroyAllWindows()
print("Script cerrado correctamente.")
