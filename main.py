import flet as ft
from datetime import datetime, timedelta
import asyncio

OFFICE_HOUR = 9
EMERGENCY_EXIT_HOUR = 8
EMERGENCY_EXIT_MINUTE = 30

def main(page: ft.Page):
    page.window_title = "Nine2Shine"
    page.title = "Nine2Shine - Office Fun"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM

    # define Light mode theme
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

    # define Dark mode theme
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE)

    # Load or initialize entry time
    def load_entry_time():
        stored_time = page.client_storage.get("entry_time")
        if stored_time:
            entry = datetime.strptime(stored_time, "%Y-%m-%d %H:%M:%S")
            if entry.date() == datetime.now().date():
                return entry
        return datetime.now()

    entry_time = load_entry_time()

    # Save entry time to persistent storage
    def save_entry_time(entry):
        page.client_storage.set("entry_time", entry.strftime("%Y-%m-%d %H:%M:%S"))

    save_entry_time(entry_time)

    # Function to calculate exit times
    def calculate_exit_time(entry, hours, minutes=0):
        return entry + timedelta(hours=hours, minutes=minutes)

    # Update the display for entry, exit, emergency exit, and remaining times
    def update_time_display():
        now = datetime.now()
        exit_time = calculate_exit_time(entry_time, OFFICE_HOUR)
        emergency_exit_time = calculate_exit_time(entry_time, EMERGENCY_EXIT_HOUR, EMERGENCY_EXIT_MINUTE)
        remaining = exit_time - now
        emergency_remaining = emergency_exit_time - now

        entry_label.content.value = f"🕒 Entry: {entry_time.strftime('%I:%M %p')}"
        exit_label.value = f"🏁 Exit: {exit_time.strftime('%I:%M %p')}"
        emergency_exit_label.value = f"🔥 Emergency Exit: {emergency_exit_time.strftime('%I:%M %p')}"

        if remaining.total_seconds() > 0:
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes = remainder // 60
            remaining_label.value = f"⏳ Remaining: {hours}h {minutes}m"
        else:
            remaining_label.value = "🎉 Time's up!"

        if emergency_remaining.total_seconds() > 0:
            hours, remainder = divmod(emergency_remaining.seconds, 3600)
            minutes = remainder // 60
            emergency_remaining_label.value = f"⚠️ Emergency Exit in: {hours}h {minutes}m"
        else:
            emergency_remaining_label.value = "🚨 Emergency Exit Time Reached!"

        page.update()

    # Handle TimePicker updates
    def handle_time_picker_change(e):
        nonlocal entry_time
        selected_time = time_picker.value
        if selected_time:
            now = datetime.now()
            entry_time = datetime.combine(now.date(), selected_time)
            save_entry_time(entry_time)
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
            f"🕒 Entry: {entry_time.strftime('%I:%M %p')}",
            weight=ft.FontWeight.BOLD,
            color="green",
            size=20,
        ),
        on_click=lambda _: page.open(time_picker),
    )

    # Exit Time Labels
    exit_label = ft.Text(
        f"🏁 Exit: {calculate_exit_time(entry_time, OFFICE_HOUR).strftime('%I:%M %p')}",
        size=24,
        color="green",
        weight=ft.FontWeight.BOLD,
    )

    emergency_exit_label = ft.Text(
        f"🔥 Emergency Exit: {calculate_exit_time(entry_time, EMERGENCY_EXIT_HOUR, EMERGENCY_EXIT_MINUTE).strftime('%I:%M %p')}",
        size=22,
        color="purple",
        weight=ft.FontWeight.BOLD,
    )

    # Remaining Time Labels
    remaining_label = ft.Text(
        "⏳ Remaining: Calculating..",
        size=20,
        color="green",
        weight=ft.FontWeight.BOLD,
    )

    emergency_remaining_label = ft.Text(
        "⚠️ Emergency Exit in: Calculating..",
        size=20,
        color="purple",
        weight=ft.FontWeight.BOLD,
    )

    # Work Icon
    work_icon = ft.Lottie(
        src='icons/work_icon.json',
        reverse=True,
        animate=True,
    )

    info_container = ft.Container(
        bgcolor=ft.Colors.ON_PRIMARY,
        content=ft.Column(
            controls=[
                entry_label,
                ft.Divider(height=10),
                work_icon,
                ft.Divider(height=10),
                remaining_label,
                emergency_remaining_label,
                ft.Divider(height=10),
                exit_label,
                emergency_exit_label
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(
            color=ft.Colors.SHADOW, blur_radius=21, spread_radius=1, offset=ft.Offset(0, 4)
        ),
    )

    # Card Layout
    info_card = ft.Card(
        content=info_container,
        width=400
    )

    # Add components to the page
    page.add(info_card)

    # Periodic Update Task
    async def periodic_update():
        while True:
            update_time_display()
            await asyncio.sleep(60)  # Update every minute

    # Initial call to display the times immediately
    update_time_display()

    # Start the periodic update
    page.on_connect = lambda _: asyncio.create_task(periodic_update())


# Run the app
ft.app(main, assets_dir="assets")