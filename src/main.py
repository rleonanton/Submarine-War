import pygame, sys, random
from config import*
from menu import *
from archivos import *


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Submarine War")
wallpaper = pygame.transform.scale(pygame.image.load("src\images\wallpaper.jpg"), (width, height))

#carga de imagenes y rectangulo de imagenes
coin_images = [pygame.transform.scale(pygame.image.load(f"src\images\coins\coin{i}.png"), (width_rect_coin, height_rect_coin)) for i in range(6)]

submarine_image = pygame.image.load("src\images\player_1.png")
submarine_image = pygame.transform.scale(submarine_image, (width_rect_submarine, height_rect_submarine))
submarine_mask = pygame.mask.from_surface(submarine_image)
submarine_rect = submarine_image.get_rect()

#sonidos del juego
#sonido principal
background_music = pygame.mixer.music.load("src\sounds\Metal Gear Solid Soundtrack.mp3")
pygame.mixer.music.play(-1)

#sonido de las balas del destroyer y del submarino
shot_bullets_sounds = pygame.mixer.Sound("src\sounds\destroyer_bullet.mp3")

#sonido al colectar un coin
collect_coin_sound = pygame.mixer.Sound("src\sounds\coins.mp3")

#sonido game over
game_over_sounds = pygame.mixer.Sound("src\sounds\mgs_game_over_sound.mp3")

#lista para almacenar la minas submarinas
naval_mine_list = []

# funcion para crear minas submarinas
def create_naval_mine(lista, qty_mines, image_path, widt_mine, height_mine, width):
    """
    Funcion que crea minas navales y las agrega a una lista.

    Args:
        lista (list): Lista para almacenar las minas navales.
        qty_mines (int): Cantidad de minas a crear.
        image_path (str): Ruta de la imagen de la mina naval.
        width_mine (int): Ancho de la mina naval.
        height_mine (int): Alto de la mina naval.
        width (int): Ancho de la pantalla.

    Returns:
        list: Lista actualizada con las minas navales.
    """
    for _ in range(qty_mines):
        image = pygame.transform.scale(pygame.image.load(image_path), (widt_mine, height_mine))
        rect = image.get_rect()
        rect.x = random.randrange( 10 * widt_mine, width - width_mine)
        rect.y = random.randrange (int(height * 0.40), height - height_mine)
        lista.append({"image": image, "rect": rect})
    return lista

create_naval_mine(naval_mine_list, qty_mines, "src\images\mina_submarina.png", width_mine, height_mine, width)

def load_naval_mine(screen, lista):
    """
    Función para cargar y renderizar las minas navales en la pantalla.

    Args:
        screen: La superficie de la pantalla en la que se renderizarán las minas navales.
        lista (list): La lista que contiene las minas navales a cargar y renderizar.

    Returns:
        None
    """
    for naval_mine in lista:
        screen.blit(naval_mine["image"], naval_mine["rect"])

#lista para almacenar el destroyer
destroyer_list = []

#funcion para crear el detroyer
def create_destroyer(lista):
    """
    Funcion para crear un destructor y lo agrega a una lista.

    Args:
        lista (list): Lista para almacenar los destructores.

    Returns:
        list: Lista actualizada con el destructor.
    """
    destroyer_image = pygame.image.load("src\images\destructor.png")
    destroyer_image = pygame.transform.scale(destroyer_image, (width_rect_enemies, height_rect_enemies))
    destroyer_rect = destroyer_image.get_rect()
    destroyer_rect.topleft = (width + pos_x_ship_enemies, pos_y_ship_enemies)
    lista.append({"image" : destroyer_image, "rect" : destroyer_rect})
    return lista

# funcion para actualizar el destroyer
def update_destroyer(destroyer_rect, ship_enemy_speed):
    """
    Funcion que actualiza la posición del destructor.

    Args:
        destroyer_rect (pygame.Rect): Rectángulo del destructor.
        ship_enemy_speed (int): Velocidad del destructor.

    """
    destroyer_rect.x += ship_enemy_speed  # Actualiza la posición en el eje x usando la velocidad en el eje x
    if destroyer_rect.right == 0:
        destroyer_rect.left = width

destroyer = create_destroyer(destroyer_list)

#lista para almacenar los diccionarios de enemigos
enemies_images = []

#lista de imagenes de los enemigos
enemies_list = ["src\images\enemigo1.png", "src\images\enemigo2.png", "src\images\enemigo3.png"]

#funcion para crear enemigos
def create_enemies(lista):
    """
    Funcion que crea enemigos y devuelve un diccionario con su información.

    Args:
        lista (list): Lista de imágenes de enemigos.

    Returns:
        dict: Diccionario con la información del enemigo.

    """
    image_path = random.choice(lista)
    image = pygame.transform.scale(pygame.image.load(image_path), (width_rect_enemies, height_rect_enemies))
    rect = image.get_rect()
    rect.x = width + width_rect_enemies
    rect.y = random.randrange(int(height * 0.30), height - height_rect_enemies)
    speed_x = random.randrange(-8, -1)
    return {"image" : image, "rect": rect, "speed_x": speed_x}  

#funcion para actualizar enemigos
def update_enemies(enemies):
    """Funcion que actualiza la posición del enemigo.

    Args:
        enemies (dict): Diccionario con la información del enemigo.
    """
    enemies["rect"].x += enemies["speed_x"]  # Actualiza la posición en el eje x usando la velocidad en el eje x
    if enemies["rect"].right <= 0:
        enemies["rect"].left = width

# configuro fuente del contador de monedas
font = pygame.font.Font(None, 36) # fuente del texto

#funcion para la barra de vida
def draw_live_bar(surface, x, y, percentage):
    """Funcion para dibujar la barra de vida en pantalla

    Args:
        surface (pygame.Surface): Superficie en la que se dibuja la barra.
        x (int): Coordenada x de la barra.
        y (int): Coordenada y de la barra.
        percentage (float): Porcentaje de la barra llena.
    """
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

# lista para almacenar los coins
coins = []

#funcion para crear coins
def create_coins(lista, qty_coins, width, width_rect_coin, height, height_rect_coin):
    """Funcion para crear monedas y las agrega a una lista.

    Args:
        lista (list): Lista para almacenar las monedas.
        qty_coins (int): Cantidad de monedas a crear.
        width (int): Ancho de la pantalla.
        width_rect_coin (int): Ancho del rectángulo de la moneda.
        height (int): Alto de la pantalla.
        height_rect_coin (int): Alto del rectángulo de la moneda.

    Returns:
        list: Lista actualizada con las monedas.
    """
    for _ in range(qty_coins):
        x = random.randrange(width - width_rect_coin)
        y = random.randint(int(height * 0.40), height - height_rect_coin)
        coin_rect = pygame.Rect(x, y, width_rect_coin, height_rect_coin)
        coin_dict = {
            "x": x,
            "y": y,
            "rect": coin_rect,
            'index': 0
        }
        lista.append(coin_dict)
    return lista

#funcion para cargar la lista de coins
def load_coins(lista, cantidad):
    """Funcion que carga la lista de coins

    Args:
        lista (list): Lista para almacenar las monedas.
        cantidad (int): Cantidad de monedas a cargar.

    Example:
        load_coins(coins, cantidad)
    """
    for i in range(cantidad):
        lista.append(coin_images) 

coins = create_coins(coins, qty_coins, width, width_rect_coin, height, height_rect_coin)

#lista de almacenado de balas frontales
front_bullets = []

# funcion para crear balas frontales
def create_front_bullet(mid_bottom, speed = 5):
    """Crea las balas frontales del submarino.

    Args:
        mid_bottom (tuple): Coordenadas del punto medio inferior de la bala.
        speed (int): Velocidad de la bala.

    Returns:
        dict: Diccionario con la información de la bala frontal.

    Example:
        create_front_bullet(mid_bottom, speed)
    """
    front_bullet_image = pygame.transform.scale(pygame.image.load("src/images/orpedo.png"), (width_front_bullet, height_front_bullet))
    front_bullet_rect = pygame.Rect(mid_bottom[0] - 3 ,mid_bottom[1] - 20, width_front_bullet, height_front_bullet)
    return {"image" : front_bullet_image, "rect" : front_bullet_rect, "speed" : speed}

#lista para almacenar balas superiores
top_bullets = []

#funcion para crear balas superiores
def create_top_bullet(mid_top, speed = 5):
    """
    Crea las balas superiores del submarino.

    Args:
        mid_top (tuple): Coordenadas del punto medio superior de la bala.
        speed (int): Velocidad de la bala.

    Returns:
        dict: Diccionario con la información de la bala superior.

    Example:
        create_top_bullet(mid_top, speed)
    """
    top_bullet_image = pygame.transform.scale(pygame.image.load("src/images/up_bullet.png"), (width_top_bullet, height_top_bullet))
    top_bullet_rect = pygame.Rect(mid_top[0] - 3 ,mid_top[1] - 8, width_top_bullet, height_top_bullet)
    return {"image" : top_bullet_image, "rect" : top_bullet_rect, "speed" : speed}

#lista para almacenar las balas del destroyer
destroyer_bullets = []

#funcion para crear las balas del destroyer
def create_destroyer_bullet(mid_bottom, speed = 5):
    """
    Crea balas del destructor.

    Args:
        mid_bottom (tuple): Coordenadas del punto medio inferior de la bala.
        speed (int): Velocidad de la bala.

    Returns:
        dict: Diccionario con la información de la bala del destructor.

    Example:
        create_destroyer_bullet(mid_bottom, speed)
    """
    destroyer_bullet_image = pygame.transform.scale(pygame.image.load("src\images\misil_enemigo.png"), (width_detroyer_bullet, height_destroyer_bullet))
    destroyer_bullet_rect = pygame.Rect(mid_bottom[0], mid_bottom[1], width_detroyer_bullet, height_destroyer_bullet)
    return{"image" : destroyer_bullet_image, "rect" : destroyer_bullet_rect, "speed" : speed }

#lista para almacenar la explosion
explotion_list = []

#funcion para crear una explosion 
def create_explosion_list(lista, x, y, width_rect_explotion, height_rect_explotion, num_frames_explotion):
    """
    Funcion que crea una lista de imágenes de una explosión.

    Args:
        lista (list): Lista para almacenar las imágenes de explosión.
        x (int): Coordenada x de la explosión.
        y (int): Coordenada y de la explosión.
        width_rect_explotion (int): Ancho del rectángulo de explosión.
        height_rect_explotion (int): Alto del rectángulo de explosión.
        num_frames_explotion (int): Número de frames de explosión.

    Returns:
        list: Lista actualizada con las imágenes de explosión.

    Example:
        create_explosion_list(explotion_list, x, y, width_rect_explotion, height_rect_explotion, num_frames_explotion)
    """
    explosion_frames = [pygame.transform.scale(pygame.image.load(f"src\images\explosion\explosion0{i}.png"), (width_rect_explotion, height_rect_explotion)) for i in range(num_frames_explotion)]
    for frame in explosion_frames:
        explosion_rect = frame.get_rect()
        explosion_rect.center = (x, y)  # Posición del centro de la explosión
        explosion_dict = {
            "image": frame,
            "rect": explosion_rect,
            'index': 0
        }
        lista.append(explosion_dict)
    return lista

# funcion para salir del juegpo
def finish():
    """
    Funcion para finalizar el juego y cierra la ventana.

    Example:
        finish()
    """
    pygame.quit()
    pygame.mixer.quit()
    sys.exit() 

# funcion para pausar o salir del programa o para volver al programa por cualquier tecla
def wait_user():
    """
    Funcion que pausa el juego y espera a que el usuario interactúe con el juego.

    Example:
        wait_user()
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finish()
                return
            
def restart_game():
    global submarine_rect, qty_mines, naval_mine_list, qty_coins, submarine_shield, score, move_up, move_down, move_left,\
        move_right, front_bullet_count, top_bullet_count, front_bullets, top_bullets, destroyer_list, destroyer_bullets, \
        enemies_images, time_last_shot, submarine_speed, time_last_shot, destroyer_hit, new_destroyer_delay, time_last_destroyer_hit, run, game_is_over

    # Restablecer las variables del juego
    submarine_rect = pygame.Rect(width // 2 - width_rect_submarine // 2, height - height_rect_submarine - 10, width_rect_submarine, height_rect_submarine)
    destroyer_image = pygame.image.load("src\images\destructor.png")
    destroyer_image = pygame.transform.scale(destroyer_image, (width_rect_enemies, height_rect_enemies))
    destroyer_rect = destroyer_image.get_rect()
    submarine_shield = 100
    score = 0
    qty_coins = 2
    qty_mines = 15
    move_up = False
    move_down = False
    move_left = False
    move_right = False
    front_bullet_count = 0
    top_bullet_count = 0
    time_last_shot = 0
    submarine_speed = 10  
    time_last_shot = 0
    destroyer_hit = False
    new_destroyer_delay = 3000
    time_last_destroyer_hit = 0
    game_is_over = False
    run = True
    naval_mine_list.clear()  # Reinicia la lista a una lista vacía
    create_naval_mine(naval_mine_list, qty_mines, "src\images\mina_submarina.png", width_mine, height_mine, width)
    update_destroyer(destroyer_rect, ship_enemy_speed)
    update_enemies(enemies)

    pygame.mixer.music.load("src\sounds\Metal Gear Solid Soundtrack.mp3")
    pygame.mixer.music.play(-1)  # Reproducir la música de fondo en bucle

def draw_game_over_screen():
    """
    Funcion para dibuja la pantalla de fin de juego.

    Example:
        draw_game_over_screen()
    """
    run = False
    pygame.mixer.music.pause()
    game_over_sounds.play(0)
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 60)
    title = font.render("Game Over", True, MAGENTA)
    restart_indications = font.render("Presiona cualquier tecla para reiniciar o escape para salir del juego", True, CYAN)
    screen.blit(title, (width // 2 - 150, height // 2 - title.get_height()))
    screen.blit(restart_indications, (width // 2 - restart_indications.get_width() // 2, height // 2 + restart_indications.get_height()))
    pygame.display.update()
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finish()
                else:
                    game_over = False
                    restart_game()
                return

#funcion para mostrar texto en pantalla
def show_text(screen, text, font_size, coordinates, font_color):
    """
    Funcion para mostrar cualquier texto en pantalla.

    Args:
        screen (pygame.Surface): Superficie en la que se muestra el texto.
        text (str): Texto a mostrar.
        font_size (int): Tamaño de fuente.
        coordinates (tuple): Coordenadas donde se muestra el texto.
        font_color (tuple): Color de fuente.

    Example:
        show_text(screen, text, font_size, coordinates, font_color)
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, font_color)
    rect_text = text_surface.get_rect()
    rect_text.center = coordinates
    screen.blit(text_surface, rect_text)
    pygame.display.flip()

   
#Bucle principal

while run_menu:
    menu_option = main_menu(window)
    if menu_option == "INICIAR JUEGO":
        run_menu = False
        run = True
        while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    # eventos para mover el submarino al presionar una tecla
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            move_up = True
                            move_down = False
                        
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            move_down = True
                            move_up = False
                        
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            move_right = True
                            move_left = False
                        
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            move_left = True
                            move_right = False
                        
                        #comando para pausar la musica de fondo del juego
                        if event.key == pygame.K_m:
                            if playing_music:
                                pygame.mixer.music.pause()
                            else:
                                pygame.mixer.music.unpause()
                            playing_music = not playing_music
                        
                        #comando para paudar el juego
                        if event.key == pygame.K_p:
                            if playing_music:
                                pygame.mixer.music.pause()
                            show_text(screen, "PAUSE", 120, center_screen, NAVY)
                            wait_user()
                            if playing_music:
                                pygame.mixer.music.unpause()
                    
                    # eventos que detienen el movimiento del subamrino al soltar la tecla presionada
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            move_up = False
                        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            move_down = False
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            move_right = False
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            move_left = False

                    # eventos que manejan los disparos del submarino, la tecla derecha dispara misiles verticales y la izquierda los misiles horizontales 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_presses = pygame.mouse.get_pressed()
                        if mouse_presses[0]:
                            if front_bullet_count <= max_front_bullets_count:
                                shot_bullets_sounds.play()
                                shot_bullets_sounds.set_volume(0.5)
                                front_bullet = create_front_bullet(submarine_rect.bottomright, speed_bullet)
                                front_bullets.append(front_bullet)
                                front_bullet_count += 1
                        if mouse_presses[2]:  # Verifica el botón derecho del mouse
                            if top_bullet_count <= max_top_bullets_count:
                                shot_bullets_sounds.play()
                                shot_bullets_sounds.set_volume(0.5)
                                top_bullet = create_top_bullet((submarine_rect.centerx, submarine_rect.top), speed_top_bullet)
                                top_bullets.append(top_bullet)
                                top_bullet_count += 1

                # Actualizar el temporizador con el tiempo transcurrido
                time_last_shot += clock.get_time() / 1000  # Tiempo en segundos

                # Actualización de la posición del objeto
                if move_up:
                    submarine_rect.y -= submarine_speed
                if move_down:
                    submarine_rect.y += submarine_speed
                if move_left:
                    submarine_rect.x -= submarine_speed
                if move_right:
                    submarine_rect.x += submarine_speed

                #----compruebo que el submarino no salga de pantalla
                if submarine_rect.right >= width:
                    submarine_rect.right = width
                if submarine_rect.top <= height * 0.30:
                    submarine_rect.top = height * 0.30
                if submarine_rect.bottom >= height:
                    submarine_rect.bottom = height
                if submarine_rect.left <= 0:
                    submarine_rect.left = 0

                if submarine_shield == 0:
                    update_high_scores(score)  
                    draw_game_over_screen()
                    main_menu(screen)

                ###----------ZONA DE DIBUJO

                # Dibuja la pantalla
                screen.blit(wallpaper, (pos_x_window, pos_y_window)) #funcion para el wallpaper
                
                # dibujo el submarino
                screen.blit(submarine_image, submarine_rect)  

                # Creo las minas submarinas

                load_naval_mine(screen, naval_mine_list)
                
                # # Actualización y dibujo del detroyer
                for destroyer in destroyer_list:
                    screen.blit(destroyer["image"], destroyer["rect"])
                    update_destroyer(destroyer["rect"], ship_enemy_speed)
                
                # dibujo los coins
                for coin_dict in coins:    
                    screen.blit(coin_images[coin_dict['index']], (coin_dict['x'], coin_dict['y']))
                    coin_dict['index'] = (coin_dict['index'] + 1) % len(coin_images)  # Actualiza el índice del coin para el próximo frame
                
                # Actualización y dibujo de enemies_images
                for enemies in enemies_images:
                    screen.blit(enemies["image"], enemies["rect"])
                    update_enemies(enemies)

                # Comprueba si ha pasado el tiempo suficiente para disparar 
                if time_last_shot >= shot_interval:
                    # Disparar un misil desde el barco enemigo}
                    shot_bullets_sounds.play()
                    shot_bullets_sounds.set_volume(0.5)
                    destroyer_bullet = create_destroyer_bullet((destroyer["rect"].left + 25, destroyer["rect"].bottom - 25))  # Crea un misil
                    destroyer_bullets.append(destroyer_bullet)  # Agrega el misil a la lista
                    time_last_shot = 0

                # Actualizar y dibujar los misiles
                for destroyer_bullet in destroyer_bullets[:]:
                    # Mueve el misil verticalmente
                    destroyer_bullet["rect"].move_ip(-destroyer_bullet["speed"], destroyer_bullet["speed"])

                    # Dibuja el misil en la pantalla
                    screen.blit(destroyer_bullet["image"], destroyer_bullet["rect"])

                #dibujo y actualizacion de balas frontales
                if front_bullet:
                    for front_bullet in front_bullets[:]:  
                        screen.blit(front_bullet["image"], front_bullet["rect"])
                        front_bullet["rect"].move_ip(front_bullet["speed"], 0)

                #dibujo y actualizacion de balas de arriba del submarino
                if top_bullet:
                    for top_bullet in top_bullets[:]:  
                        screen.blit(top_bullet["image"], top_bullet["rect"])
                        top_bullet["rect"].move_ip(0, top_bullet["speed"])

                #recargo la lista de enemies
                if len(enemies_images) == 0:
                    for _ in range(qty_enemies):
                        enemies = create_enemies(enemies_list)
                        enemies_images.append(enemies)

                # Comprobación para eliminar balas que salen de la ventana

                for front_bullet in front_bullets[:]:
                    if front_bullet["rect"].right > width + width_front_bullet:
                        front_bullets.remove(front_bullet)
                        print("se ha eliminado una bala frontal")
                for top_bullet in top_bullets[:]:
                    if top_bullet["rect"].bottom < 0:
                        top_bullets.remove(top_bullet)
                        print("se ha eliminado una bala superior")

                for destroyer_bullet in destroyer_bullets[:]:
                    if destroyer_bullet["rect"].right < 0 or destroyer_bullet["rect"].top > height:
                        destroyer_bullets.remove(destroyer_bullet)
                        print("se ha eliminado una bala del destroyer")




                ###--- colisiones
                # El manejo de excepciones en este código se realiza utilizando bloques 'try' y 'except'. 
                # El bloque 'try' contiene el código que puede lanzar una excepción en tiempo de ejecución. 
                # Si se produce una excepción en el bloque 'try', la ejecución se detiene inmediatamente y pasa al bloque 'except' correspondiente.
                # En este código, hay varios tipos de excepciones que se manejan específicamente: 
                # - IndexError: Esta excepción se lanza cuando se intenta acceder a un índice que está fuera del rango válido para una lista. Por ejemplo, si intentas acceder a un elemento de una lista que ya ha sido eliminado.
                # - TypeError: Esta excepción se lanza cuando se realiza una operación o función con un tipo de objeto inapropiado. Por ejemplo, si intentas usar un objeto None como si fuera una lista.
                # Si se produce cualquier otro tipo de excepción que no sea IndexError o TypeError, se captura con 'Exception'. 
                # Esta es una clase base para todas las excepciones. Capturar Exception manejará cualquier excepción que no haya sido manejada por los bloques 'except' anteriores.
                # Cada bloque 'except' imprime un mensaje de error que incluye el tipo de error y detalles adicionales sobre el error. 

                # Comprueba si el submarino ha colisionado con una moneda
                try:
                    for coin_dict in coins[:]:
                        if submarine_rect.colliderect(coin_dict["rect"]):
                            collect_coin_sound.play()
                            score += 25
                            coins.remove(coin_dict)
                            print("El submarino ha recogido una moneda")
                            if len(coins) == 0:
                                new_coin = create_coins(coins, qty_coins, width, width_rect_coin, height, height_rect_coin)
                except IndexError as ie:
                    print(f"Error de índice: {ie}")
                except KeyError as ke:
                    print(f"Error de clave: {ke}")
                except Exception as e:
                    print(f"Ha ocurrido un error inesperado: {e}")
                    
                # compruebo si el submarino ha colisionado con una mina submarina
                try:
                    for naval_mine in naval_mine_list[:]:
                        if submarine_rect.colliderect(naval_mine["rect"]):
                            submarine_shield -= 25
                            naval_mine_list.remove(naval_mine)
                            print("El submarino ha colisionado con una mina")
                            create_explosion_list(explotion_list, naval_mine["rect"].centerx, naval_mine["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                            for explosion in explotion_list[:]:
                                screen.blit(explosion["image"], explosion["rect"])
                                explosion["index"] += 1
                                explotion_list.remove(explosion) 
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")

                # compruebo si ha colisionado una bala del destroyer con el submarino
                try:
                    for destroyer_bullet in destroyer_bullets[:]:
                        destroyer_bullet_mask = pygame.mask.from_surface(destroyer_bullet["image"])
                        offset_x_submarine_destroyer_bullets = submarine_rect.x - destroyer_bullet["rect"].x
                        offset_y_submarine_destroyer_bullets = submarine_rect.y - destroyer_bullet["rect"].y
                        if destroyer_bullet_mask.overlap(submarine_mask, (offset_x_submarine_destroyer_bullets, offset_y_submarine_destroyer_bullets)):
                            submarine_shield -= 25
                            destroyer_bullets.remove(destroyer_bullet)
                            print("El submarino ha colisionado con un enemigo")
                            create_explosion_list(explotion_list, destroyer_bullet["rect"].centerx, destroyer_bullet["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                            for explosion in explotion_list[:]:
                                screen.blit(explosion["image"], explosion["rect"])
                                explosion["index"] += 1
                                explotion_list.remove(explosion) 
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")

                # comprubeo si el subamrino ha colisionado con un submarino enemigo
                try:
                    for enemy in enemies_images[:]:
                        enemy_mask = pygame.mask.from_surface(enemy["image"])
                        offset_x_submarine_enemy = submarine_rect.x - enemy["rect"].x
                        offset_y_submarine_enemy  = submarine_rect.y - enemy["rect"].y
                        if submarine_mask.overlap(enemy_mask, (offset_x_submarine_enemy, offset_y_submarine_enemy)):
                            submarine_shield -= 25
                            enemies_images.remove(enemy)
                            print("El submarino ha colisionado con un enemigo")
                            create_explosion_list(explotion_list, enemy["rect"].centerx, enemy["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                            for explosion in explotion_list[:]:
                                screen.blit(explosion["image"], explosion["rect"])
                                explosion["index"] += 1
                                explotion_list.remove(explosion) 
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")

                # comprubeo si una front bullet ha colisionado con un enemigo
                try:
                    for front_bullet in front_bullets[:]:
                        for enemy in enemies_images[:]:
                            front_bullet_mask = pygame.mask.from_surface(front_bullet["image"])
                            enemy_mask = pygame.mask.from_surface(enemy["image"])
                            offset_x_front_bullets_enemy = enemy["rect"].x - front_bullet["rect"].x
                            offset_y_front_bullets_enemy = enemy["rect"].y - front_bullet["rect"].y
                            if front_bullet_mask.overlap(enemy_mask, (offset_x_front_bullets_enemy, offset_y_front_bullets_enemy)):
                                score += 10
                                create_explosion_list(explotion_list, front_bullet["rect"].centerx, front_bullet["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                                for explosion in explotion_list[:]:
                                    screen.blit(explosion["image"], explosion["rect"])
                                    explosion["index"] += 1
                                    explotion_list.remove(explosion) 
                                front_bullets.remove(front_bullet)
                                enemies_images.remove(enemy)
                                print("Una bala frontal ha golpeado a un enemigo")
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")

                #compruebo si una top bullet ha colisionado con el destroyer
                try:
                    for top_bullet in top_bullets[:]:
                        for destroyer in destroyer_list[:]:
                            top_bullet_mask = pygame.mask.from_surface(top_bullet["image"])
                            destroyer_mask = pygame.mask.from_surface(destroyer["image"])
                            offset_x_top_bullets_destroyer = destroyer["rect"].x - top_bullet["rect"].x
                            offset_y_top_bullets_destroyer = destroyer["rect"].y - top_bullet["rect"].y
                            if top_bullet_mask.overlap(destroyer_mask, (offset_x_top_bullets_destroyer, offset_y_top_bullets_destroyer)):
                                score += 25
                                create_explosion_list(explotion_list, top_bullet["rect"].centerx, top_bullet["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                                for explosion in explotion_list[:]:
                                    screen.blit(explosion["image"], explosion["rect"])
                                    explosion["index"] += 1
                                    explotion_list.remove(explosion)    
                                destroyer_list.remove(destroyer)
                                top_bullets.remove(top_bullet)
                                print("Una bala superior ha golpeado a el destructor")
                                create_destroyer(destroyer_list)
                        
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")

                # compruebo si una top bullet ha colisionado con un submarino enemigo
                try:
                    for top_bullet in top_bullets[:]:
                        for enemy in enemies_images[:]:
                            top_bullet_mask = pygame.mask.from_surface(top_bullet["image"])
                            enemy_mask = pygame.mask.from_surface(enemy["image"])
                            offset_x_top_bullets_enemy = enemy["rect"].x - top_bullet["rect"].x
                            offset_y_top_bullets_enemy = enemy["rect"].y - top_bullet["rect"].y
                            if top_bullet_mask is not None and enemy_mask is not None:
                                if top_bullet_mask.overlap(enemy_mask, (offset_x_top_bullets_enemy, offset_y_top_bullets_enemy)):
                                    score += 25
                                    create_explosion_list(explotion_list, top_bullet["rect"].centerx, top_bullet["rect"].centery, width_rect_explotion, height_rect_explotion, num_frames_explotion)
                                    for explosion in explotion_list[:]:
                                        screen.blit(explosion["image"], explosion["rect"])
                                        explosion["index"] += 1
                                        explotion_list.remove(explosion) 
                                    enemies_images.remove(enemy)
                                    top_bullets.remove(top_bullet)
                                    print("Una bala superior ha golpeado a un enemigo")
                except IndexError as e:
                    print(f"Error de índice: {e}")
                except TypeError as e:
                    print(f"Error de tipo: {e}")
                except Exception as e:
                    print(f"Error desconocido: {e}")


                # dibujo la barra de vida
                draw_live_bar(screen, 10, 10, submarine_shield)

                # dibujo el texto de el score y los enemigos
                show_text(screen, (f"Enemies : {qty_enemies + 1}     Score : {score}    Top Bullets : {top_bullet_count}    Front Bullets : {front_bullet_count}"), 55, coordinates_scrore, BLACK)
                
                # dibujo los score en pantalla

                
                pygame.display.update() #funcion para actualizar partalla
                clock.tick(FPS)

        finish()
    elif menu_option == "VER PUNTUACIONES":
        show_high_scores = True  # Habilita la visualización de puntajes

        while show_high_scores:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_high_scores = False  # Sal del bucle de puntajes cuando se cierre la ventana
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica si el jugador hace clic en el botón para volver al menú
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (width // 2 - 100 <= mouse_x <= width // 2 + 100) and (500 <= mouse_y <= 550):
                        show_high_scores = False 
                    # Limpiar la pantalla
                screen.fill(BLACK)

            # Dibuja los puntajes altos
            with open("src\high_scores.txt", "r") as file:
                high_scores = [int(line.strip()) for line in file]
            
            for i, score in enumerate(high_scores, start=1):
                font = pygame.font.Font(None, 36)
                text_surface = font.render(f"Puntaje {i}: {score}", True, WHITE)
                text_rect = text_surface.get_rect(center=(width // 2, 100 + i * 40))
                screen.blit(text_surface, text_rect)

            # Dibuja un botón para volver al menú principal
            pygame.draw.rect(screen, GREEN, (width // 2 - 100, 500, 200, 50))
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Volver al Menú", True, WHITE)
            text_rect = text_surface.get_rect(center=(width // 2, 525))
            screen.blit(text_surface, text_rect)

            # Actualiza la pantalla
            pygame.display.update()




    elif menu_option == "SALIR":
        pygame.quit()
        sys.exit()

    
