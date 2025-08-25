import pygame
import os
import sys

# --- Pygame Initialization ---
# Initialize all imported pygame modules
pygame.init()

# --- Game Constants ---
GAME_WIDTH, GAME_HEIGHT = 800, 600 # The fixed resolution of the game
FPS = 60
WINDOW_TITLE = "Undertale Green"
DEBUG_MODE = True # Set to True to show hitboxes and debug info

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
GREY = (128, 128, 128)
RED = (255, 0, 0)
INTRO_SEPARATOR_COLOR = (138, 90, 157)
HITBOX_COLLISION_COLOR = (255, 255, 255, 255) # White for solid, impassable areas in the hitbox map

# --- Game Configuration ---
# This dictionary holds settings that can be changed in the options menu
game_config = {
    'volume': 0.5,
    'fullscreen': False,
    'language': 'English',
    'controls': {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
}

# --- Language & Translations ---
# A dictionary to store multi-language text for the UI
translations = {
    'start':        {'English': 'START', 'Spanish': 'INICIAR'},
    'options':      {'English': 'OPTIONS', 'Spanish': 'OPCIONES'},
    'quit':         {'English': 'QUIT', 'Spanish': 'SALIR'},
    'fullscreen':   {'English': 'FULLSCREEN', 'Spanish': 'PANTALLA COMPLETA'},
    'on':           {'English': 'ON', 'Spanish': 'SI'},
    'off':          {'English': 'OFF', 'Spanish': 'NO'},
    'volume':       {'English': 'VOLUME', 'Spanish': 'VOLUMEN'},
    'language':     {'English': 'LANGUAGE', 'Spanish': 'IDIOMA'},
    'controls':     {'English': 'CONTROLS', 'Spanish': 'CONTROLES'},
    'reset_progress': {'English': 'RESET PROGRESS', 'Spanish': 'REINICIAR PROGRESO'},
    'back':         {'English': 'BACK', 'Spanish': 'VOLVER'},
    'are_you_sure': {'English': 'ARE YOU SURE?', 'Spanish': '¿ESTÁS SEGURO?'},
    'yes':          {'English': 'YES', 'Spanish': 'SÍ'},
    'no':           {'English': 'NO', 'Spanish': 'NO'},
    'save_file':    {'English': 'SAVE FILE', 'Spanish': 'ARCHIVO DE GUARDADO'},
    'control_up':   {'English': 'UP', 'Spanish': 'ARRIBA'},
    'control_down': {'English': 'DOWN', 'Spanish': 'ABAJO'},
    'control_left': {'English': 'LEFT', 'Spanish': 'IZQUIERDA'},
    'control_right':{'English': 'RIGHT', 'Spanish': 'DERECHA'},
    'press_any_key':{'English': 'PRESS ANY KEY...', 'Spanish': 'PRESIONA UNA TECLA...'},
    'skip':         {'English': '[C] SKIP', 'Spanish': '[C] SALTAR'},
    'intro_texts': {
        'English': [
            "A long time ago, two races ruled over Earth: HUMANS and MONSTERS. They lived in peace and harmony for many years.",
            "One day, for reasons that have been lost to time, war broke out between the two races. It was a long and terrible conflict.",
            "",
            "After a legendary battle, the humans were victorious. They sealed the monsters underground with a magic spell.",
            "This betrayal filled all monsters with a rage incomparable to any other, sealing the fate of all humans who dared enter the underground.",
            "Said rage formed an eldritch horror beyond comprehension, a mass of void so dense no light could reach. PURE HATRED",
            "MT EBBOT 201X"
        ],
        'Spanish': [
            "Hace mucho tiempo, dos razas gobernaban la Tierra: HUMANOS y MONSTRUOS. Vivieron en paz y armonía durante muchos años.",
            "Un día, por razones que se han perdido en el tiempo, la guerra estalló entre las dos razas. Fue un conflicto largo y terrible.",
            "",
            "Tras una batalla legendaria, los humanos resultaron victoriosos. Sellaron a los monstruos bajo tierra con un hechizo mágico.",
            "Esta traición llenó a todos los monstruos con una rabia incomparable, sellando el destino de todos los humanos que se atrevieran a entrar al subsuelo.",
            "Dicha rabia formó un horror incomprensible, una masa de vacío tan densa que ninguna luz podía alcanzar. ODIO PURO.",
            "MT EBBOT 201X"
        ]
    },
}

# Helper function to retrieve translated text based on the current language setting
def get_text(key):
    return translations.get(key, {}).get(game_config['language'], f"<{key}>")

# --- Window and Display Setup ---
# The actual window the player sees
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
# A fixed-size surface where the game is drawn at its native resolution
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# --- Asset Loading ---
# Set up paths for loading game assets like images, fonts, and music
try:
    BASE_PATH = os.path.dirname(__file__)
except NameError:
    BASE_PATH = os.path.abspath(".") # Fallback for environments where __file__ is not defined

ASSETS_PATH = os.path.join(BASE_PATH, "assets")
BACKGROUNDS_PATH = os.path.join(ASSETS_PATH, "backgrounds")
ROOMS_PATH = os.path.join(ASSETS_PATH, "rooms")
FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
IMAGES_PATH = os.path.join(ASSETS_PATH, "images")
MUSIC_PATH = os.path.join(ASSETS_PATH, "music")

# Load fonts with fallbacks to the system default font if custom fonts are not found
try: title_font_50 = pygame.font.Font(os.path.join(FONTS_PATH, "MonsterFriendBack.otf"), 50)
except: title_font_50 = pygame.font.SysFont(None, 60)
try: font_48 = pygame.font.Font(os.path.join(FONTS_PATH, "PixelOperator-Bold.ttf"), 48)
except: font_48 = pygame.font.SysFont(None, 50)
try: font_36 = pygame.font.Font(os.path.join(FONTS_PATH, "PixelOperator-Bold.ttf"), 36)
except: font_36 = pygame.font.SysFont(None, 40)
try: font_28 = pygame.font.Font(os.path.join(FONTS_PATH, "PixelOperator-Bold.ttf"), 28)
except: font_28 = pygame.font.SysFont(None, 32)
# Load the selector icon (the green soul) for menus
try:
    raw_icon = pygame.image.load(os.path.join(IMAGES_PATH, "player", "green_soul.png")).convert_alpha()
    selector_icon = pygame.transform.scale(raw_icon, (raw_icon.get_width() * 2, raw_icon.get_height() * 2))
except:
    selector_icon = pygame.Surface((40, 40))
    selector_icon.fill(WHITE)
    print("Warning: Could not load selector icon, using a placeholder.")


# --- Room Class ---
class Room:
    """Manages the visual layers and collision map for a single game area."""
    def __init__(self, name):
        self.name = name
        self.layers = []  # List of (z_order, surface) tuples for drawing
        self.hitbox = None # A surface used for collision detection
        self.hitbox_mask = None # A mask for fast pixel-perfect collision
        self.debug_hitbox_surface = None # A surface for visualizing the hitbox
        self.load_assets()

    def load_assets(self):
        """
        Loads all images for the room. Visual layers are aspect-scaled.
        The hitbox is built pixel-by-pixel from the source image's white pixels
        and centered on the screen, but not scaled.
        """
        print(f"Loading room: {self.name}")
        room_path = ROOMS_PATH
        try:
            unscaled_hitbox_source = pygame.image.load(os.path.join(room_path, f"{self.name}_hitbox.png")).convert_alpha()
            
            self.hitbox = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            self.hitbox.fill((0, 0, 0, 0))
            self.debug_hitbox_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            self.debug_hitbox_surface.fill((0, 0, 0, 0))

            source_width, source_height = unscaled_hitbox_source.get_size()
            offset_x = (GAME_WIDTH - source_width) // 2
            offset_y = (GAME_HEIGHT - source_height) // 2
            
            for x in range(source_width):
                for y in range(source_height):
                    pixel_color = unscaled_hitbox_source.get_at((x, y))
                    if pixel_color == HITBOX_COLLISION_COLOR:
                        self.hitbox.set_at((x + offset_x, y + offset_y), HITBOX_COLLISION_COLOR)
                        self.debug_hitbox_surface.set_at((x + offset_x, y + offset_y), (255, 255, 255, 100))

            # Create the collision mask from the generated hitbox surface
            self.hitbox_mask = pygame.mask.from_surface(self.hitbox)
            print(f"  - Built and centered hitbox from {self.name}_hitbox.png")

        except pygame.error:
            print(f"  - WARNING: No hitbox found for room '{self.name}'. Creating blank ones.")
            self.hitbox = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            self.hitbox.fill((0, 0, 0, 0))
            self.debug_hitbox_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
            self.debug_hitbox_surface.fill((0, 0, 0, 0))
            self.hitbox_mask = pygame.mask.from_surface(self.hitbox)

        # Load all visual layers for the room
        for filename in os.listdir(room_path):
            if "hitbox" in filename or not filename.startswith(f"{self.name}_") or not filename.endswith(".png"):
                continue

            try:
                is_shadow_layer = "_shadow_" in filename
                layer_str = filename.replace(f"{self.name}_", "").replace(".png", "").replace("shadow_", "")
                z_order = int(layer_str)
                
                unscaled_image = pygame.image.load(os.path.join(room_path, filename)).convert_alpha()

                original_width, original_height = unscaled_image.get_size()
                scale = min(GAME_WIDTH / original_width, GAME_HEIGHT / original_height)
                scaled_width = int(original_width * scale)
                scaled_height = int(original_height * scale)
                scaled_layer_img = pygame.transform.scale(unscaled_image, (scaled_width, scaled_height))

                image = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
                image.fill((0, 0, 0, 0))
                x_pos = (GAME_WIDTH - scaled_width) // 2
                y_pos = (GAME_HEIGHT - scaled_height) // 2
                image.blit(scaled_layer_img, (x_pos, y_pos))

                if is_shadow_layer:
                    image.set_alpha(128)
                    print(f"  - Loaded and aspect-scaled SHADOW layer {filename} with z-order {z_order}")
                else:
                    print(f"  - Loaded and aspect-scaled layer {filename} with z-order {z_order}")
                
                self.layers.append((z_order, image))

            except (ValueError, pygame.error) as e:
                print(f"  - WARNING: Could not load or parse layer: {filename} ({e})")
        
        self.layers.sort()


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """Represents the player character, handling movement, animation, and collision."""
    def __init__(self, x, y):
        super().__init__()
        self.speed = 4
        self.Z_ORDER = 1
        self.animations = {'down': [], 'up': [], 'left': [], 'right': []}
        self.idle_images = {'down': None, 'up': None, 'left': None, 'right': None}
        self.direction = 'down'
        self.animation_index = 0
        self.animation_speed = 0.15
        self.is_moving = False
        
        self.load_sprites()
        self.image = self.idle_images['down']
        # The rect for the visual sprite
        self.rect = self.image.get_rect(center=(x, y))
        
        # Load the hitbox image and create a separate rect for it
        self.hitbox_image = self.load_hitbox_image()
        self.mask = pygame.mask.from_surface(self.hitbox_image)
        self.hitbox_rect = self.hitbox_image.get_rect(center=self.rect.center)
        self.align_hitbox()

    def load_sprites(self):
        """Loads all player animation frames."""
        player_path = os.path.join(IMAGES_PATH, "player")
        scale_factor = 2
        for direction in self.animations.keys():
            try:
                idle_img = pygame.image.load(os.path.join(player_path, f"player_{direction}_idle.png")).convert_alpha()
                self.idle_images[direction] = pygame.transform.scale(idle_img, (idle_img.get_width() * scale_factor, idle_img.get_height() * scale_factor))
            except pygame.error:
                self.idle_images[direction] = pygame.Surface((32 * scale_factor, 48 * scale_factor), pygame.SRCALPHA)
            
            walk_frames = []
            for i in range(2):
                try:
                    img = pygame.image.load(os.path.join(player_path, f"player_{direction}_{i}.png")).convert_alpha()
                    walk_frames.append(pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor)))
                except pygame.error:
                    walk_frames.append(pygame.Surface((32 * scale_factor, 48 * scale_factor), pygame.SRCALPHA))
            
            if direction in ['left', 'right'] and len(walk_frames) == 2:
                self.animations[direction] = [walk_frames[0], self.idle_images[direction], walk_frames[1], self.idle_images[direction]]
            else:
                self.animations[direction] = walk_frames

    def load_hitbox_image(self):
        """Loads the single, unscaled hitbox image from a file."""
        player_path = os.path.join(IMAGES_PATH, "player")
        try:
            hitbox_img = pygame.image.load(os.path.join(player_path, "player_hitbox.png")).convert_alpha()
            print("  - Loaded single player_hitbox.png")
            return hitbox_img
        except pygame.error:
            print(f"  - FATAL ERROR: 'player_hitbox.png' not found. Cannot create player.")
            # Create a tiny fallback surface to prevent a crash, but this is a critical error.
            return pygame.Surface((1, 1), pygame.SRCALPHA)
            
    def align_hitbox(self):
        """Aligns the hitbox rect to the visual rect's bottom-center."""
        self.hitbox_rect.centerx = self.rect.centerx
        self.hitbox_rect.bottom = self.rect.bottom

    def update(self, room):
        """Update player state once per frame."""
        self.handle_input(room)
        self.animate()

    def handle_input(self, room):
        """Handles keyboard input for movement and collision detection using a single mask."""
        keys = pygame.key.get_pressed()
        self.is_moving = False
        last_rect = self.rect.copy()
        last_hitbox_rect = self.hitbox_rect.copy()

        # Move both the visual rect and the hitbox rect
        if keys[game_config['controls']['up']]:
            self.rect.y -= self.speed; self.direction = 'up'; self.is_moving = True
        if keys[game_config['controls']['down']]:
            self.rect.y += self.speed; self.direction = 'down'; self.is_moving = True
        if keys[game_config['controls']['left']]:
            self.rect.x -= self.speed; self.direction = 'left'; self.is_moving = True
        if keys[game_config['controls']['right']]:
            self.rect.x += self.speed; self.direction = 'right'; self.is_moving = True
        
        # Re-align the hitbox to the new visual rect position
        self.align_hitbox()

        if not game_surface.get_rect().contains(self.rect):
            self.rect = last_rect
            self.hitbox_rect = last_hitbox_rect
            return

        # --- Mask-based Collision Detection ---
        offset = (self.hitbox_rect.x, self.hitbox_rect.y)
        if room.hitbox_mask.overlap(self.mask, offset):
            self.rect = last_rect # Revert both rects on collision
            self.hitbox_rect = last_hitbox_rect

    def animate(self):
        """Updates the player's sprite. The mask is now static and does not change."""
        if self.is_moving:
            current_animation = self.animations[self.direction]
            if current_animation:
                self.animation_index = (self.animation_index + self.animation_speed) % len(current_animation)
                self.image = current_animation[int(self.animation_index)]
        else:
            self.image = self.idle_images[self.direction]
            self.animation_index = 0

# --- Helper Functions ---
def draw_text(text, font, color, surface, x, y, center=True):
    """A utility function to draw text onto a surface."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def draw_text_wrapped(text, font, color, surface, rect):
    """Draws text that wraps within a given rectangle."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    y = rect.top
    for line in lines:
        draw_text(line.strip(), font, color, surface, rect.left, y, center=False)
        y += font.get_linesize()

def update_display():
    """Scales the game surface to fit the window while maintaining aspect ratio."""
    screen.fill(BLACK)
    screen_w, screen_h = screen.get_size()
    scale = min(screen_w / GAME_WIDTH, screen_h / GAME_HEIGHT)
    scaled_w, scaled_h = int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale)
    scaled_surf = pygame.transform.scale(game_surface, (scaled_w, scaled_h))
    x_pos = (screen_w - scaled_w) // 2
    y_pos = (screen_h - scaled_h) // 2
    screen.blit(scaled_surf, (x_pos, y_pos))
    pygame.display.flip()

def toggle_fullscreen():
    """Toggles the display between fullscreen and windowed mode."""
    global screen
    game_config['fullscreen'] = not game_config['fullscreen']
    if game_config['fullscreen']:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)

# --- Sprite Sheet Parser ---
def parse_spritesheet(sheet, separator_color):
    """Splits a spritesheet into individual frames based on a separator color."""
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    start_y = 0
    for y in range(sheet_height):
        is_separator = all(sheet.get_at((x, y))[:3] == separator_color for x in range(sheet_width))
        if is_separator or y == sheet_height - 1:
            frame_height = (y - start_y)
            if frame_height > 0:
                frames.append(sheet.subsurface(pygame.Rect(0, start_y, sheet_width, frame_height)))
            start_y = y + 1
    return frames

# --- Game State Functions ---
def intro_sequence():
    """Displays the opening cinematic sequence."""
    try:
        sheet = pygame.image.load(os.path.join(BACKGROUNDS_PATH, "intro.png")).convert()
    except pygame.error:
        print("Warning: intro.png not found. Skipping intro.")
        return "PLAYING"
    
    frames = parse_spritesheet(sheet, INTRO_SEPARATOR_COLOR)
    intro_texts = get_text('intro_texts')
    if not frames:
        print("Warning: No frames found in intro.png. Skipping intro.")
        return "PLAYING"

    frame_index = 0
    clock = pygame.time.Clock()
    typed_chars = 0.0
    typing_speed = 0.75
    typing_finished = False
    typing_finish_time = 0
    POST_TYPE_DELAY = 5000 # 5 seconds

    while frame_index < len(frames):
        current_time = pygame.time.get_ticks()
        current_full_text = intro_texts[frame_index] if frame_index < len(intro_texts) else ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: return "PLAYING" # Skip intro
                if event.key == pygame.K_RETURN:
                    if not typing_finished:
                        typed_chars = len(current_full_text)
                        typing_finished = True
                        typing_finish_time = current_time
                    else:
                        typing_finish_time = current_time - POST_TYPE_DELAY

        if not typing_finished:
            if len(current_full_text) == 0:
                typed_chars = 0; typing_finished = True; typing_finish_time = current_time
            else:
                typed_chars += typing_speed
                if typed_chars >= len(current_full_text):
                    typed_chars = len(current_full_text); typing_finished = True; typing_finish_time = current_time
        
        if typing_finished and current_time - typing_finish_time > POST_TYPE_DELAY:
            frame_index += 1; typed_chars = 0.0; typing_finished = False
            if frame_index >= len(frames): break

        game_surface.fill(BLACK)
        if frame_index < len(frames):
            current_frame = pygame.transform.scale(frames[frame_index], (GAME_WIDTH, GAME_HEIGHT))
            game_surface.blit(current_frame, (0, 0))
            if frame_index < len(intro_texts):
                text_to_display = current_full_text[:int(typed_chars)]
                text_area = pygame.Rect(150, GAME_HEIGHT - 165, 500, 100)
                if current_full_text == "MT EBBOT 201X":
                    draw_text(text_to_display, font_28, WHITE, game_surface, text_area.centerx, text_area.centery)
                else:
                    draw_text_wrapped(text_to_display, font_28, WHITE, game_surface, text_area)
            draw_text(get_text('skip'), font_36, WHITE, game_surface, GAME_WIDTH - 80, GAME_HEIGHT - 30)
        
        update_display(); clock.tick(FPS)
    
    return "PLAYING"

def start_menu():
    """Displays the main menu."""
    title1 = title_font_50.render("undertale ", True, WHITE)
    title2 = title_font_50.render("green", True, GREEN)
    total_w = title1.get_width() + title2.get_width()
    start_x = (GAME_WIDTH - total_w) // 2
    t1_rect = title1.get_rect(topleft=(start_x, GAME_HEIGHT // 5))
    t2_rect = title2.get_rect(topleft=(t1_rect.right, GAME_HEIGHT // 5))
    selected = 0
    
    while True:
        options = [get_text('start'), get_text('options'), get_text('quit')]
        game_surface.fill(BLACK)
        game_surface.blit(title1, t1_rect)
        game_surface.blit(title2, t2_rect)
        
        for i, opt in enumerate(options):
            rect = draw_text(opt, font_48, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT // 2 + 40 + (i - 1) * 60)
            if i == selected:
                sel_rect = selector_icon.get_rect(midright=(rect.left - 20, rect.centery))
                game_surface.blit(selector_icon, sel_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % len(options)
                elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if selected == 0: return "SAVE_SELECT"
                    if selected == 1: return "OPTIONS_MENU"
                    if selected == 2: return "QUIT"
        
        update_display()

def options_menu():
    """Displays the options menu."""
    selected = 0
    while True:
        option_keys = ["FULLSCREEN", "VOLUME", "LANGUAGE", "CONTROLS", "RESET PROGRESS", "BACK"]
        game_surface.fill(BLACK)
        draw_text(get_text('options'), font_48, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT // 8)
        
        for i, key in enumerate(option_keys):
            y_pos = GAME_HEIGHT // 3 + i * 45
            if key == "FULLSCREEN": display_text = f"{get_text('fullscreen')}: {get_text('on') if game_config['fullscreen'] else get_text('off')}"
            elif key == "VOLUME": display_text = f"< {get_text('volume')}: {int(game_config['volume'] * 100)}% >"
            elif key == "LANGUAGE": display_text = f"{get_text('language')}: < {game_config['language']} >"
            else: display_text = get_text(key.lower().replace(" ", "_"))
            
            rect = draw_text(display_text, font_36, WHITE, game_surface, GAME_WIDTH // 2, y_pos)
            if i == selected:
                sel_rect = selector_icon.get_rect(midright=(rect.left - 20, rect.centery))
                game_surface.blit(selector_icon, sel_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % len(option_keys)
                elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % len(option_keys)
                elif event.key == pygame.K_ESCAPE: return "START_MENU"
                
                current_option = option_keys[selected]
                if current_option == "VOLUME":
                    if event.key in [pygame.K_LEFT, pygame.K_a]: game_config['volume'] = round(max(0.0, game_config['volume'] - 0.1), 1)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]: game_config['volume'] = round(min(1.0, game_config['volume'] + 0.1), 1)
                    pygame.mixer.music.set_volume(game_config['volume'])
                elif current_option == "LANGUAGE":
                    if event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                        game_config['language'] = "Spanish" if game_config['language'] == "English" else "English"
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if current_option == "FULLSCREEN": toggle_fullscreen()
                    elif current_option == "CONTROLS": return "CONTROLS_MENU"
                    elif current_option == "RESET PROGRESS":
                        if confirmation_menu(get_text('are_you_sure')):
                            print("Progress would be reset here.")
                    elif current_option == "BACK": return "START_MENU"
        
        update_display()

def controls_menu():
    """Displays the controls rebinding menu."""
    selected = 0
    listening_for_key = -1
    
    while True:
        control_actions = ['up', 'down', 'left', 'right']
        game_surface.fill(BLACK)
        draw_text(get_text('controls'), font_48, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT // 8)
        
        for i, action in enumerate(control_actions):
            y_pos = GAME_HEIGHT // 4 + i * 60
            key_name = pygame.key.name(game_config['controls'][action]).upper()
            display_text = f"{get_text('control_' + action)}: {key_name}"
            if listening_for_key == i:
                display_text = f"{get_text('control_' + action)}: {get_text('press_any_key')}"
            
            rect = draw_text(display_text, font_36, WHITE, game_surface, GAME_WIDTH // 2, y_pos)
            if i == selected and listening_for_key == -1:
                sel_rect = selector_icon.get_rect(midright=(rect.left - 20, rect.centery))
                game_surface.blit(selector_icon, sel_rect)
        
        back_rect = draw_text(get_text('back'), font_36, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT - 100)
        if selected == len(control_actions) and listening_for_key == -1:
            sel_rect = selector_icon.get_rect(midright=(back_rect.left - 20, back_rect.centery))
            game_surface.blit(selector_icon, sel_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if listening_for_key != -1:
                    game_config['controls'][control_actions[listening_for_key]] = event.key
                    listening_for_key = -1
                else:
                    if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % (len(control_actions) + 1)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % (len(control_actions) + 1)
                    elif event.key == pygame.K_ESCAPE: return "OPTIONS_MENU"
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        if selected < len(control_actions):
                            listening_for_key = selected
                        else:
                            return "OPTIONS_MENU"
        
        update_display()

def confirmation_menu(message):
    """A generic confirmation dialog (Yes/No)."""
    selected = 1
    while True:
        options = [get_text('yes'), get_text('no')]
        game_surface.fill(BLACK)
        draw_text(message, font_36, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT // 3)
        
        for i, opt in enumerate(options):
            rect = draw_text(opt, font_36, WHITE, game_surface, GAME_WIDTH // 2, GAME_HEIGHT // 2 + i * 60)
            if i == selected:
                draw_text(">", font_36, WHITE, game_surface, rect.left - 30, rect.centery)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]: selected = 1 - selected
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: return options[selected] == get_text('yes')
                elif event.key == pygame.K_ESCAPE: return False
        
        update_display()

def save_select_menu():
    """Displays the save file selection screen."""
    try:
        bg_image = pygame.transform.scale(pygame.image.load(os.path.join(BACKGROUNDS_PATH, "saves.png")).convert(), (GAME_WIDTH, GAME_HEIGHT))
    except pygame.error:
        bg_image = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        bg_image.fill(BLACK)
    
    selected = 0
    while True:
        game_surface.blit(bg_image, (0, 0))
        for i in range(3):
            opt = f"{get_text('save_file')} {i + 1}"
            box_surf = pygame.Surface((GAME_WIDTH // 2, 100), pygame.SRCALPHA)
            box_surf.fill((0, 0, 0, 150))
            pygame.draw.rect(box_surf, GREEN, box_surf.get_rect(), 3)
            draw_text(opt, font_36, WHITE, box_surf, box_surf.get_width()//2, box_surf.get_height()//2)
            
            main_box_rect = game_surface.blit(box_surf, box_surf.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 + (i - 1) * 120)))
            if i == selected:
                sel_rect = selector_icon.get_rect(midright=(main_box_rect.left - 15, main_box_rect.centery))
                game_surface.blit(selector_icon, sel_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]: selected = (selected - 1) % 3
                elif event.key in [pygame.K_DOWN, pygame.K_s]: selected = (selected + 1) % 3
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]: return "INTRO"
                elif event.key == pygame.K_ESCAPE: return "START_MENU"
        
        update_display()

def game_loop():
    """The main game loop where gameplay occurs."""
    clock = pygame.time.Clock()
    player = Player(GAME_WIDTH // 2, GAME_HEIGHT // 2)
    all_sprites = pygame.sprite.Group(player)
    
    current_room = Room("startingscene")

    pygame.mixer.music.set_volume(game_config['volume'])
    try:
        pygame.mixer.music.load(os.path.join(MUSIC_PATH, "background_music.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Could not load music: {e}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "OPTIONS_MENU"

        all_sprites.update(current_room)
        
        game_surface.fill(BLACK)
        
        render_groups = {}
        for z, layer_img in current_room.layers:
            if z not in render_groups: render_groups[z] = []
            render_groups[z].append(layer_img)
        
        player_z = player.Z_ORDER
        if player_z not in render_groups: render_groups[player_z] = []
        render_groups[player_z].append(all_sprites)

        for z in sorted(render_groups.keys()):
            for item in render_groups[z]:
                if isinstance(item, pygame.sprite.Group):
                    item.draw(game_surface)
                else:
                    game_surface.blit(item, (0, 0))

        if DEBUG_MODE:
            game_surface.blit(current_room.debug_hitbox_surface, (0, 0))
            
            # Create a surface from the player's hitbox mask to visualize it
            mask_surf = player.mask.to_surface(setcolor=RED, unsetcolor=(0,0,0,0))
            mask_surf.set_colorkey((0,0,0))
            mask_surf.set_alpha(150)
            game_surface.blit(mask_surf, player.hitbox_rect.topleft)
            
            debug_info = f"Speed: {player.speed} | Pos: ({player.rect.x}, {player.rect.y})"
            draw_text(debug_info, font_28, WHITE, game_surface, 10, 10, center=False)

        update_display()
        clock.tick(FPS)

# --- Main Game Manager ---
def main():
    """Manages the overall game state and transitions between different screens."""
    try:
        icon = pygame.image.load(os.path.join(IMAGES_PATH, "player", "green_soul.png"))
        pygame.display.set_icon(icon)
    except pygame.error as e:
        print(f"Could not load window icon: {e}")
    
    game_state = "START_MENU"
    while True:
        if game_state == "START_MENU": game_state = start_menu()
        elif game_state == "OPTIONS_MENU": game_state = options_menu()
        elif game_state == "CONTROLS_MENU": game_state = controls_menu()
        elif game_state == "SAVE_SELECT": game_state = save_select_menu()
        elif game_state == "INTRO": game_state = intro_sequence()
        elif game_state == "PLAYING": game_state = game_loop()
        elif game_state == "QUIT": break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
