import os
import ctypes
import subprocess
import psutil
from PIL import ImageGrab

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    PYCAW_AVAILABLE = True
except Exception:
    PYCAW_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except Exception:
    SBC_AVAILABLE = False


def _get_audio_endpoint():
    if not PYCAW_AVAILABLE:
        return None
    try:
        device = AudioUtilities.GetSpeakers()
        if hasattr(device, "EndpointVolume"):
            return device.EndpointVolume
        interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return interface.QueryInterface(IAudioEndpointVolume)
    except Exception:
        return None



def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return "No battery detected (Desktop or AC power)."

        percent = int(battery.percent)
        is_charging = battery.power_plugged
        charging_str = "Plugged in and charging" if is_charging else "Running on battery"
        
        return f"Battery is at {percent}%. Status: {charging_str}."
    except Exception as e:
        return f"Error checking battery: {e}"


def get_system_stats():
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}% utilized."
    except Exception as e:
        return f"Error reading system statistics: {e}"


def set_volume(level_percent):
    try:
        level = max(0, min(100, int(level_percent)))
        endpoint = _get_audio_endpoint()
        if endpoint:
            scalar = level / 100.0
            endpoint.SetMasterVolumeLevelScalar(scalar, None)
            return f"Volume set to {level}%."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error setting volume: {e}"


def get_volume():
    try:
        endpoint = _get_audio_endpoint()
        if endpoint:
            current = int(round(endpoint.GetMasterVolumeLevelScalar() * 100))
            is_muted = endpoint.GetMute() == 1
            status = " (Muted)" if is_muted else ""
            return f"Current volume is {current}%{status}."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error getting volume: {e}"


def volume_up(step=10):
    try:
        endpoint = _get_audio_endpoint()
        if endpoint:
            current = endpoint.GetMasterVolumeLevelScalar() * 100
            new_level = min(100, current + int(step))
            endpoint.SetMasterVolumeLevelScalar(new_level / 100.0, None)
            return f"Volume increased to {int(new_level)}%."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error changing volume: {e}"


def volume_down(step=10):
    try:
        endpoint = _get_audio_endpoint()
        if endpoint:
            current = endpoint.GetMasterVolumeLevelScalar() * 100
            new_level = max(0, current - int(step))
            endpoint.SetMasterVolumeLevelScalar(new_level / 100.0, None)
            return f"Volume decreased to {int(new_level)}%."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error changing volume: {e}"


def mute_volume():
    try:
        endpoint = _get_audio_endpoint()
        if endpoint:
            endpoint.SetMute(1, None)
            return "System audio muted."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error muting volume: {e}"


def unmute_volume():
    try:
        endpoint = _get_audio_endpoint()
        if endpoint:
            endpoint.SetMute(0, None)
            return "System audio unmuted."
        return "Audio controller unavailable."
    except Exception as e:
        return f"Error unmuting volume: {e}"


def set_brightness(level_percent):
    if not SBC_AVAILABLE:
        return "Brightness control module unavailable."
    try:
        level = max(0, min(100, int(level_percent)))
        sbc.set_brightness(level)
        return f"Screen brightness set to {level}%."
    except Exception as e:
        return f"Error adjusting brightness: {e}"


def get_brightness():
    if not SBC_AVAILABLE:
        return "Brightness control module unavailable."
    try:
        current = sbc.get_brightness()
        val = current[0] if isinstance(current, list) else current
        return f"Screen brightness is {val}%."
    except Exception as e:
        return f"Error checking brightness: {e}"


def lock_laptop():
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Laptop screen locked successfully."
    except Exception as e:
        return f"Error locking screen: {e}"


def close_application(app_name):
    try:
        clean_name = app_name.lower().replace(".exe", "").strip()
        closed_count = 0
        for proc in psutil.process_iter(["name", "pid"]):
            try:
                proc_name = proc.info["name"].lower()
                if clean_name in proc_name:
                    proc.kill()
                    closed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if closed_count > 0:
            return f"Closed {closed_count} instances of '{app_name}'."
        return f"No running application found matching '{app_name}'."
    except Exception as e:
        return f"Error closing application: {e}"


def take_desktop_screenshot(filename="desktop_screenshot.png"):
    try:
        os.makedirs("reports", exist_ok=True)
        save_path = os.path.join("reports", filename)
        screenshot = ImageGrab.grab()
        screenshot.save(save_path)
        return f"Desktop screenshot captured and saved to '{save_path}'."
    except Exception as e:
        return f"Error capturing desktop screenshot: {e}"
