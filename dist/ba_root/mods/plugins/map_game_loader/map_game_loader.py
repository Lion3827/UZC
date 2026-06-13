# ba_meta require api 9
from __future__ import annotations

import importlib.util
import inspect
import os
import sys

import bascenev1 as bs

_BASE_DIR   = os.path.dirname(__file__)
_MAPS_DIR   = os.path.join(_BASE_DIR, "maps")
_GAMES_DIR  = os.path.join(_BASE_DIR, "games")



def _register_maps_from_file(filepath: str) -> None:
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    unique_name = f"_map_game_loader__map__{module_name}"

    try:
        spec = importlib.util.spec_from_file_location(unique_name, filepath)
        mod  = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = mod
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"[map_game_loader] error al importar mapa {module_name}: {e}")
        return

    registered = 0
    for _name, obj in inspect.getmembers(mod, inspect.isclass):
        if obj.__module__ != unique_name:
            continue
        if not issubclass(obj, bs.Map) or obj is bs.Map:
            continue
        try:
            bs.register_map(obj)
            print(f"[map_game_loader] mapa registrado: {obj.__name__}")
            registered += 1
        except Exception as e:
            print(f"[map_game_loader] error al registrar mapa {obj.__name__}: {e}")

    if registered == 0:
        print(f"[map_game_loader] advertencia: {module_name} no tiene clases bs.Map válidas")


def _load_maps() -> None:
    if not os.path.isdir(_MAPS_DIR):
        os.makedirs(_MAPS_DIR)
        print("[map_game_loader] carpeta /maps/ creada, agrega tus mapas ahí")
        return

    files = sorted(
        f for f in os.listdir(_MAPS_DIR)
        if f.endswith(".py") and not f.startswith("_")
    )

    if not files:
        print("[map_game_loader] /maps/ está vacía, no hay mapas que cargar")
        return

    print(f"[map_game_loader] cargando {len(files)} mapa(s)...")
    for filename in files:
        _register_maps_from_file(os.path.join(_MAPS_DIR, filename))



def _load_game_file(filepath: str) -> None:
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    unique_name = f"_map_game_loader__game__{module_name}"

    try:
        spec = importlib.util.spec_from_file_location(unique_name, filepath)
        mod  = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = mod
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"[map_game_loader] error al importar game {module_name}: {e}")
        return

    if hasattr(mod, "enable"):
        try:
            mod.enable()
            print(f"[map_game_loader] game habilitado: {module_name}")
        except Exception as e:
            print(f"[map_game_loader] error al habilitar {module_name}: {e}")
    else:
        print(f"[map_game_loader] game cargado (sin enable): {module_name}")


def _load_games() -> None:
    if not os.path.isdir(_GAMES_DIR):
        os.makedirs(_GAMES_DIR)
        print("[map_game_loader] carpeta /games/ creada, agrega tus minijuegos ahí")
        return

    files = sorted(
        f for f in os.listdir(_GAMES_DIR)
        if f.endswith(".py") and not f.startswith("_")
    )

    if not files:
        print("[map_game_loader] /games/ está vacía, no hay minijuegos que cargar")
        return

    print(f"[map_game_loader] cargando {len(files)} game(s)...")
    for filename in files:
        _load_game_file(os.path.join(_GAMES_DIR, filename))


def scan() -> None:
    _load_maps()
    _load_games()


enable = scan
