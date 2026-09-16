import os
import sys

STARTUP_FOLDER = os.path.join(
    os.environ.get("APPDATA", ""),
    r"Microsoft\Windows\Start Menu\Programs\Startup"
)

SHORTCUT_NAME = "AstraAssistant.vbs"


def enable_windows_startup(silent=True):
    try:
        if not os.path.exists(STARTUP_FOLDER):
            return "Windows Startup folder not found."

        dest = os.path.join(STARTUP_FOLDER, SHORTCUT_NAME)
        src = os.path.abspath(
            "startup/astra_silent.vbs" if silent else "startup/astra_launcher.bat"
        )

        with open(src, "r", encoding="utf-8") as f_src:
            content = f_src.read()

        with open(dest, "w", encoding="utf-8") as f_dst:
            f_dst.write(content)

        return f"Astra auto-start successfully enabled in: {dest}"
    except Exception as e:
        return f"Error enabling auto-start: {e}"


def disable_windows_startup():
    try:
        dest = os.path.join(STARTUP_FOLDER, SHORTCUT_NAME)
        if os.path.exists(dest):
            os.remove(dest)
            return "Astra auto-start successfully disabled."
        return "Astra was not found in Windows Startup."
    except Exception as e:
        return f"Error disabling auto-start: {e}"


def check_startup_status():
    dest = os.path.join(STARTUP_FOLDER, SHORTCUT_NAME)
    return "Enabled" if os.path.exists(dest) else "Disabled"


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "enable":
        print(enable_windows_startup())
    elif action == "disable":
        print(disable_windows_startup())
    else:
        print("Startup status:", check_startup_status())
