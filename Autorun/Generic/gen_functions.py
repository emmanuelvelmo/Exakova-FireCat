import pyautogui
import numpy
import cv2
import pytesseract
import time
import datetime
import os
import re

# Escribir mensaje
def gen_escribir_msg(val_msg, val_tiempo):
    # Reemplazar caracteres acentuados por sus equivalentes no acentuados
    ch_reemp = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','ñ':'n','Ñ':'N'}
    
    for ch_it, val_it in ch_reemp.items():
        val_msg = val_msg.replace(ch_it, val_it)
    
    pyautogui.typewrite(val_msg)
    pyautogui.press('enter')
    time.sleep(val_tiempo)

# Eliminar espacios y líneas en blanco en un texto
def gen_del_lin(tmp_txt):
    # Limpiar espacios en blanco
    tmp_txt = tmp_txt.strip()
    
    # Retornar texto sin saltos de línea
    return re.sub(r'\n\s*\n', '\n', tmp_txt).strip()

# Reemplazar saltos de línea por espacios
def gen_reemp_salt(tmp_txt):
    return re.sub(r'\s+', ' ', tmp_txt).strip()

# Buscar en txt y asignar valor a variable
def gen_busq_txt(ruta_txt, pos_linea):
    # Verifica si el archivo txt existe en su directorio
    if os.path.isfile(ruta_txt):
        # Leer el contenido del archivo
        with open(ruta_txt, 'r') as ref_txt:
            # Contador de líneas
            cont_linea = 0
            
            # Iterar cada línea del archivo
            for linea_tmp in ref_txt:
                # Moverse hasta la línea
                if cont_linea == pos_linea and linea_tmp != '':
                    # Limpiar espacios en blanco y retornar
                    return linea_tmp.strip()
                    
                cont_linea += 1

# Actualizar línea en txt
def gen_act_txt(ruta_txt, pos_linea, tmp_palabra):
    # Verifica si el archivo txt existe en su directorio
    if os.path.isfile(ruta_txt):
        # Leer el contenido del archivo
        with open(ruta_txt, 'r') as ref_txt:
            tmp_lineas = ref_txt.readlines()

        # Actualizar la línea en la posición deseada
        tmp_lineas[pos_linea] = str(tmp_palabra) + '\n'

        # Escribir el contenido actualizado en el archivo
        with open(ruta_txt, 'w') as ref_txt:
            ref_txt.writelines(tmp_lineas)

# Diferencia de horas entre fecha actual y previa
def gen_dif_hr(fecha_tmp):
    # Obtener la fecha y hora actual
    fecha_act = datetime.datetime.now()
    
    # Convertir fecha previa de string a datetime
    fecha_prev = datetime.datetime.strptime(fecha_tmp, "%Y-%m-%d-%H:%M:%S")
    
    # Calcular diferencia entre fechas en horas
    dif_hr = (fecha_act - fecha_prev).total_seconds() / 3600
    
    return dif_hr

# Actualizar fecha actual en archivo cada 36 horas o más
def gen_act_fecha(ruta_txt, pos_linea):
    gen_act_txt(ruta_txt, pos_linea, datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

# Convertir imagen a escala de grises
def gen_escala_grises(tmp_img):
    # Convertir la imagen a un array de numpy
    arr_numpy = numpy.array(tmp_img)

    # Convertir la imagen de RGB a BGR
    img_bgr = cv2.cvtColor(arr_numpy, cv2.COLOR_RGB2BGR)

    # Convertir la imagen a escala de grises y retornar
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Capturar pantalla y convertir a escala de grises
def gen_capt_pant():
    # Capturar la pantalla
    tmp_screenshot = pyautogui.screenshot()
    
    # Convertir a escala de grises y retornar
    return gen_escala_grises(tmp_screenshot)

# Capturar un área específica de la pantalla y convertir a escala de grises
def gen_capt_spec_pant(vis_box):
    # Captura una región específica de la pantalla
    tmp_screenshot = pyautogui.screenshot(region=(vis_box[0], vis_box[1], vis_box[2], vis_box[3]))
    
    # Convertir a escala de grises y retornar
    return gen_escala_grises(tmp_screenshot)

# Actualizar ratio entre seguidos y seguidores
def gen_act_ratio(val_seguidos, val_seguidores):
    # Evitar error de división entre cero
    if val_seguidores == 0: val_seguidores = 1
    
    return val_seguidos / val_seguidores

# Obtener texto de una imagen
def gen_text_img(tmp_img):
    # Usa pytesseract para extraer el texto de la imagen
    val_text = pytesseract.image_to_string(tmp_img)
    
    # Limpiar espacios en blanco y retornar
    return val_text.strip()

# Obtener texto de un área específica de la pantalla
def gen_(vis_box):
    # Capturar un área específica de la pantalla
    tmp_img = gen_capt_spec_pant(vis_box)
    
    # Retornar texto de la imagen sin espacios
    return gen_text_img(tmp_img)

# Corregir saltos de línea en texto
def gen_corr_lin(tmp_img):
    # Obtener texto de la imagen
    tmp_txt = gen_text_img(tmp_img)

    # Eliminar líneas en blanco
    tmp_txt = re.sub(r'\n\s*\n', '\n', tmp_txt).strip()

    # El texto contiene dos o más líneas
    if len(tmp_txt.splitlines()) >= 2:
        # Dividir texto en líneas
        tmp_txt = tmp_txt.split('\n')
        
        # Separar cifras y palabras
        nmb_tmp = tmp_txt[0].split()
        pal_tmp = tmp_txt[1].split()

        # Retornar cifras y palabras combinadas en una línea
        return ' '.join(f"{num_v} {pal_v}" for num_v, pal_v in zip(nmb_tmp, pal_tmp))

# Obtener cifra anterior a una palabra en un texto
def gen_cifra_palabra(tmp_txt, tmp_palabra):
    # Reemplazar guiones y guiones bajos por puntos (correción de errores de OCR)
    tmp_txt = tmp_txt.replace('-', '.').replace('_', '.')
    
    # La expresión regular busca una cifra con o sin decimales seguida de opcionalmente un sufijo (K, k, M, m)
    tmp_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:([KkMm])\s*)?' + re.escape(tmp_palabra), tmp_txt)
    
    # Se encuentra una cifra seguida de la palabra en el texto
    if tmp_match:
        # Extraer la cifra encontrada
        tmp_cifra = tmp_match.group(1)
        
        # Extraer el sufijo encontrado (si existe)
        suf_val = tmp_match.group(2) if tmp_match.group(2) else ''
        
        # Convertir la cifra a float para manejar decimales correctamente
        cifra_val = float(tmp_cifra)
        
        # Procesar la cifra con su sufijo
        if suf_val in {'K', 'k'}:
            # Multiplicar por mil
            return int(cifra_val * 1000)
        elif suf_val in {'M', 'm'}:
            # Multiplicar por un millón
            return int(cifra_val * 1000000)
        else:
            # No hay sufijo, devolver la cifra como entero
            return int(cifra_val)
    # No se encuentra la palabra o la cifra
    else:
        return 0

# Obtener una cifra a partir de imagen y una palabra
def gen_cifra(tmp_img, tmp_palabra):
    # Obtener texto de la imagen sin espacios
    tmp_txt = gen_text_img(tmp_img)
    
    # Obtener número desde el texto y retornar
    return gen_cifra_palabra(tmp_txt, tmp_palabra)

# Coordenadas del elemento a encontrar
gen_centro_xy = [0, 0]

# Cambiar coordenadas de la variable génerica de coordenadas
def gen_camb_coords(tmp_coords):
    global gen_centro_xy
    
    gen_centro_xy[0] = tmp_coords[0]
    gen_centro_xy[1] = tmp_coords[1]

# Colocar cursor sobre una posición específica
def gen_cur_spec():
    pyautogui.moveTo(gen_centro_xy[0], gen_centro_xy[1])
    time.sleep(2)

# Hacer click sobre una posición específica
def gen_click_spec(val_tiempo):
    pyautogui.moveTo(gen_centro_xy[0], gen_centro_xy[1])
    
    pyautogui.click()
    time.sleep(val_tiempo)

# Hacer click sobre una posición específica y abrir en otra pestaña
def gen_ab_click_spec(val_tiempo):
    pyautogui.moveTo(gen_centro_xy[0], gen_centro_xy[1])
    
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    time.sleep(0.1)
    pyautogui.click()
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    time.sleep(val_tiempo)

# Calcular centro de un campo de captura
def gen_calc_cent(vis_box):
    global gen_centro_xy
    
    # Asinar puntos medios del rectángulo
    gen_centro_xy[0] = round(vis_box[0] + (vis_box[2] / 2))
    gen_centro_xy[1] = round(vis_box[1] + (vis_box[3] / 2))

# Calcular centro de un campo de captura y retornar coordenadas
def gen_calc_cent_rtn(vis_box):
    # Variable a retornar
    tmp_xy = [0,0]
    
    # Asinar puntos medios del rectángulo
    tmp_xy[0] = round(vis_box[0] + (vis_box[2] / 2))
    tmp_xy[1] = round(vis_box[1] + (vis_box[3] / 2))
    
    return tmp_xy

# Conservar segunda línea con texto de una captura de texto
def gen_2l_text(tmp_txt):
    # El texto por lo menos tiene 2 líneas
    if len(tmp_txt.splitlines()) >= 2:
        seg_lin = tmp_txt.splitlines()[1]
        
        # Eliminar espacios en blanco para la línea conservada
        seg_lin_limp = seg_lin.strip()
        
        return seg_lin_limp
    else:
        return ''

# Conservar primera línea con texto de una captura de texto
def gen_limp_text(tmp_txt):
    # Eliminar líneas en blanco
    lins_text = [lin_it.strip() for lin_it in tmp_txt.splitlines() if lin_it.strip()]
    
    # Eliminar todas las líneas excepto la primera
    if lins_text:
        prim_lin = lins_text[0]
    else:
        prim_lin = ''
    
    # Eliminar espacios en blanco para la línea conservada
    prim_lin_limp = prim_lin.strip()
    
    return prim_lin_limp

# Líneas de referencia de usuario
gen_usr_ref = ''
gen_2l_ref = ''

# Actualizar líneas de referencia de usuario
def gen_usr_lins(tmp_img):
    global gen_usr_ref, gen_2l_ref
    
    # Obtener texto de la imagen sin espacios
    tmp_txt = gen_text_img(tmp_img)
    
    # Obtener primera línea del texto
    gen_usr_ref = gen_limp_text(tmp_txt)
    
    # Obtener segunda línea del texto
    gen_2l_ref = gen_2l_text(tmp_txt)

# Asignar nombre del primer usuario en lista y asignar coordenadas
def gen_prim_usr(vis_box):
    # Capturar un área específica de la pantalla
    tmp_img = gen_capt_spec_pant(vis_box)
    
    # Actualizar usuario de referencia y segunda línea si la hay
    gen_usr_lins(tmp_img)
    
    # Calcular coordenas para el usuario de referencia
    gen_calc_pos_text(tmp_img, gen_usr_ref)
    
    # Corregir coordenadas
    gen_aj_coords(vis_box)

# Desplazar hacia el siguiente usuario
def gen_desp_usr(vis_box):
    while True:
        # Capturar un área específica de la pantalla
        tmp_img = gen_capt_spec_pant(vis_box)
        
        # Obtener texto de la imagen sin espacios
        tmp_txt = gen_text_img(tmp_img)
        
        # Obtener nombre de usuario (primera línea en campo de captura)
        tmp_usr = gen_limp_text(tmp_txt)
        
        # Desplazar si el nombre del usuario o la segunda línea están presentes
        if tmp_usr == gen_usr_ref or tmp_usr == gen_2l_ref:
            # Desplazar hacia abajo
            pyautogui.mouseDown(button='middle')
            pyautogui.moveRel(0, 20)
            time.sleep(0.3)
            pyautogui.mouseUp(button='middle')
            pyautogui.moveRel(0, -20)
        else:
            # Dejar de desplazar hacia abajo
            break

# Asignar coordenadas del centro de un objeto en pantalla
def gen_coinc_imgs(vis_box, ref_img_dir):
    global gen_centro_xy
    
    # Capturar un área específica de la pantalla
    base_img = gen_capt_spec_pant(vis_box)
    
    # Cargar imagen de referencia
    ref_img = cv2.imread(ref_img_dir, cv2.IMREAD_GRAYSCALE)
    
    # Encontrar valores de coincidencia y el vértice X1,Y1
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cv2.matchTemplate(base_img, ref_img, cv2.TM_CCOEFF_NORMED))
    
    # Obtener las dimensiones del template (imagen de referencia)
    ancho_val, alto_val = ref_img.shape[::-1]
    
    # Asignar coordenadas del centro del objeto
    gen_centro_xy[0] = round(vis_box[0] + (max_loc[0] + (ancho_val / 2)))
    gen_centro_xy[1] = round(vis_box[1] + (max_loc[1] + (alto_val / 2)))

# Asignar coordenadas de un texto en pantalla
def gen_calc_pos_text(tmp_img, text_ref):
    global gen_centro_xy
    
    # Realizar OCR y obtener textos
    texts_img = pytesseract.image_to_data(tmp_img, output_type=pytesseract.Output.DICT)
    
    # Obtener el número total de elementos tipo texto
    num_texts = len(texts_img['text'])
    
    # Iterar y comparar cada una de las palabras de la imagen
    for iter_elem in range(num_texts):
        if int(texts_img['conf'][iter_elem]) > 0:
            tmp_txt = texts_img['text'][iter_elem].strip()
            
            if any(tmp_txt in eval_ch for eval_ch in text_ref.split()):
                # Obtener las coordenadas X1,Y1, X4,Y4 del bloque de texto
                x1 = texts_img['left'][iter_elem]
                y1 = texts_img['top'][iter_elem]
                x4 = x1 + texts_img['width'][iter_elem]
                y4 = y1 + texts_img['height'][iter_elem]
                
                # Calcular coordenada central del objeto
                gen_centro_xy[0] = round((x1 + x4) / 2)
                gen_centro_xy[1] = round((y1 + y4) / 2)
                
                break

# Ajustar coordenadas
def gen_aj_coords(vis_box):
    global gen_centro_xy
    
    # Sumar a X,Y en gen_centro_xy X1,Y1 en campo de captura de imagen
    gen_centro_xy[0] += vis_box[0]
    gen_centro_xy[1] += vis_box[1]

gen_camb_bl = False

# Cambiar el valor del bool
def gen_f_camb_bl(val_bl):
    global gen_camb_bl
    
    gen_camb_bl = val_bl

# Evaluar cambio en el entorno
def gen_camb_entn(capt_1, capt_2):
    global gen_camb_bl
    
    if cv2.norm(capt_1, capt_2, cv2.NORM_L2) > 50000:
        gen_camb_bl = True
    else:
        gen_camb_bl = False

# Encontrar posición de un elemento visual
def gen_calc_pos_vis(capt_pant, nom_ref_img):
    # Cargar imagen de referencia
    with open('Autorun/TikTok/Refs/' + nom_ref_img, 'rb') as tmp_arch:
        tmp_img = tmp_arch.read()
    
    # Convertir imagen de referencia a escala de grises
    ref_img = gen_escala_grises(tmp_img)
    
    # Comparar imágenes y asignar coordenadas
    coords_fig = gen_coinc_imgs(capt_pant, ref_img)
    
    # Actualizar coordenadas del objeto encontrado
    gen_calc_cent(coords_fig)
