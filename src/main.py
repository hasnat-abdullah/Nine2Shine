import flet as ft
from datetime import datetime, timedelta
import asyncio

OFFICE_HOUR = 9
EMERGENCY_EXIT_HOUR = 8
EMERGENCY_EXIT_MINUTE = 30

def main(page: ft.Page):
    # Page settings
    page.window_title = "Nine2Shine"
    page.window.resizable = True
    page.window.maximizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = ft.Colors.BLUE_GREY_50  # Light background color

    # Load or set entry time
    def load_entry_time():
        stored_time = page.client_storage.get("entry_time")
        if stored_time:
            entry = datetime.strptime(stored_time, "%Y-%m-%d %H:%M:%S")
            if entry.date() == datetime.now().date():
                return entry
        return datetime.now()

    entry_time = load_entry_time()

    def save_entry_time(entry):
        page.client_storage.set("entry_time", entry.strftime("%Y-%m-%d %H:%M:%S"))

    save_entry_time(entry_time)

    # Calculate exit times
    def calculate_exit_time(entry, hours, minutes=0):
        return entry + timedelta(hours=hours, minutes=minutes)

    # Update time display
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

    # Handle time picker change
    def handle_time_picker_change(e):
        nonlocal entry_time
        selected_time = time_picker.value
        if selected_time:
            now = datetime.now()
            entry_time = datetime.combine(now.date(), selected_time)
            save_entry_time(entry_time)
            update_time_display()

    # Time Picker
    time_picker = ft.TimePicker(
        confirm_text="Set Entry Time",
        error_invalid_text="Invalid Time",
        help_text="Select your entry time",
        on_change=handle_time_picker_change,
    )

    # Entry Label (Clickable to open Time Picker)
    entry_label = ft.TextButton(
        content=ft.Text(
            f"🕒 Entry: {entry_time.strftime('%I:%M %p')}",
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_800,
            size=20,
        ),
        on_click=lambda _: set_time_picker_value_and_open(),
    )

    def set_time_picker_value_and_open():
        time_picker.value = entry_time.time()
        page.open(time_picker)

    # Exit Label
    exit_label = ft.Text(
        f"🏁 Exit: {calculate_exit_time(entry_time, OFFICE_HOUR).strftime('%I:%M %p')}",
        size=20,
        color=ft.Colors.RED_800,
        weight=ft.FontWeight.BOLD,
    )

    # Emergency Exit Label
    emergency_exit_label = ft.Text(
        f"🔥 Emergency Exit: {calculate_exit_time(entry_time, EMERGENCY_EXIT_HOUR, EMERGENCY_EXIT_MINUTE).strftime('%I:%M %p')}",
        size=18,
        color=ft.Colors.ORANGE_800,
        weight=ft.FontWeight.BOLD,
    )

    # Remaining Time Label
    remaining_label = ft.Text(
        "⏳ Remaining: Calculating..",
        size=18,
        color=ft.Colors.BLUE_800,
        weight=ft.FontWeight.BOLD,
    )

    # Emergency Remaining Time Label
    emergency_remaining_label = ft.Text(
        "⚠️ Emergency Exit in: Calculating..",
        size=18,
        color=ft.Colors.PURPLE_800,
        weight=ft.FontWeight.BOLD,
    )

    # Work Icon Animation
    work_icon = ft.Lottie(
        src="icons/work_icon.json",
        reverse=True,
        animate=True,
        width=120,
        height=120,
    )

    # Card Design
    info_card = ft.Card(
        elevation=10,
        content=ft.Container(
            content=ft.Column(
                controls=[
                    entry_label,
                    ft.Divider(height=10, color=ft.Colors.BLUE_GREY_200),
                    work_icon,
                    remaining_label,
                    emergency_remaining_label,
                    ft.Divider(height=10, color=ft.Colors.BLUE_GREY_200),
                    exit_label,
                    emergency_exit_label,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            width=400,
            height=400,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
        ),
        margin=10,
    )

    # Add card to the page
    page.add(info_card)

    # Set window size
    page.window.width = 450
    page.window.height = 500
    page.window.center()

    # Periodic update for time display
    async def periodic_update():
        while True:
            update_time_display()
            await asyncio.sleep(1)

    # Schedule the periodic_update task
    page.run_task(periodic_update)

ft.app(main, assets_dir="assets")