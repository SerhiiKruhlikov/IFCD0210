from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal, Optional
import geocoder
import requests
import json

import config
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    """Return current coordinates using multiple methods"""

    # Список методов в порядке приоритета
    methods = [
        _get_geocoder_coordinates,  # 1. IP-based через geocoder
        _get_ipinfo_coordinates,  # 2. Резервный: ipinfo.io
    ]

    last_error = None

    for method in methods:
        try:
            coordinates = method()
            print(f"✅ Координаты получены через {method.__name__}")
            return _round_coordinates(coordinates)
        except CantGetCoordinates as e:
            last_error = e
            print(f"⚠️  Метод {method.__name__} не сработал, пробуем следующий...")
            continue
        except Exception as e:
            last_error = CantGetCoordinates(f"Unexpected error in {method.__name__}: {str(e)}")
            continue

        # Если все методы не сработали
    raise last_error or CantGetCoordinates("All methods failed to get coordinates")


def _get_geocoder_coordinates() -> Coordinates:
    """Get coordinates using geocoder library (IP-based)"""
    try:
        # Получаем по текущему IP
        g = geocoder.ip('me')

        if not g.ok or not g.latlng:
            raise CantGetCoordinates("Geocoder returned no coordinates")

        lat, lon = g.latlng

        # Валидация координат
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise CantGetCoordinates(f"Invalid coordinates from geocoder: {lat}, {lon}")

        return Coordinates(latitude=lat, longitude=lon)

    except Exception as e:
        raise CantGetCoordinates(f"Geocoder failed: {str(e)}")


def _get_ipinfo_coordinates() -> Coordinates:
    """Fallback method using ipinfo.io API"""
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        response.raise_for_status()
        data = response.json()

        loc = data.get('loc', '').split(',')
        if len(loc) != 2:
            raise CantGetCoordinates("ipinfo.io returned invalid location format")

        lat, lon = map(float, loc)
        return Coordinates(latitude=lat, longitude=lon)

    except Exception as e:
        raise CantGetCoordinates(f"ipinfo.io failed: {str(e)}")


def _get_whereami_output() -> bytes:
    """Get raw output from whereami command"""
    try:
        process = Popen(["whereami"], stdout=PIPE, stderr=PIPE)
        output, err = process.communicate(timeout=10)  # таймаут 10 секунд
        exit_code = process.returncode

        if exit_code != 0 or err:
            raise CantGetCoordinates(f"whereami command failed: {err.decode() if err else 'Unknown error'}")

        if not output:
            raise CantGetCoordinates("whereami returned empty output")

        return output

    except FileNotFoundError:
        raise CantGetCoordinates("whereami command not found")
    except Exception as e:
        raise CantGetCoordinates(f"Error running whereami: {str(e)}")


def _parse_coordinates(whereami_output: bytes) -> Coordinates:
    """Parse coordinates from whereami output"""
    try:
        output = whereami_output.decode().strip().split("\n")
    except UnicodeDecodeError:
        raise CantGetCoordinates("Failed to decode whereami output")

    # Ищем координаты в выводе
    latitude = None
    longitude = None

    for line in output:
        line_lower = line.lower().strip()

        if line_lower.startswith("latitude:"):
            try:
                latitude = float(line_lower.split(":")[1].strip())
            except (ValueError, IndexError):
                pass

        elif line_lower.startswith("longitude:"):
            try:
                longitude = float(line_lower.split(":")[1].strip())
            except (ValueError, IndexError):
                pass

    if latitude is None or longitude is None:
        raise CantGetCoordinates("Could not parse coordinates from whereami output")

    return Coordinates(latitude=latitude, longitude=longitude)


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    """Round coordinates if configured to do so"""
    if not config.USE_ROUNDED_COORDS:
        return coordinates

    return Coordinates(
        latitude=round(coordinates.latitude, 1),
        longitude=round(coordinates.longitude, 1)
    )


def get_location_info() -> dict:
    """Get detailed location information (for debugging/info)"""
    try:
        g = geocoder.ip('me')

        if not g.ok:
            return {"error": "Could not get location info"}

        info = {
            "method": "geocoder",
            "coordinates": g.latlng,
            "address": g.address,
            "city": g.city,
            "country": g.country,
            "postal": g.postal,
            "state": g.state,
            "provider": g.org,
            "ip": g.ip,
        }

        # Попробуем получить больше информации
        try:
            response = requests.get(f'https://ipapi.co/{g.ip}/json/', timeout=3)
            if response.status_code == 200:
                ipapi_data = response.json()
                info.update({
                    "timezone": ipapi_data.get("timezone"),
                    "currency": ipapi_data.get("currency"),
                    "languages": ipapi_data.get("languages"),
                    "asn": ipapi_data.get("asn"),
                })
        except:
            pass  # Дополнительная информация не критична

        return info

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    try:
        print("🔍 Получаем координаты...")
        coords = get_gps_coordinates()
        print(f"✅ Координаты: {coords.latitude}, {coords.longitude}")

        print("\n📋 Детальная информация:")
        info = get_location_info()
        for key, value in info.items():
            print(f"  {key}: {value}")

        print(f"\n🌍 Google Maps: https://maps.google.com/?q={coords.latitude},{coords.longitude}")
        print(f"🗺️  OpenStreetMap: https://www.openstreetmap.org/#map=15/{coords.latitude}/{coords.longitude}")

    except CantGetCoordinates as e:
        print(f"❌ Ошибка: {e}")
        print("\n💡 Рекомендации:")
        print("  1. Проверьте подключение к интернету")
        print("  2. Если используете whereami, подключитесь к WiFi сети")
        print("  3. Установите geocoder: pip install geocoder")
