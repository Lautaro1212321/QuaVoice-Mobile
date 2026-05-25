import os
import threading
import flet as ft
from yt_dlp import YoutubeDL

def main(page: ft.Page):
    page.title = "QuaVoice Mobile"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK 

    # --- UI ELEMENTS ---
    titulo = ft.Text("QuaVoice", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    subtitulo = ft.Text("Descarga música directo a tu celular", size=14, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
    
    entry_link = ft.TextField(
        label="Enlace de YouTube",
        hint_text="Pega el link acá...",
        width=360,
        border_radius=10
    )
    
    lbl_estado = ft.Text("Estado: Esperando enlace...", size=12, weight=ft.FontWeight.W_500)
    
    txt_resultado = ft.TextField(
        label="Información de Descarga",
        multiline=True,
        read_only=True,
        min_lines=6,
        max_lines=8,
        width=360,
        text_size=12,
        border_radius=10
    )
    
    loading_icon = ft.ProgressRing(visible=False)

    def actualizar_interfaz():
        page.update()

    def procesar_video_hilo(url_video):
        # En Android, esto creará una carpeta interna de la app para las descargas
        carpeta_descargas = "Descargas"
        if not os.path.exists(carpeta_descargas):
            os.makedirs(carpeta_descargas)

        try:
            lbl_estado.value = "Estado: ⏳ Descargando audio en el celular..."
            actualizar_interfaz()

            # Configuración limpia sin depender de FFmpeg.exe
            opciones = {
                'format': 'bestaudio[ext=m4a]/bestaudio', # Descarga el m4a nativo de YouTube
                'outtmpl': os.path.join(carpeta_descargas, '%(title)s.%(ext)s'),
                'quiet': True
            }
            
            with YoutubeDL(opciones) as ydl:
                info_dict = ydl.extract_info(url_video, download=True)
                nombre_cancion = info_dict.get('title', 'Audio')
                ext = info_dict.get('ext', 'm4a')
                ruta_final = os.path.join(carpeta_descargas, f"{nombre_cancion}.{ext}")

            txt_resultado.value = f"🎵 ¡Descarga Completada en tu Móvil!\n\n📂 Archivo: {nombre_cancion}.{ext}\n📍 Guardado localmente en la app."
            lbl_estado.value = "Estado: ✅ ¡Proceso completado!"

        except Exception as e:
            lbl_estado.value = "Estado: ❌ Ocurrió un error"
            txt_resultado.value = f"[Error]: {e}"
        finally:
            loading_icon.visible = False
            btn_iniciar.disabled = False
            actualizar_interfaz()

    def comenzar_proceso(e):
        url = entry_link.value.strip()
        if not url:
            lbl_estado.value = "Estado: ❌ ¡Ingresa un link!"
            actualizar_interfaz()
            return
        
        btn_iniciar.disabled = True
        loading_icon.visible = True
        txt_resultado.value = ""
        lbl_estado.value = "Estado: Iniciando descarga..."
        actualizar_interfaz()
        
        threading.Thread(target=procesar_video_hilo, args=(url,), daemon=True).start()

    btn_iniciar = ft.ElevatedButton(
        content=ft.Text("Descargar en mi Celular", weight=ft.FontWeight.BOLD),
        on_click=comenzar_proceso,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        width=220
    )

    page.add(
        ft.Container(height=20), 
        titulo,
        subtitulo,
        ft.Container(height=20), 
        entry_link,
        btn_iniciar,
        loading_icon,
        lbl_estado,
        txt_resultado
    )

# Volvemos al modo de app nativa estándar
ft.app(target=main)
