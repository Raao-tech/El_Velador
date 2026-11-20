"""Cargador de sprites para VELADOR (pygame / pygame-ce).

Uso:
    import pygame
    from sprites import Sprites
    pygame.init()
    pantalla = pygame.display.set_mode((960, 540))
    spr = Sprites("ruta/a/la/carpeta", escala=4)   # después de set_mode
    img = spr.get("velador_down_idle")
    anim = spr.anim("huesped_acecha")             # lista de Surfaces
"""
import json, os
import pygame


class Sprites:
    def __init__(self, carpeta=".", escala=4):
        with open(os.path.join(carpeta, "sprites.json"), encoding="utf-8") as f:
            self.meta = json.load(f)
        self.frames = {}
        for hoja in self.meta["sheets"].values():
            img = pygame.image.load(os.path.join(carpeta, hoja["file"])).convert_alpha()
            for nombre, (x, y, w, h) in hoja["frames"].items():
                sub = img.subsurface(pygame.Rect(x, y, w, h))
                self.frames[nombre] = pygame.transform.scale(sub, (w * escala, h * escala))

    def get(self, nombre):
        return self.frames[nombre]

    def anim(self, nombre):
        """Animaciones definidas en sprites.json -> lista de Surfaces."""
        pasos = self.meta["animaciones"][nombre]
        if nombre == "velador_caminar":
            raise ValueError("Usa caminar(direccion) para el velador")
        return [self.frames[p] for p in pasos]

    def caminar(self, direccion):
        """direccion: 'down' | 'up' | 'left' | 'right'"""
        return [self.frames[f"velador_{direccion}_{p}"]
                for p in self.meta["animaciones"]["velador_caminar"]]
