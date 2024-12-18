import flet as ft
from datetime import datetime, timedelta


def main(page: ft.Page):
    # Set a modern, professional theme
    page.title = "Nine2Shine - Office Exit Time Calculator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Light theme for professional look

    # Initial entry time (program start time)
    entry_time = datetime.now()

    # Function to calculate and format the exit time
    def calculate_exit_time(entry):
        exit_time = entry + timedelta(hours=9)
        return exit_time.strftime("%I:%M %p")  # Format as HH:MM AM/PM

    # Update the display for entry and exit times
    def update_time_display():
        entry_label.content.value = f"🕒 Entry Time: {entry_time.strftime('%I:%M %p')}"
        exit_label.value = f"🏁 Exit Time: {calculate_exit_time(entry_time)}"
        page.update()

    # Handle TimePicker updates
    def handle_time_picker_change(e):
        nonlocal entry_time
        selected_time = time_picker.value  # Get the new time from TimePicker
        if selected_time:
            now = datetime.now()
            entry_time = datetime.combine(now.date(), selected_time)  # Update entry time
            update_time_display()

    # TimePicker for selecting entry time
    time_picker = ft.TimePicker(
        confirm_text="Set Entry Time",
        error_invalid_text="Invalid Time",
        help_text="Select your entry time",
        on_change=handle_time_picker_change,
    )

    # Entry Time Label (clickable text)
    entry_label = ft.TextButton(
        content=ft.Text(
            f"🕒 Entry Time: {entry_time.strftime('%I:%M %p')}",
            weight=ft.FontWeight.BOLD,
            color="green",
            size=20
        ),
        on_click=lambda _: page.open(time_picker),
    )

    # Working Description Label replaced by work_icon
    work_icon = ft.Lottie(
        src='work_icon.json',  # Replace with your animation source
        reverse=False,
        animate=True
    )

    # Exit Time Label
    exit_label = ft.Text(
        f"🏁 Exit Time: {calculate_exit_time(entry_time)}",
        size=24,
        color="red",
        weight=ft.FontWeight.BOLD,
    )

    # Card Layout for the Entry and Exit Times
    info_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    entry_label,
                    ft.Divider(height=10),
                    work_icon,  # Show the work_icon here
                    ft.Divider(height=10),
                    exit_label,
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                color="lightgrey", blur_radius=8, spread_radius=2, offset=ft.Offset(0, 4)
            ),
        ),
        width=400,
    )

    # Add components to the page
    page.add(
        ft.Text(
            "⏱️ Nine2Shine - Office Exit Time Calculator",
            size=28,
            weight=ft.FontWeight.BOLD,
            color="blue",
        ),
        ft.Divider(height=20, thickness=2, color="grey"),
        info_card,
    )


# Run the app
ft.app(main, assets_dir="assets")