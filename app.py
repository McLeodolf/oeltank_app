#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Öltank Peilstab-Rechner - Streamlit Web Version MIT BILD
Gibt die Literzahl basierend auf der Peilstab-Ablesung in cm an
HINWEIS: Lege eine Datei "splash.jpg" oder "splash.png" im gleichen Verzeichnis ab!
"""
import streamlit as st
import time
import base64
from pathlib import Path

# Peiltabelle-Daten (cm -> Liter)
PEILTABELLE = {
    1: 10, 2: 28, 3: 51, 4: 79, 5: 110, 6: 144, 7: 181, 8: 223, 9: 265, 10: 291,
    11: 358, 12: 408, 13: 460, 14: 513, 15: 567, 16: 625, 17: 684, 18: 745, 19: 806, 20: 869,
    21: 934, 22: 1000, 23: 1067, 24: 1135, 25: 1206, 26: 1277, 27: 1350, 28: 1422, 29: 1496, 30: 1571,
    31: 1647, 32: 1723, 33: 1809, 34: 1883, 35: 1965, 36: 2046, 37: 2125, 38: 2210, 39: 2295, 40: 2380,
    41: 2465, 42: 2550, 43: 2635, 44: 2720, 45: 2806, 46: 2895, 47: 2980, 48: 3065, 49: 3150, 50: 3237,
    51: 3325, 52: 3413, 53: 3500, 54: 3588, 55: 3677, 56: 3765, 57: 3854, 58: 3943, 59: 4033, 60: 4122,
    61: 4212, 62: 4302, 63: 4392, 64: 4482, 65: 4572, 66: 4663, 67: 4753, 68: 4844, 69: 4936, 70: 5027,
    71: 5119, 72: 5210, 73: 5302, 74: 5394, 75: 5487, 76: 5580, 77: 5673, 78: 5766, 79: 5859, 80: 5952,
    81: 6043, 82: 6139, 83: 6233, 84: 6327, 85: 6420, 86: 6515, 87: 6610, 88: 6705, 89: 6800, 90: 6895,
    91: 6990, 92: 7085, 93: 7180, 94: 7275, 95: 7370, 96: 7465, 97: 7560, 98: 7656, 99: 7751, 100: 7847,
    101: 7943, 102: 8039, 103: 8135, 104: 8230, 105: 8327, 106: 8423, 107: 8520, 108: 8616, 109: 8713, 110: 8809,
    111: 8906, 112: 9003, 113: 9100, 114: 9197, 115: 9295, 116: 9392, 117: 9490, 118: 9588, 119: 9686, 120: 9784,
    121: 10050, 122: 10120, 123: 10210, 124: 10290, 125: 10380, 126: 10440, 127: 10530, 128: 10610, 129: 10680, 130: 10775,
    131: 10820, 132: 10900, 133: 10980, 134: 11050, 135: 11120, 136: 11200, 137: 11280, 138: 11330, 139: 11390, 140: 11465,
    141: 11510, 142: 11580, 143: 11645, 144: 11700, 145: 11755, 146: 11800, 147: 11835, 148: 11900, 149: 11955, 150: 12000,
    151: 12047, 152: 12090, 153: 12125, 154: 12150, 155: 12175, 156: 12210, 157: 12235, 158: 12255, 159: 12269, 160: 12298
}


def berechne_liter(cm_wert):
    """Berechnet Liter basierend auf cm-Wert"""
    try:
        cm = float(cm_wert)
        
        if cm < 1:
            return "error", "Jetzt hast an' Schmarrn gemacht (muss mind. 1 sein)"
        if cm > 160:
            return "error", "Jetzt hast an' Schmarrn gemacht (darf max. 160 sein)"
        
        if cm in PEILTABELLE:
            return "success", f"{PEILTABELLE[int(cm)]:,} Liter".replace(",", ".")
        
        cm_unten = int(cm)
        cm_oben = cm_unten + 1
        
        if cm_oben in PEILTABELLE and cm_unten in PEILTABELLE:
            liter_unten = PEILTABELLE[cm_unten]
            liter_oben = PEILTABELLE[cm_oben]
            anteil = cm - cm_unten
            liter = liter_unten + (liter_oben - liter_unten) * anteil
            return "warning", f"{liter:,.0f} Liter (...mit Komma...seit wann brauch mas denn so genau??)".replace(",", ".")
        
        return "error", "Den Wert ham ma aber ned in der oidn Tabelle ghabt!"
        
    except ValueError:
        return "error", "Des moan I steht aber ned aufm Peilstab!"


# Streamlit Konfiguration
st.set_page_config(
    page_title="Öltank Peilstab-Rechner",
    page_icon="🛢️",
    layout="centered"
)

# Session State initialisieren
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False
if 'splash_start_time' not in st.session_state:
    st.session_state.splash_start_time = time.time()


def find_splash_image():
    """Sucht nach splash.jpg oder splash.png"""
    for ext in ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']:
        img_path = Path(f'splash.{ext}')
        if img_path.exists():
            return str(img_path)
    return None


def get_image_base64(image_path):
    """Lädt Bild und gibt base64 Data-URL zurück"""
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = image_path.split('.')[-1].lower()
    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    return "data:" + mime + ";base64," + data


def show_splash_screen():
    """Zeigt den Splash Screen mit Ladebalken und optional Bild"""
    
    # Berechne Fortschritt
    elapsed = time.time() - st.session_state.splash_start_time
    total_duration = 8.0
    progress = min(elapsed / total_duration, 1.0)
    percentage = int(progress * 100)
    
    # CSS für Zentrierung
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Alles zentrieren */
        [data-testid="stVerticalBlock"] {
            align-items: center;
        }
        [data-testid="stImage"] {
            max-width: 450px !important;
            margin: 0 auto !important;
        }
        .splash-title {
            font-size: 32px !important;
            font-weight: bold !important;
            color: #7eb3c9 !important;
            text-align: center !important;
            margin: 20px 0 10px 0 !important;
        }
        .splash-subtitle {
            font-size: 18px !important;
            color: #ffffff !important;
            text-align: center !important;
            margin-bottom: 25px !important;
        }
        .splash-percent {
            font-size: 16px !important;
            font-weight: bold !important;
            color: #a0aec0 !important;
            text-align: center !important;
            margin-top: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Bild zentriert anzeigen
    splash_img_path = find_splash_image()
    if splash_img_path:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # ============================================================
            # BILD-GRÖSSE: width hier ändern (aktuell 400)
            # ============================================================
            st.image(splash_img_path, width=400)
    else:
        st.markdown('<div style="font-size: 90px; text-align: center;">🛢️</div>', unsafe_allow_html=True)
    
    # Titel
    st.markdown('<p class="splash-title">ÖLTANK-RECHNER</p>', unsafe_allow_html=True)
    
    # ============================================================
    # UNTERTITEL: Größe und Farbe oben im CSS bei .splash-subtitle ändern
    # ============================================================
    st.markdown('<p class="splash-subtitle">Unglaublich komplexes Umrechnungs-Tool wird geladen</p>', unsafe_allow_html=True)
    
    # Progress Bar mit Streamlit's nativer Komponente
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.progress(progress)
        st.markdown('<p class="splash-percent">' + str(percentage) + '%</p>', unsafe_allow_html=True)
    
    # Nach 8 Sekunden zur Main App wechseln
    if progress >= 1.0:
        st.session_state.splash_shown = True
        st.rerun()
    else:
        time.sleep(0.1)
        st.rerun()


def show_main_app():
    """Zeigt die Hauptanwendung"""
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #1e1e1e;
        }
        .stTextInput > div > div > input {
            font-size: 22px;
            text-align: center;
            padding: 12px;
            border: 2px solid #3498db;
            border-radius: 8px;
            background-color: #2d2d2d;
            color: #ecf0f1;
        }
        .stTextInput > div > div > input:focus {
            border-color: #2980b9;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
        }
        .big-font {
            font-size: 36px !important;
            font-weight: bold;
            text-align: center;
        }
        .input-label {
            font-size: 20px;
            font-weight: 600;
            color: #bdc3c7;
            text-align: center;
            margin-bottom: 15px;
        }
        .result-label {
            font-size: 22px;
            font-weight: 600;
            color: #bdc3c7;
            text-align: center;
            margin-bottom: 20px;
        }
        .error-emoji {
            font-size: 52px;
            text-align: center;
            animation: blink 0.5s infinite;
        }
        @keyframes blink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0.3; }
        }
        .info-box {
            background-color: rgba(52, 152, 219, 0.2);
            border-left: 4px solid #3498db;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            color: #bdc3c7;
        }
        hr {
            border-color: #3d3d3d !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # ============================================================
    # MAIN APP TITEL UND UNTERTITEL - ALLES IN EINEM ZENTRIERTEN BLOCK
    # UNTERTITEL GRÖSSE: font-size ändern (aktuell 22px)
    # UNTERTITEL FARBE: color ändern (aktuell #bdc3c7)
    # ============================================================
    st.markdown("""
        <div style="text-align: center; width: 100%;">
            <h1 style="font-size: 50px; font-weight: bold; color: #ecf0f1; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                🛢️ Öltank Peilstab-Rechner
            </h1>
            <p style="font-size: 22px; color: #bdc3c7; font-style: italic; margin-top: 0; text-align: center;">
                fia faule, aber technisch gscheide Eltern
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Input
    st.markdown('<p class="input-label">Wos auf\'m Peilstab stand da eine:</p>', unsafe_allow_html=True)
    cm_input = st.text_input("Peilstab Wert", value="", placeholder="z.B. 75", label_visibility="collapsed", key="cm_input")

    st.markdown("---")
    st.markdown('<p class="result-label">Is no inna:</p>', unsafe_allow_html=True)

    # Berechnung und Anzeige
    if cm_input:
        status, ergebnis = berechne_liter(cm_input)
        
        if status == "error":
            st.markdown('<div class="error-emoji">🚨 ⚠️ 💥</div>', unsafe_allow_html=True)
            st.markdown('<p class="big-font" style="color: #e74c3c;">' + ergebnis + '</p>', unsafe_allow_html=True)
        elif status == "warning":
            st.markdown('<div style="text-align: center; font-size: 42px;">🤔</div>', unsafe_allow_html=True)
            st.markdown('<p class="big-font" style="color: #f39c12;">' + ergebnis + '</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; font-size: 42px;">✅</div>', unsafe_allow_html=True)
            st.markdown('<p class="big-font" style="color: #27ae60;">' + ergebnis + '</p>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; font-size: 42px;">⏳</div>', unsafe_allow_html=True)
        st.markdown('<p class="big-font" style="color: #7f8c8d;">--- Liter</p>', unsafe_allow_html=True)

    # Info Text
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <div style="text-align: center; color: #ecf0f1; font-size: 15px;">
        <strong>Oben eindrong und nachad da untn schaung, wia vui no im Tank is!</strong><br>
        <em style="color: #95a5a6;">(Gültiger Bereich san Zoin vo Oans bis Hundertsechtzge)</em>
        </div>
    </div>
    """, unsafe_allow_html=True)


# MAIN: Entscheide ob Splash oder Main App
if not st.session_state.splash_shown:
    show_splash_screen()
else:
    show_main_app()