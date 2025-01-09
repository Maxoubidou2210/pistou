
import math
import pygame
import sys
from datetime import datetime

import numpy as np
import textwrap
import threading
import queue
import SIMU_LIB as sim
import time
import socket


#Création de la queue
Data=np.zeros(77)
Data[:4]=[0,0,0,0]
Data[4:]=sim.moteur(0,1279,0) #tt4_0=1279K

D=queue.Queue()
D.put(Data)

#Données réseau

MULTICAST_IP_DEST='1'
PORT_DEST='1'

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 1280, 1024  
BACKGROUND_COLOR = (150, 150, 150)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (254, 203, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)  # Light green for the active button
LIGHT_GRAY = (210, 210, 210)
BUTTON_COLOR = LIGHT_GRAY
BLUE = (0,255,255)
DARK_GRAY = (169, 169, 169)
BLUE_GRAY = (120, 150, 180)
Alaska_color=LIGHT_GRAY
# Polices
def_font = pygame.font.Font(None, 24)
font_bold = pygame.font.Font(None, 20)

# Enter
active_CSG = False  
active_TLA1=False
ative_TLA2=False
active_TLA3=False
CSG_color=LIGHT_GRAY
TLA1_color = LIGHT_GRAY 
TLA2_color=LIGHT_GRAY
TLA3_color=LIGHT_GRAY
 
value_CSG = ""  
value_TLA1=""
value_TLA2=""
value_TLA3=""

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Win CC Simulateur pour Safran")

# Fonts
font = pygame.font.SysFont("arial", 14)
font_bold = pygame.font.SysFont("arial", 14, bold=True)
font_large = pygame.font.SysFont("arial", 20, bold=True)

# Gauge variables
gauge_y = 400
gauge_min_y = 300
gauge_max_y = 600
gauge_x = 90
gauge_width = 40
gauge_height = gauge_max_y - gauge_min_y
cursor_width = 50
cursor_height = 10
gauge_dragging = False
Data=D.get()

# Degrees variable for precision
gauge_degrees = Data[3]  # Current degree (0° to 40°)
D.put(Data)
# Button dimensions and positions
button_width = 80
button_height = 30
button_spacing = 5
button_y = gauge_min_y - button_height - button_spacing
button_apprch_x = gauge_x - 65
button_sol_x = button_apprch_x + button_width + button_spacing
button_vol_x = button_sol_x + button_width - 40 + button_spacing
tk_off_x = gauge_x + 50
tk_off_y = gauge_min_y - 30
max_rvrs_x = tk_off_x
max_rvrs_y = gauge_max_y - 25

# Gauge control buttons dimensions
control_width = int(50 * 0.7)
control_height = int(50 * 0.7)
control_x = gauge_x - 50
center_y = (gauge_min_y + gauge_max_y) // 2

# Track the selected button
selected_button = None  # Can be "Apprch", "Sol", or "Vol"

# Track the state of the buttons for approach, vol, and sol
button_states = {"Apprch": False, "Sol": False, "Vol": False}

# Buttons in the header
buttons = {
    "Recettes Historisation": (10, 110, 120, 30),
    "Platine de démarrage": (140, 110, 120, 30),
    "Alarmes moteur": (270, 110, 120, 30),
    "Protec. survitesse": (400, 110, 120, 30),
    "Profil Manette": (530, 110, 120, 30),
    "PMA Coup./c.circuit": (660, 110, 120, 30),
    "ATC 1": (800, 110, 50, 30),
    "ATC 2": (850, 110, 50, 30),
    "ATC 3": (900, 110, 50, 30),
    "MCO 1": (1000, 110, 50, 30),
    "MCO 2": (1050, 110, 50, 30)
}

# Windows for each button
window_contents = {
    "Recettes Historisation": "Window 1 Content",
    "Platine de démarrage": "Platine de démarrage Content",  # For this page, we will display the gauge.
    "Alarmes moteur": "Window 3 Content",
    "Protec. survitesse": "Window 4 Content",
    "Profil Manette": "Window 5 Content",
    "PMA Coup./c.circuit": "Window 6 Content",
    "ATC 1": "Window 7 Content",
    "ATC 2": "Window 8 Content",
    "ATC 3": "Window 9 Content",
    "MCO 1": "Window 10 Content",
    "MCO 2": "Window 11 Content"
}

# Load and resize the logo image
logo = pygame.image.load("Safran_logo.png")  # Assumes the logo is in the same directory as the script
logo = pygame.transform.scale(logo, (180, 100))  # Resize the logo to a smaller size



# Définition des boutons
button_A = pygame.Rect(300, 400, 50, 25)
button_AB = pygame.Rect(350, 400, 50, 25)
button_B = pygame.Rect(400, 400, 50, 25)
button_OFF = pygame.Rect(350, 530, 50, 25)  # Nouveau bouton OFF

# Chargement de l'image (rond jaune)
rond_jaune = pygame.image.load("rond_jaune.png")
rond_jaune = pygame.transform.scale(rond_jaune, (70, 70))  # Redimensionner l'image si nécessaire
rond_jaune_rect = rond_jaune.get_rect()
rond_jaune_rect.center = (375, 470)  # Position initiale sous les boutons

# Initialisation de l'angle de rotation
rotation_angle = 0  # angle initial


# Boutons Fenetre 9

button_M2 = pygame.Rect(550, 630, 80, 50)  # Nouveau bouton 1 à gauche de A
button_M1 = pygame.Rect(630, 630, 80, 50)
button_N = pygame.Rect(710, 630, 80, 50)
button_nor = pygame.Rect(790, 630, 80, 50)
button_S = pygame.Rect(870, 630, 80, 50)  
rond_jaune9 = pygame.image.load("rond_jaune.png")
rond_jaune9 = pygame.transform.scale(rond_jaune9, (70, 70))  # Redimensionner l'image si nécessaire
rond_jaune_rect9 = rond_jaune9.get_rect()
rond_jaune_rect9.center = (750, 740)  # Position initiale sous les boutons
rotation_angle9 = 0  # angle initial

# Bouttons Fenetre 10
button_A10 = pygame.Rect(1075, 630, 50, 25)
button_AB10 = pygame.Rect(1125, 630, 50, 25)
button_B10 = pygame.Rect(1175, 630, 50, 25)
rond_jaune10 = pygame.image.load("rond_jaune.png")
rond_jaune10 = pygame.transform.scale(rond_jaune10, (70, 70))  # Redimensionner l'image si nécessaire
rond_jaune_rect10 = rond_jaune10.get_rect()
rond_jaune_rect10.center = (1150, 700)  # Position initiale sous les boutons
rotation_angle10 = 0  # angle initial

# Boutons fenetre 11
button_1 = pygame.Rect(300, 850, 50, 25)
button_12 = pygame.Rect(350, 850, 50, 25)
button_2 = pygame.Rect(400, 850, 50, 25)
button_OFF11 = pygame.Rect(350, 980, 50, 25)  # Nouveau bouton OFF
rond_jaune11 = pygame.image.load("rond_jaune.png")
rond_jaune11 = pygame.transform.scale(rond_jaune11, (70, 70)) 
rond_jaune_rect11 = rond_jaune11.get_rect()
rond_jaune_rect11.center = (375, 920)  
rotation_angle11 = 0  


active_button = None
# Fonction pour vérifier si un clic est sur un bouton
def button_click(rect, pos):
    return rect.collidepoint(pos)

# Fonction pour dessiner une ligne reliant l'image au bouton
def draw_line_to_button(start_pos, button_rect, button_type="vertical"):
    if button_type == "vertical":
        pygame.draw.line(screen, BLACK, start_pos, (button_rect.centerx, button_rect.bottom), 4)
    elif button_type == "vertical1":
        pygame.draw.line(screen, BLACK, start_pos, (button_rect.centerx, button_rect.top), 4)


# Utility functions
def draw_text(surface, text, x, y, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
    
def draw_rectangle(screen, color, rect, text, font, text_color, border_color=(0, 0, 0), border_width=1):
    # Function to check if text fits inside the rectangle
    def text_fits(font, text, width, height):
        # Wrap the text within the rectangle width
        lines = textwrap.wrap(text, width=width // (font.size(' ')[0]))
        total_height = sum([font.size(line)[1] for line in lines])
        return (max(font.size(line)[0] for line in lines) <= width) and (total_height <= height)

    # Draw the filled rectangle
    pygame.draw.rect(screen, color, rect)

    # Draw the border around the rectangle
    pygame.draw.rect(screen, border_color, rect, border_width)

    # Initial font size
    font_size = 15
    font = pygame.font.SysFont("arial", font_size, bold=True)

    # Check if the text fits
    while not text_fits(font, text, rect.width, rect.height) and font_size > 8:
        font_size -= 1
        font = pygame.font.SysFont("arial", font_size, bold=True)

    # Wrap the text if necessary
    lines = textwrap.wrap(text, width=rect.width // (font.size(' ')[0]))

    # Calculate the vertical offset to center the text in the rectangle
    total_text_height = sum([font.size(line)[1] for line in lines])
    y_offset = (rect.height - total_text_height) // 2 + rect.top

    # Draw the text within the rectangle
    for line in lines:
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_offset + font.size(line)[1] // 2))
        screen.blit(text_surface, text_rect)
        y_offset += font.size(line)[1]
    
def draw_button(x, y, w, h, color, text, text_color=(0, 0, 0), border_color=None, shadow_offset=1.2, shadow_color=(255, 255, 255)):
    shadow_rect = pygame.Rect(x - shadow_offset, y - shadow_offset, w, h)
    pygame.draw.rect(screen, shadow_color, shadow_rect)
    pygame.draw.rect(screen, color, (x, y, w, h))

    # Adjust font size to fit the button
    max_font_size = 14
    font_size = max_font_size
    font = pygame.font.SysFont("arial", font_size, bold=True)

    # Function to check if text fits within the button
    def text_fits(font, text, width):
        lines = textwrap.wrap(text, width=width // (font_size // 2))
        total_width = max(font.size(line)[0] for line in lines)
        return total_width <= width

    # Reduce font size until text fits
    while not text_fits(font, text, w - 10) and font_size > 8:
        font_size -= 1
        font = pygame.font.SysFont("arial", font_size, bold=True)

    # Wrap the text without breaking words
    text_lines = textwrap.wrap(text, width=w // (font_size // 2))

    total_text_height = sum([font.size(line)[1] for line in text_lines])
    y_offset = (h - total_text_height) // 2

    for line in text_lines:
        text_surface = font.render(line, True, text_color)
        text_rect = text_surface.get_rect(center=(x + w // 2, y + y_offset + font.size(line)[1] // 2))
        screen.blit(text_surface, text_rect)
        y_offset += font.size(line)[1]

    if border_color:
        pygame.draw.rect(screen, border_color, (x, y, w, h), 1)

def calculate_percentage(y_pos):
    return int(100 * (gauge_max_y - y_pos) / gauge_height)

def calculate_degrees(percentage):
    return -30 + (percentage * (45 + 30)) / 100

def degrees_to_y(degrees):
    return gauge_max_y - (degrees / 43) * gauge_height

def y_to_degrees(y):
    return (gauge_max_y - y) / gauge_height * 43

def draw_horizontal_gauge(x, y, value, max_value, label, unit, font):
    pygame.draw.rect(screen, BLACK, (x, y, 400, 20))  # Jauge en jaune
    pygame.draw.rect(screen, BLACK, (x, y, 400, 20), 1)  # Bordure noire
    fill_width = (value / max_value) * 400
    pygame.draw.rect(screen, (0, 0, 139), (x, y, fill_width, 20))  # Jauge remplie
    label_text = f"{label} {value} {unit}"
    draw_text(screen, label_text, x - 140, y , font)
    

def draw_vertical_gauge(x, y, value, max_value, background_color, fill_color):
    pygame.draw.rect(screen, background_color, (x, y, 30, 130))  # Draw the background of the gauge
    fill_height = (value / max_value) * 130
    pygame.draw.rect(screen, fill_color, (x, y + 130 - fill_height, 30, fill_height))  # Draw the fill of the gauge
    pygame.draw.rect(screen, BLACK, (x, y, 30, 130), 1)  # Draw the border of the gauge
    label_text = f"{value}"
    draw_text(screen, label_text, x+5, y+140 , font)
    label_text = "############"
    draw_text(screen, label_text, x-20, y-25 , font)

# Function to change gauge values periodically
def change_gauge_values():
    global gauge_values
    Data=D.get()
    gauge_values =[int(Data[60]),Data[26]*10**(-5),int(Data[34]),int(Data[69]*100)]
    D.put(Data)

def draw_interface():
    global gauge_y, selected_button, button_state, gauge_degrees,rotation_angle

    screen.fill(BACKGROUND_COLOR)

    header_height = 150
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, header_height))  # Header area with yellow background
    pygame.draw.line(screen, BLACK, (0, header_height), (WIDTH, header_height), 2)  # Draw a line to separate the header
    # Draw the logo in the top left corner
    screen.blit(logo, (0, 0))  # Draw the logo at position (10, 10)
    
    for button_text, (x, y, w, h) in buttons.items():
        draw_button(x, y, w, h, BUTTON_COLOR, button_text)

    now = datetime.now()
    draw_text(screen, now.strftime("%d/%m/%Y"), 1190, 10, pygame.font.Font(None, 22))
    draw_text(screen, now.strftime("%H:%M:%S"), 1200, 30, pygame.font.Font(None, 22))

    draw_text(screen, "Ver. 0 0 0", 1180, 50, pygame.font.Font(None, 16))
    draw_text(screen, "Version Soft EEC", 1180, 70, pygame.font.Font(None, 16))

    if selected_button == "Platine de démarrage":
        
        #Grey background
        
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(5, 160, 230, 850)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(5, 160, 230, 850), 1)
        
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(240, 160, 600, 200)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(240, 160, 600, 200), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(845, 160, 430, 200)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(845, 160, 430, 200), 1)
        
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(240, 365, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(240, 365, 255, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(500, 365, 515, 225)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(500, 365, 515, 225), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(1020, 365, 90, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1020, 365, 90, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(1115, 365, 160, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1115, 365, 160, 220), 1)
        
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(240, 590, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(240, 590, 255, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(500, 595, 515, 215)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(500, 595, 515, 215), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(1020, 590, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1020, 590, 255, 220), 1)
        
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(240, 815, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(240, 815, 255, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(500, 815, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(500, 815, 255, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(760, 815, 255, 150)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(760, 815, 255, 150), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(760, 970, 255, 70)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(760, 970, 255, 220), 1)
        pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(1020, 815, 255, 220)); pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1020, 815, 255, 220), 1)


        # Value
        draw_text(screen, f"{gauge_degrees:.1f}°", gauge_x - 50, gauge_max_y - 300, def_font)
        # Draw the main gauge below the header
        pygame.draw.rect(screen, YELLOW, (gauge_x, gauge_min_y, gauge_width, gauge_height))
        pygame.draw.rect(screen, BLACK, (gauge_x, gauge_min_y, gauge_width, gauge_height), 1)
        cursor_rect = pygame.Rect(gauge_x - 5, gauge_y, cursor_width, cursor_height)
        pygame.draw.rect(screen, BLACK, cursor_rect, border_radius=5)

        percentage = y_to_degrees(gauge_y) #pourcentage
        degrees = degrees_to_y(percentage) #degress
        
        # Case for the enter

        draw_text(screen, "Csg", gauge_x - 38, gauge_max_y + 10, font_large)
        pygame.draw.rect(screen, WHITE, (gauge_x, gauge_max_y + 10, 60, 30))
        draw_text(screen, f"{gauge_degrees:.1f}°", gauge_x + 10, gauge_max_y + 17, font_bold)

        draw_button(gauge_x - 50, gauge_max_y + 50, 180, 40, YELLOW, "Stop")
         
        pygame.draw.rect(screen, CSG_color, (gauge_x, gauge_max_y + 10, 60, 30))
        pygame.draw.rect(screen, BLACK, (gauge_x, gauge_max_y + 10, 60, 30), 2)

            
        #TLA
        draw_button(gauge_x - 77, gauge_max_y + 160, 65, 30, BUTTON_COLOR, "GO\nTLA1", BLACK)
        draw_button(gauge_x-10 , gauge_max_y + 160, 80, 30, BUTTON_COLOR, "GO\nTLA2", BLACK)
        draw_button(gauge_x +62, gauge_max_y + 160, 80, 30, BUTTON_COLOR, "GO\nTLA3", BLACK)
        
        draw_text(screen, "TLA1", gauge_x - 72, gauge_max_y + 95, font_large)
        draw_text(screen, "TLA2", gauge_x-5, gauge_max_y + 95, font_large)
        draw_text(screen, "TLA3", gauge_x +67, gauge_max_y + 95, font_large)
        
        draw_text(screen, "Inc.(°/s)", gauge_x - 72, gauge_max_y + 220, font_large)
        draw_text(screen, "Déc.(°/s)", gauge_x+50, gauge_max_y + 220, font_large)
        
        pygame.draw.rect(screen, TLA1_color, (gauge_x - 77, gauge_max_y + 120, 60, 30))
        pygame.draw.rect(screen, TLA2_color, (gauge_x-10, gauge_max_y + 120, 60, 30))
        pygame.draw.rect(screen, TLA3_color, (gauge_x+62, gauge_max_y + 120, 60, 30))
        
        pygame.draw.rect(screen, WHITE, (gauge_x - 77, gauge_max_y + 250, 100, 30))
        pygame.draw.rect(screen, WHITE, (gauge_x+40, gauge_max_y + 250, 100, 30))
        
        #enter value
      
        if value_CSG:
            draw_text(screen,value_CSG , gauge_x+5, gauge_max_y + 17, def_font)
        if value_TLA1:
            draw_text(screen, value_TLA1, gauge_x - 65, gauge_max_y + 130, def_font)
        if value_TLA2:
            draw_text(screen, value_TLA2, gauge_x + 5, gauge_max_y + 130, def_font)
        if value_TLA3:
            draw_text(screen, value_TLA3, gauge_x +75 , gauge_max_y + 130, def_font)
    
        # Draw the 3 buttons above the gauge with color based on selection
        draw_button(button_apprch_x, button_y - 10, button_width - 15, button_height, 
                    GREEN if button_states["Apprch"] else LIGHT_GRAY, "Apprch")
        draw_button(button_sol_x - 15, button_y - 10, button_width - 40, button_height, 
                    GREEN if button_states["Sol"] else LIGHT_GRAY, "Sol")
        draw_button(button_vol_x - 15, button_y - 10, button_width - 40, button_height, 
                    GREEN if button_states["Vol"] else LIGHT_GRAY, "Vol")

        
        draw_button(control_x, center_y - 8, control_width, control_height, BUTTON_COLOR, "+")
        draw_button(control_x, center_y + 30, control_width, control_height - 10, BUTTON_COLOR, "0.1°")
        draw_button(control_x, center_y + 58, control_width, control_height, BUTTON_COLOR, "-")
        # Auxiliary buttons
        draw_button(tk_off_x, tk_off_y + 25, 65, 30, BUTTON_COLOR, "<Tk OFF", BLACK)
        draw_button(max_rvrs_x, max_rvrs_y, 80, 30, BUTTON_COLOR, "<Max Rvrs", BLACK)
        
        
        #Fenetre 2
        gauge_positions = [(400, 180), (400, 230), (400, 280), (400, 330)]
        
        for idx, (x, y) in enumerate(gauge_positions):
            label = ["Poussée", "Pt3", "EGT", "rendement_th"]
            unit = ["N", "bar", "K", "%"]
            MAX=[100000,35,780,55]
            value = gauge_values[idx]
            draw_horizontal_gauge(x, y, value, MAX[idx], label[idx], unit[idx], font_bold)

        #Fenetre 3
        gauge_positions1 = [(900, 200), (1000, 200), (1100, 200), (1200, 200)]
        
        for idx, (x, y) in enumerate(gauge_positions1):
            MAX=[100000,35,780,55]
            value = gauge_values[idx]
            draw_vertical_gauge(x, y, gauge_values[idx], MAX[idx], YELLOW, BLACK)


    #Fenetre 4
    
        draw_text(screen, "28 VDC EEC", 320, 370, font_large)
        draw_button(button_A.x, button_A.y, button_A.width, button_A.height, LIGHT_GRAY, "A", text_color=BLACK)
        draw_button(button_AB.x, button_AB.y, button_AB.width, button_AB.height, LIGHT_GRAY, "A&B", text_color=BLACK)
        draw_button(button_B.x, button_B.y, button_B.width, button_B.height, LIGHT_GRAY, "B", text_color=BLACK)
        draw_button(button_OFF.x, button_OFF.y, button_OFF.width, button_OFF.height, LIGHT_GRAY, "OFF", text_color=BLACK)
        pygame.draw.line(screen, BLACK, (button_A.centerx, button_A.bottom), (button_A.centerx, button_A.bottom + 20), 4)
        end_pos_A = (button_A.centerx, button_A.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_B.centerx, button_B.bottom), (button_B.centerx, button_B.bottom + 20), 4)
        end_pos_B = (button_B.centerx, button_B.bottom + 20)
        pygame.draw.line(screen, BLACK, end_pos_A, rond_jaune_rect.center, 6)  # Ligne de A à l'image
        pygame.draw.line(screen, BLACK, end_pos_B, rond_jaune_rect.center, 6)  # Ligne de B à l'image
        draw_line_to_button(rond_jaune_rect.center, button_AB, button_type="vertical")
        draw_line_to_button(rond_jaune_rect.center, button_OFF, button_type="vertical1")
        rotated_image = pygame.transform.rotate(rond_jaune, math.degrees(rotation_angle))
        rotated_rect = rotated_image.get_rect(center=rond_jaune_rect.center)
    # Afficher l'image tournée sous les boutons
        screen.blit(rotated_image, rotated_rect.topleft)
        
        #Fenetre 5
        
        BASE_X, BASE_Y = 460, 355
        BASE_X_GRAD=BASE_X+120
        
        pygame.draw.rect(screen, LIGHT_GRAY, (BASE_X + 150, BASE_Y + 20, 404, 40))
        pygame.draw.rect(screen, DARK_GRAY, (BASE_X_GRAD + 50, BASE_Y + 20, 375, 15))  
        pygame.draw.rect(screen, BLUE_GRAY, (BASE_X_GRAD + 50, BASE_Y + 20, 150, 15))  

        for i in range(6):  # 6 graduations (0 à 125 par pas de 25)
            x_pos = BASE_X_GRAD + 50 + i * 75  
            pygame.draw.line(screen, BLACK, (x_pos, BASE_Y + 20), (x_pos, BASE_Y + 40), 2)  
            draw_text(screen, str(i * 25), x_pos - 10, BASE_Y + 40, font)  
      
        draw_text(screen, "N2 % : ###", BASE_X +55 , BASE_Y+20 , font_large)

        draw_text(screen, "Alimentation 115V / 400Hz", BASE_X + 85, BASE_Y + 70, font_large)
        draw_text(screen, "#### V    #### A", BASE_X + 95, BASE_Y + 100, font_large)
    
        pygame.draw.rect(screen, BACKGROUND_COLOR, (BASE_X + 400, BASE_Y + 70, 150, 30))
        draw_text(screen, "Default fatal", BASE_X + 435, BASE_Y + 75, font)

        pygame.draw.rect(screen, BACKGROUND_COLOR, (BASE_X + 400, BASE_Y + 105, 150, 30))
        draw_text(screen, "Default majeur", BASE_X + 435, BASE_Y + 110, font)

        pygame.draw.rect(screen, LIGHT_GRAY, (BASE_X + 50, BASE_Y + 145, 235, 30))
        draw_text(screen, "PDB - Etat INDEFINI", BASE_X + 100, BASE_Y + 150, font)
        pygame.draw.rect(screen, LIGHT_GRAY, (BASE_X + 310, BASE_Y + 145, 235, 30))
        draw_text(screen, "SVS - Mode INDEFINI", BASE_X + 360, BASE_Y + 150, font)

        draw_text(screen, "Air refroid. S/G", BASE_X + 50, BASE_Y + 190, font_large)
        pygame.draw.rect(screen, WHITE, (BASE_X + 200, BASE_Y + 185, 55, 30))
        draw_text(screen, "#####   g/s", BASE_X + 207, BASE_Y + 190, font_large)

        draw_text(screen, "### g/s", BASE_X + 365, BASE_Y + 190, font_large)

        draw_text(screen, "### bar", BASE_X + 465, BASE_Y + 190, font_large)
        #Fenetre 6
        draw_text(screen, "ф level", 1030, 370, font_large)
        
        # Fenetre 7 
        draw_text(screen, "Air Data", 1160, 370, font_large)
        
        #Fenetre 9
        draw_button(button_M2.x, button_M2.y, button_M2.width, button_M2.height, GREEN if active_button == button_M2 else LIGHT_GRAY, "Moteur 2", text_color=BLACK)
        draw_button(button_M1.x, button_M1.y, button_M1.width, button_M1.height,GREEN if active_button == button_M1 else LIGHT_GRAY , "Moteur 1", text_color=BLACK)
        draw_button(button_N.x, button_N.y, button_N.width, button_N.height,GREEN if active_button == button_N else LIGHT_GRAY , "Neutre", text_color=BLACK)
        draw_button(button_nor.x, button_nor.y, button_nor.width, button_nor.height, GREEN if active_button == button_nor else LIGHT_GRAY, "Normal", text_color=BLACK)
        draw_button(button_S.x, button_S.y, button_S.width, button_S.height, GREEN if active_button == button_S else LIGHT_GRAY, "Start", text_color=BLACK)
        pygame.draw.line(screen, BLACK, (button_M2.centerx, button_M2.bottom), (button_M2.centerx, button_M2.bottom + 20), 4)
        end_pos_M2 = (button_M2.centerx, button_M2.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_S.centerx, button_S.bottom), (button_S.centerx, button_S.bottom + 20), 4)
        end_pos_S = (button_S.centerx, button_S.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_M1.centerx, button_M1.bottom), (button_M1.centerx, button_M1.bottom + 20), 4)
        end_pos_M1 = (button_M1.centerx, button_M1.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_nor.centerx, button_nor.bottom), (button_nor.centerx, button_nor.bottom + 20), 4)
        end_pos_nor = (button_nor.centerx, button_nor.bottom + 20)
        pygame.draw.line(screen, BLACK, end_pos_M2, rond_jaune_rect9.center, 6)  # Ligne de 1 à l'image
        pygame.draw.line(screen, BLACK, end_pos_S, rond_jaune_rect9.center, 6)  # Ligne de 2 à l'image
        pygame.draw.line(screen, BLACK, end_pos_M1, rond_jaune_rect9.center, 6)  # Ligne de A à l'image
        pygame.draw.line(screen, BLACK, end_pos_nor, rond_jaune_rect9.center, 6)  # Ligne de B à l'image
        draw_line_to_button(rond_jaune_rect9.center, button_N, button_type="vertical")
        rotated_image9 = pygame.transform.rotate(rond_jaune9, math.degrees(rotation_angle9))
        rotated_rect9 = rotated_image9.get_rect(center=rond_jaune_rect9.center)
        screen.blit(rotated_image9, rotated_rect9.topleft)
        
     # Fenetre 10
        draw_text(screen, "Forçage canal actif", 1060, 600, font_large)
        draw_button(button_A10.x, button_A10.y, button_A10.width, button_A10.height, LIGHT_GRAY, "A", text_color=BLACK)
        draw_button(button_AB10.x, button_AB10.y, button_AB10.width, button_AB10.height, LIGHT_GRAY, "NEUTRE", text_color=BLACK)
        draw_button(button_B10.x, button_B10.y, button_B10.width, button_B10.height, LIGHT_GRAY, "B", text_color=BLACK)
        pygame.draw.line(screen, BLACK, (button_A10.centerx, button_A10.bottom), (button_A10.centerx, button_A10.bottom + 20), 4)
        end_pos_A10 = (button_A10.centerx, button_A10.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_B10.centerx, button_B10.bottom), (button_B10.centerx, button_B10.bottom + 20), 4)
        end_pos_B10 = (button_B10.centerx, button_B10.bottom + 20)
        pygame.draw.line(screen, BLACK, end_pos_A10, rond_jaune_rect10.center, 6) 
        pygame.draw.line(screen, BLACK, end_pos_B10, rond_jaune_rect10.center, 6)  
        draw_line_to_button(rond_jaune_rect10.center, button_AB10, button_type="vertical")
        rotated_image10 = pygame.transform.rotate(rond_jaune10, math.degrees(rotation_angle10))
        rotated_rect10 = rotated_image10.get_rect(center=rond_jaune_rect10.center)
        screen.blit(rotated_image10, rotated_rect10.topleft)
        
        canal_a_rect = pygame.Rect(1060, 730, 50, 30)  
        canal_b_rect = pygame.Rect(1190, 730, 50, 30) 
        canal_a_color = GREEN if Data[39] == 1 else LIGHT_GRAY  #Remplacer par la valeur d'entrée necessaire à la place de Data[39]
        canal_b_color = GREEN if Data[40] == 1 else LIGHT_GRAY

        draw_rectangle(screen, canal_a_color, canal_a_rect, "Ch A    Actif", font_large, BLACK)
        draw_rectangle(screen, canal_b_color, canal_b_rect, "Ch B    Actif", font_large, BLACK)


    # Fenetre 11
    
        draw_text(screen, "28 VDC bougies", 290, 820, font_large)
        draw_button(button_1.x, button_1.y, button_1.width, button_1.height, LIGHT_GRAY, "1", text_color=BLACK)
        draw_button(button_12.x, button_12.y, button_12.width, button_12.height, LIGHT_GRAY, "1&2", text_color=BLACK)
        draw_button(button_2.x, button_2.y, button_2.width, button_2.height, LIGHT_GRAY, "2", text_color=BLACK)
        draw_button(button_OFF11.x, button_OFF11.y, button_OFF11.width, button_OFF11.height, LIGHT_GRAY, "OFF", text_color=BLACK)
        pygame.draw.line(screen, BLACK, (button_1.centerx, button_1.bottom), (button_1.centerx, button_1.bottom + 20), 4)
        end_pos_1 = (button_1.centerx, button_1.bottom + 20)
        pygame.draw.line(screen, BLACK, (button_2.centerx, button_2.bottom), (button_2.centerx, button_2.bottom + 20), 4)
        end_pos_2 = (button_2.centerx, button_2.bottom + 20)
        pygame.draw.line(screen, BLACK, end_pos_1, rond_jaune_rect11.center, 6)  # Ligne de A à l'image
        pygame.draw.line(screen, BLACK, end_pos_2, rond_jaune_rect11.center, 6)  # Ligne de B à l'image
        draw_line_to_button(rond_jaune_rect11.center, button_12, button_type="vertical")
        draw_line_to_button(rond_jaune_rect11.center, button_OFF11, button_type="vertical1")
        rotated_image11 = pygame.transform.rotate(rond_jaune11, math.degrees(rotation_angle11))
        rotated_rect11 = rotated_image11.get_rect(center=rond_jaune_rect11.center)
    # Afficher l'image tournée sous les boutons
        screen.blit(rotated_image11, rotated_rect11.topleft)
    
    # Fenetre 12
    
    # Fenetre 13 
       
        draw_button(780,910,220,40,Alaska_color,"Utilisation Alaska",text_color=BLACK)
    
    # Fenetre 14
    
        draw_text(screen, "Sans gycleur", 825, 975, font_large, WHITE)
    
    # Fenetre 15
   
        banc = pygame.Rect(1040, 830, 220, 40)  
        air_dem = pygame.Rect(1040, 880, 220, 40) 
        carb = pygame.Rect(1040, 930, 220, 40) 
        
        banc_color = GREEN if Data[39] == 1 else LIGHT_GRAY   #REMPLACER DATA PAR L'entrée 
        air_dem_color = GREEN if Data[40] == 1 else LIGHT_GRAY
        carb_color = GREEN if Data[40] == 1 else LIGHT_GRAY

        draw_rectangle(screen, banc_color, banc, "Banc ok", font_large, BLACK)
        draw_rectangle(screen, air_dem_color, air_dem, "Air démarrage ok", font_large, BLACK)
        draw_rectangle(screen, carb_color, carb, "Carburant ok", font_large, BLACK)



    elif selected_button:
        draw_text(screen, window_contents[selected_button], 20, 210, font_bold, BLACK)

def get_state_matrix():
    matrix = np.zeros(4)  # 4 elements: Apprch, Sol, Vol, Gauge degrees
    matrix[0] = 1 if button_states["Apprch"] else 0
    matrix[1] = 1 if button_states["Sol"] else 0
    matrix[2] = 1 if button_states["Vol"] else 0
    matrix[3] = gauge_degrees
    return matrix
# Main loop

def main():
    global draw_interface, gauge_y, gauge_dragging, selected_button, button_states, gauge_values, gauge_degrees,rotation_angle,rotation_angle9, rotation_angle10, rotation_angle11, active_CSG, active_TLA1, active_TLA2, active_TLA2, active_TLA3, CSG_color, TLA1_color, TLA2_color,TLA3_color,value_CSG,value_TLA1,value_TLA2_value_TLA3
    global value_CSG, value_TLA1,value_TLA2, value_TLA3,active_button, Alaska_color
    f=10
    running=True
    compteur=1
    i=1
    T = 1.0 / f  # Intervalle entre chaque envoi en secondes
    start_time = time.time()  # Heure de début
    next_send_time = start_time  # Heure prévue du prochain envoi
    

    

    while running:
        current_time = time.time()
        draw_interface()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                

                if event.button == 1:
                    # Événements
                    
                    if button_click(button_A, event.pos):
                        #print("Bouton 'A' cliqué")
                        # Tourner de -pi/4
                        rotation_angle = math.pi / 2.8
                    elif button_click(button_AB, event.pos):
                        #print("Bouton 'A&B' cliqué")
                        # Remettre à 0
                        rotation_angle = 0
                    elif button_click(button_B, event.pos):
                        #print("Bouton 'B' cliqué")
                        # Tourner de pi/4
                        rotation_angle = -math.pi / 2.8
                    elif button_click(button_OFF, event.pos):
                        #print("OFF")  # Afficher "OFF" dans la console
                        # Tourner de pi (180 degrés)
                        rotation_angle = math.pi
                        
                    
                    elif button_click(button_M2, event.pos):
                        rotation_angle9 = math.pi / 2.4
                        active_button = button_M2
                    elif button_click(button_M1, event.pos):
                        rotation_angle9 = math.pi / 2.8
                        active_button = button_M1
                    elif button_click(button_N, event.pos):
                        rotation_angle9 = 0
                        active_button = button_N
                    elif button_click(button_nor, event.pos):
                        rotation_angle9 = -math.pi / 2.8
                        active_button = button_nor
                    elif button_click(button_S, event.pos):
                        rotation_angle9 = -math.pi / 2.4
                        active_button = button_S
                  
                        
                        
                        
                    elif button_click(button_A10, event.pos):
                        #print("Bouton 'A' cliqué")
                        # Tourner de -pi/4
                        rotation_angle10 = math.pi / 2.8
                    elif button_click(button_AB10, event.pos):
                        #print("Bouton 'A&B' cliqué")
                        # Remettre à 0
                        rotation_angle10 = 0
                    elif button_click(button_B10, event.pos):
                        #print("Bouton 'B' cliqué")
                        # Tourner de pi/4
                        rotation_angle10 = -math.pi / 2.8
                    
                    
                      
                    elif button_click(button_1, event.pos):
                        #print("Bouton 'A' cliqué")
                        # Tourner de -pi/4
                        rotation_angle11 = math.pi / 2.8
                    elif button_click(button_12, event.pos):
                        #print("Bouton 'A&B' cliqué")
                        # Remettre à 0
                        rotation_angle11 = 0
                    elif button_click(button_2, event.pos):
                        #print("Bouton 'B' cliqué")
                        # Tourner de pi/4
                        rotation_angle11 = -math.pi / 2.8
                        
                    elif button_click(button_OFF11, event.pos):
                        #print("OFF")  # Afficher "OFF" dans la console
                        # Tourner de pi (180 degrés)
                        rotation_angle11 = math.pi

                    
                    # Check for the enter value
                   
                    if gauge_x <= event.pos[0] <= gauge_x + 60 and gauge_max_y + 10 <= event.pos[1] <= gauge_max_y + 40 :
                        active_CSG = True
                        CSG_color = LIGHT_GREEN
                    else:
                        active_CSG= False
                        CSG_color = WHITE  
                    if  gauge_x - 77 <= event.pos[0] <= gauge_x -17 and gauge_max_y + 120 <= event.pos[1] <= gauge_max_y + 150 :
                        active_TLA1 = True
                        TLA1_color = LIGHT_GREEN
                    else:
                         active_TLA1 = False
                         TLA1_color = WHITE
                    if  gauge_x - 10<= event.pos[0] <= gauge_x + 50 and gauge_max_y + 120 <= event.pos[1] <= gauge_max_y + 150 :
                        active_TLA2 = True
                        TLA2_color = LIGHT_GREEN
                    else:
                         active_TLA2 = False
                         TLA2_color = WHITE
                    if  gauge_x + 62 <= event.pos[0] <= gauge_x +122 and gauge_max_y + 120 <= event.pos[1] <= gauge_max_y + 150 :
                        active_TLA3 = True
                        TLA3_color = LIGHT_GREEN
                    else:
                         active_TLA3 = False
                         TLA3_color = WHITE
                    if 780 <= event.pos[0] <= 780 + 220 and 910 <= event.pos[1] <= 950 :
                        Alaska_color= GREEN
                    else:
                        Alaska_color= LIGHT_GRAY
                        
                   
                        
                    
                    # Check for button clicks in the header
                    for button_text, (x, y, w, h) in buttons.items():
                        if x <= event.pos[0] <= x + w and y <= event.pos[1] <= y + h:
                            selected_button = button_text

                    # Check for gauge dragging
                    if gauge_x <= event.pos[0] <= gauge_x + gauge_width and gauge_y <= event.pos[1] <= gauge_y + cursor_height:
                        gauge_dragging = True

                    # Check for approach, sol, vol button clicks
                    if button_apprch_x <= event.pos[0] <= button_apprch_x + button_width - 15 and button_y - 10 <= event.pos[1] <= button_y - 10 + button_height:
                        button_states = {key: False for key in button_states}  # Reset all buttons
                        button_states["Apprch"] = True
                    if button_sol_x - 15 <= event.pos[0] <= button_sol_x - 15 + button_width - 40 and button_y - 10 <= event.pos[1] <= button_y - 10 + button_height:
                        button_states = {key: False for key in button_states}  # Reset all buttons
                        button_states["Sol"] = True
                    if button_vol_x - 15 <= event.pos[0] <= button_vol_x - 15 + button_width - 40 and button_y - 10 <= event.pos[1] <= button_y - 10 + button_height:
                        button_states = {key: False for key in button_states}  # Reset all buttons
                        button_states["Vol"] = True

                   # Check for "+" button
                    if control_x <= event.pos[0] <= control_x + control_width and center_y - 8 <= event.pos[1] <= center_y - 8 + control_height:
                        gauge_degrees = min(43, gauge_degrees + 0.1)
                        gauge_y = degrees_to_y(gauge_degrees)

                    # Check for "-" button
                    if control_x <= event.pos[0] <= control_x + control_width and center_y + 58 <= event.pos[1] <= center_y + 58 + control_height:
                        gauge_degrees = max(0, gauge_degrees - 0.1)
                        gauge_y = degrees_to_y(gauge_degrees)
                    # Check for "Stop" button
                    if gauge_x - 50 <= event.pos[0] <= gauge_x - 50 + 180 and gauge_max_y + 50 <= event.pos[1] <= gauge_max_y + 50 + 40:
                        gauge_y = gauge_max_y  # Reset to minimum position
                        gauge_degrees = 0
                        print(f"Stop button pressed. gauge_degrees set to {gauge_degrees}°")
                    if tk_off_x<=event.pos[0]<=tk_off_x+control_width+30 and tk_off_y + 25<=event.pos[1]<=tk_off_y + 25+control_width+30:
                        gauge_y = gauge_min_y
                        gauge_degrees = 43
                    if max_rvrs_x<=event.pos[0]<=max_rvrs_x+control_width and max_rvrs_y<=event.pos[1]<=max_rvrs_y+control_width:
                        gauge_y = gauge_max_y  # Reset to minimum position
                        gauge_degrees = 0
                           
                    if gauge_x - 77 <= event.pos[0] <= gauge_x - 12 and gauge_max_y + 160 <= event.pos[1] <= gauge_max_y + 190 :
                        try:
                            new_value2 = float(value_TLA1)
                            if 0 <= new_value2 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value2
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA1 = ""  # Réinitialiser 
                    if gauge_x - 10<= event.pos[0] <= gauge_x + 70  and gauge_max_y + 160 <= event.pos[1] <= gauge_max_y + 190 :
                        try:
                            new_value3 = float(value_TLA2)
                            if 0 <= new_value3 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value3
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA2 = ""  # Réinitialiser 
                    if gauge_x + 62 <= event.pos[0] <= gauge_x + 142 and gauge_max_y + 160 <= event.pos[1] <= gauge_max_y + 190 :
                        try:
                            new_value4 = float(value_TLA3)
                            if 0 <= new_value4 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value4
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA3 = ""  # Réinitialiser 
                   
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    gauge_dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if gauge_dragging:
                    gauge_y = max(gauge_min_y, min(gauge_max_y, event.pos[1]))
                    gauge_degrees = y_to_degrees(gauge_y)
            elif event.type == pygame.KEYDOWN:
                if active_CSG:
                    if event.key == pygame.K_RETURN:  # 
                        try:
                            new_value = float(value_CSG)
                            if 0 <= new_value <= 43:  # Analyse for the enter
                                gauge_degrees = new_value
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_CSG = ""  # Réinitialiser 
                    elif event.key == pygame.K_BACKSPACE:  # delete a character
                        value_CSG = value_CSG[:-1]
                    else:  # Add a character
                        value_CSG += event.unicode
                if active_TLA1:
                    if event.key == pygame.K_RETURN:  # 
                        try:
                            new_value2 = float(value_TLA1)
                            if 0 <= new_value2 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value2
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA1 = ""  # Réinitialiser 
                    elif event.key == pygame.K_BACKSPACE:  # delete a character
                        value_TLA1 = value_TLA1[:-1]
                    else:  # Add a character
                        value_TLA1 += event.unicode
                if active_TLA2:
                    if event.key == pygame.K_RETURN:  # 
                        try:
                            new_value3 = float(value_TLA2)
                            if 0 <= new_value3 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value3
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA2 = ""  # Réinitialiser 
                    elif event.key == pygame.K_BACKSPACE:  # delete a character
                        value_TLA2 = value_TLA1[:-1]
                    else:  # Add a character
                        value_TLA2 += event.unicode
                if active_TLA3:
                    if event.key == pygame.K_RETURN:  # 
                        try:
                            new_value4 = float(value_TLA3)
                            if 0 <= new_value4 <= 43:  # Analyse for the enter
                                gauge_degrees = new_value4
                                gauge_y = degrees_to_y(gauge_degrees)
                            else:
                                print("The value is out of 0°- 43°")
                        except ValueError:
                            print("The value is not valid")
                        #value_TLA3 = ""  # Réinitialiser 
                    elif event.key == pygame.K_BACKSPACE:  # delete a character
                        value_TLA3 = value_TLA3[:-1]
                    else:  # Add a character
                        value_TLA3 += event.unicode
                    
        """# Check if 2 seconds have passed to change gauge values
        if current_time >= next_send_time:
            V=sim.moteur(Alti,Tt4,M0)
            D.put(V)
            change_gauge_values() 
        current_time = pygame.time.get_ticks()
        
        draw_interface()
        pygame.display.flip()
        print(get_state_matrix())
        
        """
        if current_time >= next_send_time:
            Data=D.get()
            Data[:4]=get_state_matrix()
            
            
            V=sim.moteur(0,Data[3]*5.52+1279,0)
            Data[4:]=V
            D.put(Data)
            
            # Création et envoi de la trame
            iena_frame = sim.trame(V)
            """
            # Configuration du socket UDP pour l'envoi en Multicast
            sockE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sockE.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)  # Portée de 1 pour le réseau local
            
            # Envoi de la trame à l'adresse de Multicast et au port spécifiés
            sockE.sendto(iena_frame, (MULTICAST_IP_DEST, PORT_DEST))
            """
            print("Trame envoyée à", MULTICAST_IP_DEST, "sur le port", PORT_DEST)
            print(compteur)
            change_gauge_values()
            compteur+=1
            

            next_send_time += T  # Programmer le prochain envoi
            

        # Attendre juste assez de temps pour ne pas consommer trop de ressources
        sleep_time = next_send_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
        draw_interface()
        pygame.display.flip()
        print(Data)
        i+=1
    
    fin=time.time()
        

    pygame.quit()
    sys.exit()
    return

if __name__ == "__main__":
    main()
