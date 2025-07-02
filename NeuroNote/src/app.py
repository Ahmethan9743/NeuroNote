# Required libraries are imported
import flet as ft
import json
import os
import sys
import traceback
from fpdf import FPDF
from summa.summarizer import summarize
import threading

# The file name where notes will be saved
DATA_FILE = "notlar.json"

# Function that summarizes the text (with summa library)
def summarize_text(text, max_length=120, min_length=40):
    """
    Summarizes the entered text. If the summary is too short, increases the ratio.
    """
    try:
        summary = summarize(text, ratio=0.2, split=False)
        if len(summary) < min_length:
            summary = summarize(text, ratio=0.4, split=False)
        if not summary.strip():
            summary = text.split(".")[0]
        return summary.strip()
    except Exception:
        return text.split(".")[0]

# Function that reads notes and trash from file
def load_data(data_file=DATA_FILE):
    """
    Loads notes, trash, and summaries from the JSON file.
    """
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("notes", []), data.get("trash", []), data.get("summaries", [])
    return [], [], []

# Function that saves notes and trash to file
def save_data(notes, trash, summaries, data_file=DATA_FILE):
    """
    Saves notes, trash, and summaries to the JSON file.
    """
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump({"notes": notes, "trash": trash, "summaries": summaries}, f, ensure_ascii=False, indent=2)

# Main function of the application
def main(page: ft.Page):
    try:
        # Page title and theme are set
        page.title = "NeuroNote"
        page.theme_mode = ft.ThemeMode.LIGHT

        # Language state: "tr" or "en"
        lang = {"current": "en"}  # Default language is now English

        # All UI texts in both languages
        TEXTS = {
            "tr": {
                "app_title": "NeuroNote",
                "subtitle": "Yapay zekâ destekli not defteri uygulaması",
                "save": "Kaydet",
                "cancel": "İptal",
                "edit_note": "Notu Düzenle",
                "notes": "Notlarınız:",
                "export_pdf": "Notları PDF Olarak Dışa Aktar",
                "export_txt": "Notları TXT Olarak Dışa Aktar",
                "copy": "Kopyala",
                "edit": "Düzenle",
                "delete": "Çöp Kutusuna Taşı",
                "summarize": "Yapay Zekâ ile Özetle",
                "clipboard_copied": "Not panoya kopyalandı!",
                "trash": "Çöp Kutusu",
                "restore": "Geri Al",
                "delete_forever": "Kalıcı Sil",
                "no_notes_export": "Dışa aktarılacak not yok!",
                "notes_saved": "Notlar {path} olarak kaydedildi!",
                "full_note": "Notu Tam Gör",
                "record_voice": "Sesli Not Al",
                "voice_not_ready": "Sesli not alma özelliği henüz eklenmedi!",
                "summarizing": "Özetleniyor...",
                "please_wait": "Lütfen bekleyin.",
                "note_title": "Not Başlığı",
                "note_content": "Not İçeriği",
                "back": "Geri",
            },
            "en": {
                "app_title": "NeuroNote",
                "subtitle": "AI-powered note-taking application",
                "save": "Save",
                "cancel": "Cancel",
                "edit_note": "Edit Note",
                "notes": "Your Notes:",
                "export_pdf": "Export Notes as PDF",
                "export_txt": "Export Notes as TXT",
                "copy": "Copy",
                "edit": "Edit",
                "delete": "Move to Trash",
                "summarize": "Summarize with AI",
                "clipboard_copied": "Note copied to clipboard!",
                "trash": "Trash Bin",
                "restore": "Restore",
                "delete_forever": "Delete Forever",
                "no_notes_export": "No notes to export!",
                "notes_saved": "Notes saved as {path}!",
                "full_note": "View Full Note",
                "record_voice": "Record Voice Note",
                "voice_not_ready": "Voice note feature not implemented yet!",
                "summarizing": "Summarizing...",
                "please_wait": "Please wait.",
                "note_title": "Note Title",
                "note_content": "Note Content",
                "back": "Back",
            }
        }

        # Notes, trash, and summaries are loaded
        notes, trash, note_summaries = load_data()
        editing_note = None  # Reference to the note being edited
        editing_index = None # Index of the note being edited

        # Input fields and main views are created (use dynamic labels)
        title_input = ft.TextField(label=TEXTS[lang["current"]]["note_title"], expand=True, text_size=15, text_align="left", height=None)
        content_input = ft.TextField(label=TEXTS[lang["current"]]["note_content"], multiline=True, expand=True, text_size=14, text_align="left", height=None)
        notes_list = ft.ListView(expand=True, spacing=20, padding=0)
        trash_list = ft.ListView(expand=True, spacing=20, padding=0)
        main_view = ft.Column(expand=True)
        edit_view = ft.Column(expand=True)
        trash_view = ft.Column(expand=True)
        current_view = ft.Column(expand=True)

        # File picker (for export)
        file_picker = ft.FilePicker()
        page.overlay.append(file_picker)
        export_path = {"pdf": None, "txt": None}

        # Language toggle button (top right)
        def toggle_language(e):
            lang["current"] = "en" if lang["current"] == "tr" else "tr"
            # Update all labels and UI
            title_input.label = TEXTS[lang["current"]]["note_title"]
            content_input.label = TEXTS[lang["current"]]["note_content"]
            edit_title.label = TEXTS[lang["current"]]["note_title"]
            edit_content.label = TEXTS[lang["current"]]["note_content"]
            show_main_view()

        # Function that copies the note to the clipboard
        def copy_note(idx):
            """
            Copies the selected note's title and content to the clipboard.
            """
            note = notes[idx]
            text = f"{note['title']}\n{note['content']}"
            page.set_clipboard(text)
            page.snack_bar = ft.SnackBar(ft.Text(TEXTS[lang["current"]]["clipboard_copied"], size=12))
            page.snack_bar.open = True
            page.update()

        # Function that shows the note in full screen
        def show_full_note(idx):
            """
            Shows the note's title, content, and summary in full screen.
            """
            note = notes[idx]
            summary = note_summaries[idx] if idx < len(note_summaries) and note_summaries[idx] else ""
            def close_full(e=None):
                # Return to main page when exiting full screen view
                page.views.clear()
                show_main_view()
                page.update()
            # Theme colors are set
            is_dark = page.theme_mode == ft.ThemeMode.DARK
            card_bg = "#232425" if is_dark else "#f5f6fa"
            text_color = "#b0b3b8" if is_dark else "#222222"
            summary_color = "#7a8fa6" if is_dark else "#1976d2"
            # A new View is added (full screen note view)
            page.views.append(
                ft.View(
                    f"/fullnote/{idx}",
                    [
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.IconButton(icon="arrow_back", tooltip=TEXTS[lang["current"]]["back"], on_click=close_full, icon_size=22),
                                    ft.Text(note["title"], weight="bold", size=20, max_lines=2, overflow="ellipsis", expand=True, color=text_color),
                                ], alignment="spaceBetween"),
                                ft.Divider(),
                                ft.Container(
                                    content=ft.Text(note["content"], size=17, selectable=True, expand=True, color=text_color),
                                    expand=True,
                                    bgcolor=card_bg,
                                    border_radius=12,
                                    padding=20,
                                    alignment=ft.alignment.top_left,
                                ),
                                ft.Divider(),
                                ft.Text(
                                    summary if summary else "",
                                    size=15,
                                    italic=True,
                                    color=summary_color,
                                    font_family="monospace"
                                ) if summary else ft.Container(),
                            ], expand=True),
                            expand=True,
                            bgcolor=card_bg,
                            border_radius=16,
                            padding=20,
                            alignment=ft.alignment.top_center,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    bgcolor=card_bg
                )
            )
            page.update()

        # Function that summarizes the note (with AI)
        def summarize_note(idx):
            """
            Summarizes the note's title and content, saves the result.
            """
            if idx < 0 or idx >= len(notes):
                return
            note = notes[idx]
            metin = f"{note['title']}\n{note['content']}"
            # Show summarizing message to the user
            page.dialog = ft.AlertDialog(
                title=ft.Text(TEXTS[lang["current"]]["summarizing"], size=13),
                content=ft.Text(TEXTS[lang["current"]]["please_wait"], size=12),
                open=True
            )
            page.update()
            # Perform summarization in a separate thread
            def run_summary():
                summary = summarize_text(metin)
                if idx < len(note_summaries):
                    note_summaries[idx] = summary
                    save_data(notes, trash, note_summaries)
                page.dialog = None
                show_main_view()
            threading.Thread(target=run_summary).start()

        # Called when the page route changes (e.g. when exiting full screen note)
        def route_change(e):
            """
            Loads the appropriate view when the page route changes.
            """
            route = page.route
            if route.startswith("/fullnote/"):
                try:
                    idx = int(route.split("/")[-1])
                    show_full_note(idx)
                except:
                    page.go("/")
            elif route == "/":
                page.views.clear()
                show_main_view()

        # Function that creates the main page view
        def show_main_view():
            """
            Main page: note list, input boxes, and buttons.
            """
            notes_list.controls.clear()
            # Theme colors are set
            is_dark = page.theme_mode == ft.ThemeMode.DARK
            bg = "#242526" if is_dark else "#f7f8fa"           # Main background
            card_bg = "#292b2e" if is_dark else "#f0f1f5"      # Card/box background (soft contrast)
            input_bg = "#232425" if is_dark else "#ffffff"     # For input boxes (optional)
            text_color = "#e4e6eb" if is_dark else "#222222"
            summary_color = "#7a8fa6" if is_dark else "#1976d2"
            divider_color = "#393b3d" if is_dark else "#e0e0e0"
            page.bgcolor = bg

            # Notes list is created
            for idx, note in enumerate(notes):
                summary = note_summaries[idx] if idx < len(note_summaries) and note_summaries[idx] else ""
                notes_list.controls.append(
                    ft.Container(
                        bgcolor=card_bg,
                        border_radius=16,
                        padding=20,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(
                                    note["title"],
                                    weight="bold",
                                    size=16,
                                    max_lines=1,
                                    overflow="ellipsis",
                                    color=text_color,
                                    expand=True
                                ),
                                # Action buttons on the note
                                ft.IconButton(icon="visibility", tooltip=TEXTS[lang["current"]]["full_note"], on_click=lambda e, idx=idx: show_full_note(idx), icon_size=18),
                                ft.IconButton(icon="content_copy", tooltip=TEXTS[lang["current"]]["copy"], on_click=lambda e, idx=idx: copy_note(idx), icon_size=16),
                                ft.IconButton(icon="edit", tooltip=TEXTS[lang["current"]]["edit"], on_click=lambda e, idx=idx: edit_note(idx), icon_size=16),
                                ft.IconButton(icon="delete", tooltip=TEXTS[lang["current"]]["delete"], on_click=lambda e, idx=idx: move_to_trash(idx), icon_size=16),
                                ft.IconButton(icon="summarize", tooltip=TEXTS[lang["current"]]["summarize"], on_click=lambda e, idx=idx: summarize_note(idx), icon_size=16),
                            ], alignment="center", vertical_alignment="center"),
                            ft.Divider(color=divider_color),
                            ft.Text(
                                note["content"],
                                size=15,
                                selectable=True,
                                max_lines=8,
                                overflow="ellipsis",
                                color=text_color,
                                text_align="center"
                            ),
                            ft.Text(
                                summary,
                                size=13,
                                color=summary_color,
                                font_family="monospace",
                                italic=True,
                                text_align="center"
                            ) if summary else ft.Container(),
                        ], horizontal_alignment="center", spacing=10)
                    )
                )
            # Main page controls (title, input boxes, buttons, note list)
            main_view.controls = [
                ft.Row([
                    ft.Text(
                        TEXTS[lang["current"]]["app_title"],
                        style="headlineSmall",
                        size=17,
                        expand=True,
                        color=text_color
                    ),
                    ft.Text(
                        TEXTS[lang["current"]]["subtitle"],
                        size=13,
                        color=summary_color,
                        italic=True,
                        expand=True
                    ),
                    ft.IconButton(
                        icon="language",
                        tooltip="Switch Language / Dili Değiştir",
                        on_click=toggle_language,
                        icon_size=20
                    ),
                    ft.IconButton(
                        icon="brightness_6",
                        tooltip="Tema Değiştir / Toggle Theme",
                        on_click=toggle_theme,
                        icon_size=18
                    ),
                    ft.IconButton(
                        icon="delete_outline",
                        tooltip=TEXTS[lang["current"]]["trash"],
                        on_click=lambda e: show_trash_view(),
                        icon_size=18
                    ),
                ], alignment="start"),
                ft.Container(
                    content=ft.Column([
                        title_input,
                        content_input,
                        ft.Row([
                            ft.ElevatedButton(TEXTS[lang["current"]]["save"], on_click=save_note, height=32),
                            ft.IconButton(
                                icon="mic",
                                tooltip=TEXTS[lang["current"]]["record_voice"],
                                on_click=lambda e: print(TEXTS[lang["current"]]["voice_not_ready"]),
                                icon_size=22
                            ),
                            ft.Container(expand=True),
                            ft.ElevatedButton(TEXTS[lang["current"]]["export_pdf"], on_click=export_notes_pdf, height=32),
                            ft.ElevatedButton(TEXTS[lang["current"]]["export_txt"], on_click=export_notes_txt, height=32),
                        ], alignment="center"),
                    ], spacing=6),
                    padding=ft.padding.only(left=0, right=0, top=4, bottom=4),
                    margin=ft.margin.only(bottom=4),
                    bgcolor=card_bg  # Card color here!
                ),
                ft.Divider(color=divider_color),
                ft.Text(TEXTS[lang["current"]]["notes"], style="titleMedium", size=14, color=text_color),
                ft.Container(notes_list, expand=True, padding=0, bgcolor=bg),
            ]
            # Update the view
            current_view.controls = [main_view]
            page.views.clear()
            page.views.append(
                ft.View(
                    "/",  # route
                    [current_view],
                    bgcolor=bg  # background suitable for theme
                )
            )
            page.update()

        # Function that creates the trash view
        def show_trash_view():
            """
            Shows the notes in the trash and related actions.
            """
            trash_list.controls.clear()
            is_dark = page.theme_mode == ft.ThemeMode.DARK
            card_bg = "#232425" if is_dark else "#f5f6fa"
            text_color = "#b0b3b8" if is_dark else "#222222"
            summary_color = "#7a8fa6" if is_dark else "#1976d2"
            bg = "#242526" if is_dark else "#ffffff"
            page.bgcolor = bg
            for idx, note in enumerate(trash):
                trash_list.controls.append(
                    ft.Container(
                        bgcolor=card_bg,
                        border_radius=16,
                        padding=20,
                        alignment=ft.alignment.center,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(note["title"], weight="bold", size=16, max_lines=1, overflow="ellipsis", color=text_color, expand=True),
                                ft.IconButton(icon="restore_from_trash", tooltip=TEXTS[lang["current"]]["restore"], on_click=lambda e, i=idx: restore_from_trash(i), icon_size=16),
                                ft.IconButton(icon="delete_forever", tooltip=TEXTS[lang["current"]]["delete_forever"], on_click=lambda e, i=idx: delete_forever(i), icon_size=16),
                            ], alignment="center", vertical_alignment="center"),
                            ft.Divider(),
                            ft.Text(note["content"], size=14, max_lines=8, overflow="ellipsis", color=text_color, text_align="center"),
                        ], horizontal_alignment="center", spacing=10)
                    )
                )
            trash_view.controls = [
                ft.Row([
                    ft.Text(TEXTS[lang["current"]]["trash"], style="headlineSmall", size=17, expand=True, color=text_color),
                    ft.IconButton(
                        icon="arrow_back",
                        tooltip=TEXTS[lang["current"]]["back"],
                        on_click=lambda e: show_main_view(),
                        icon_size=18
                    ),
                ], alignment="start"),
                ft.Container(trash_list, expand=True, padding=0, bgcolor=bg)
            ]
            current_view.controls = [trash_view]
            page.update()

        # Theme toggle function (light/dark)
        def toggle_theme(e):
            """
            Changes the theme mode (light <-> dark).
            """
            page.theme_mode = (
                ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
            )
            show_main_view()

        # Function to save a new note
        def save_note(e):
            """
            Saves the new note and updates the main page.
            """
            if title_input.value and content_input.value:
                notes.append({"title": title_input.value, "content": content_input.value})
                note_summaries.append("")
                save_data(notes, trash, note_summaries)
                title_input.value = ""
                content_input.value = ""
                show_main_view()

        # Function to switch to note editing screen
        def edit_note(idx):
            """
            Transfers the selected note to the editing screen.
            """
            nonlocal editing_note, editing_index
            editing_note = notes[idx]
            editing_index = idx
            show_edit_view()

        # Input boxes for editing screen
        edit_title = ft.TextField(label=TEXTS[lang["current"]]["note_title"], expand=True, text_size=16)
        edit_content = ft.TextField(label=TEXTS[lang["current"]]["note_content"], multiline=True, expand=True, height=220, text_size=15)

        # Function that saves the edited note
        def save_edited_note(e):
            """
            Saves the edited note and returns to the main page.
            """
            notes[editing_index]["title"] = edit_title.value
            notes[editing_index]["content"] = edit_content.value
            note_summaries[editing_index] = ""
            save_data(notes, trash, note_summaries)
            show_main_view()

        # Function that shows the note editing screen
        def show_edit_view():
            """
            Creates the note editing screen.
            """
            edit_title.value = editing_note["title"]
            edit_content.value = editing_note["content"]
            edit_content.expand = False
            edit_content.multiline = True
            edit_content.height = None  # Automatic height

            current_view.controls = [
                ft.Row([
                    ft.Text(TEXTS[lang["current"]]["edit_note"], style="headlineSmall", size=17, expand=True),
                    ft.IconButton(
                        icon="arrow_back",
                        tooltip=TEXTS[lang["current"]]["back"],
                        on_click=lambda e: show_main_view(),
                        icon_size=18
                    ),
                ], alignment="start"),
                ft.Column(
                    [
                        edit_title,
                        edit_content,
                        ft.Row([
                            ft.ElevatedButton(TEXTS[lang["current"]]["save"], on_click=save_edited_note, height=32),
                            ft.ElevatedButton(TEXTS[lang["current"]]["cancel"], on_click=lambda e: show_main_view(), height=32),
                        ], alignment="start"),
                    ],
                    spacing=6,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                    alignment="start"
                ),
            ]
            page.update()

        # Function that moves the note to the trash
        def move_to_trash(idx, from_edit=False):
            """
            Moves the selected note to the trash.
            """
            if idx < 0 or idx >= len(notes):
                return
            trash.append(notes.pop(idx))
            note_summaries.pop(idx)
            save_data(notes, trash, note_summaries)
            show_main_view()

        # Function that restores the note from the trash
        def restore_from_trash(idx):
            """
            Restores the note from the trash.
            """
            notes.append(trash.pop(idx))
            note_summaries.append("")
            save_data(notes, trash, note_summaries)
            show_trash_view()

        # Function that permanently deletes the note
        def delete_forever(idx):
            """
            Permanently deletes the note from the trash.
            """
            trash.pop(idx)
            save_data(notes, trash, note_summaries)
            show_trash_view()

        # Function to export as PDF
        def export_notes_pdf(e):
            """
            Exports all notes as a PDF file.
            """
            if not notes:
                page.snack_bar = ft.SnackBar(ft.Text(TEXTS[lang["current"]]["no_notes_export"], size=12))
                page.snack_bar.open = True
                page.update()
                return  # clear previous result
            file_picker.on_result = on_pdf_dir_selected
            file_picker.get_directory_path()

        # Called when PDF export is completed
        def on_txt_dir_selected(e: ft.FilePickerResultEvent):
            """
            After selecting a folder for TXT export, creates the file.
            """
            if e.path:
                # SECURITY: Only allow saving inside the selected directory, prevent path traversal
                export_dir = os.path.abspath(e.path)
                if not os.path.isdir(export_dir):
                    page.snack_bar = ft.SnackBar(ft.Text("Invalid export directory!", size=12))
                    page.snack_bar.open = True
                    page.update()
                    return
                export_path["txt"] = export_dir
                out_path = os.path.join(export_dir, "notlar.txt")
                # Ensure the output path is inside the export directory
                if not out_path.startswith(export_dir):
                    page.snack_bar = ft.SnackBar(ft.Text("Export path error!", size=12))
                    page.snack_bar.open = True
                    page.update()
                    return
                with open(out_path, "w", encoding="utf-8") as f:
                    for note in notes:
                        f.write(f"{TEXTS[lang['current']]['note_title']}: {note['title']}\n")
                        f.write(f"{TEXTS[lang['current']]['note_content']}: {note['content']}\n")
                        f.write("-"*40 + "\n")
                page.snack_bar = ft.SnackBar(ft.Text(TEXTS[lang["current"]]["notes_saved"].format(path=out_path), size=12))
                page.snack_bar.open = True
                page.update()


        # Function to export as TXT
        def export_notes_txt(e):
            """
            Exports all notes as a TXT file.
            """
            if not notes:
                page.snack_bar = ft.SnackBar(ft.Text(TEXTS[lang["current"]]["no_notes_export"], size=12))
                page.snack_bar.open = True
                page.update()
                return
            file_picker.on_result = on_txt_dir_selected
            file_picker.get_directory_path()

        # Called when TXT export is completed
        def on_txt_dir_selected(e: ft.FilePickerResultEvent):
            """
            After selecting a folder for TXT export, creates the file.
            """
            if e.path:
                export_path["txt"] = e.path
                out_path = os.path.join(export_path["txt"], "notlar.txt")
                with open(out_path, "w", encoding="utf-8") as f:
                    for note in notes:
                        f.write(f"{TEXTS[lang['current']]['note_title']}: {note['title']}\n")
                        f.write(f"{TEXTS[lang['current']]['note_content']}: {note['content']}\n")
                        f.write("-"*40 + "\n")
                page.snack_bar = ft.SnackBar(ft.Text(TEXTS[lang["current"]]["notes_saved"].format(path=out_path), size=12))
                page.snack_bar.open = True
                page.update()
        # --- END OF EXPORT FUNCTIONS ---

        # Assign function to be called when page route changes
        page.on_route_change = route_change
        # Add and show the main view
        page.add(current_view)
        show_main_view()

    except Exception as e:
        # Print to console if there is an error
        print("ERROR:", e)
        traceback.print_exc()
        sys.exit(1)

# Application is
ft.app(target=main)