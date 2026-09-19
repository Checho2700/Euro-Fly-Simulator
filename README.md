================================================================================
  Euro Fly Simulator v1.0 - ETS2 + Fruit Fly Connectome Bridge
================================================================================

¡Bienvenido al primer piloto automático bio-inspirado para Euro Truck Simulator 2! 
Este proyecto crea un puente de visión artificial en Python que simula los 
reflejos reactivos y los circuitos visuales del conectoma de la mosca de la 
fruta para conducir camiones de forma autónoma.


--------------------------------------------------------------------------------
 [!] CARACTERÍSTICAS ACTUALES
--------------------------------------------------------------------------------

 * Modo Pavimento Seguro
   Segmentación adaptativa en tiempo real con OpenCV que procesa el asfalto 
   como zona segura y las barreras como obstáculos.

 * Lazo de Control Motor
   Inyección directa de inputs de teclado mediante pydirectinput sin latencia 
   en motores DirectX.

 * Reflejo de Escape Avanzado
   Sistema de seguridad que detecta colisiones inminentes, frena a fondo y 
   ejecuta maniobras de evasión automáticas basándose en la densidad de 
   píxeles.


--------------------------------------------------------------------------------
 [>] REQUISITOS E INSTALACIÓN
--------------------------------------------------------------------------------

 1. Instalar las dependencias de automatización y visión artificial ejecutando 
    en tu consola:

    pip install opencv-python numpy pyautogui pygetwindow pydirectinput

 2. Abrir Euro Truck Simulator 2 en modo ventana, resolución 1280x720 y 
    gráficos mínimos para optimizar FPS.

 3. Alinear el camión en un carril y ejecutar el puente visual en el CMD:

    python puente_visual.py


--------------------------------------------------------------------------------
 [*] PRÓXIMOS PASOS EN EL ROADMAP - ¡ÚNETE A LA COMUNIDAD!
--------------------------------------------------------------------------------

 [ ] Integración de Estimación de Profundidad 3D monocular mediante modelos 
     de IA como MiDaS de Intel Labs.

 [ ] Conexión de los impulsos del script directo a la arquitectura de red 
     neuronal estática de OpenFly MaleCNS v1.0.


================================================================================
 Desarrollado en estado de flow absoluto. 
 ¡Siéntete libre de clonar, abrir un Issue o mandar tu Pull Request para 
 mejorar los reflejos de la mosca!
================================================================================