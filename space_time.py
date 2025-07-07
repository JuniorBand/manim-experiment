# Varniex - CodingManim 09: Parametric Surfaces
# YouTube Video: https://youtu.be/pUC5a6XNEn4

from manimlib import *
import numpy as np
import math

EARTH_DAY_TEXTURE = "C:/Users/bande/Downloads/Earth.jpg"

EARTH_NIGHT_TEXTURE = "C:/Users/bande/Downloads/Earth_night.jpg"

SUN_TEXTURE = "C:/Users/bande/Downloads/Solarsystemscope_texture_2k_sun.jpg"

MOON_TEXTURE = "C:/Users/bande/Downloads/Moon_texture.jpg"

GRID = "C:\\Users\\bande\\Manimgl_files\\media\\images\\squaresheet\\OpeningManimExample_ManimCE_v0.19.0.png"

class SpaceTimeCurvature(ThreeDScene):
    default_frame_orientation = (0, 90)

    def construct(self):
        sphere = Sphere()  

        # Adding Earth
        earth_radius = 1
        earth = TexturedSurface(
            uv_surface=sphere.scale(earth_radius),
            image_file=EARTH_DAY_TEXTURE,
            dark_image_file=EARTH_NIGHT_TEXTURE
        )
        self.add(earth)
        earth.rotate(23.5 * DEG, axis=UP)

        axis_line = rotate_vector(OUT, 23.5 * DEG, UP)

        # always_rotate(earth, 2 * DEG, axis=axis_line)
        earth.always.rotate(2 * DEG, axis=axis_line)
        
        # Introdução suave - câmera próxima da Terra
        frame = self.frame
        frame.reorient(0, 60).set_width(8)
        frame.move_to(earth.get_center())
        
        # Aguarda um pouco para mostrar a Terra
        self.wait(2)
        
        # Afasta um pouco para mostrar o contexto
        self.play(

            frame.animate.set_width(60),
            run_time=1
        )
        
        self.wait(1)

        # Adding Sun
        sun_radius = 6
        sun = TexturedSurface(
            uv_surface=sphere.scale(sun_radius), image_file=SUN_TEXTURE, 
            z_index=1
        )
        always_rotate(sun, 0.5 * DEG)
        self.add(sun)

        # adding sun glow
        glow = TrueDot(
            center=sun.get_center(),
            radius=sun_radius,
            color=YELLOW,
            glow_factor=2.5,
            z_index=2,
        )
        glow.f_always.move_to(sun.get_center)
        self.add(glow)

        # Adding Moon
        moon_radius = 0.1
        moon = TexturedSurface(
            uv_surface=sphere.scale(moon_radius), 
            image_file=MOON_TEXTURE, 
            z_index=-2
        )
        always_rotate(moon, 5 * DEG)
        self.add(moon)

        # start orbital motion
        def earth_orbit_smooth():
            t = self.time
            
            # Velocidade para completar três órbitas elípticas
            omega_elliptical = 0.628  # Três órbitas completas em ~30 segundos (2π/0.628 ≈ 10s por órbita)
            
            if t < 30:
                # Primeiros 30s: três órbitas elípticas completas
                return self.get_orbital_position(sun.get_center(), 28, 35, omega_elliptical)
            elif t < 35:
                # Transição suave para parábola (5 segundos)
                transition = (t - 30) / 5.0  # 0 a 1 em 5 segundos
                
                # Velocidade constante durante transição
                omega_parabolic = 0.3  # Velocidade muito lenta para parábola
                
                # Posição final da elipse (t=30)
                final_elliptical = self.get_orbital_position(sun.get_center(), 28, 35, omega_elliptical)
                
                # Posição da parábola no mesmo ponto
                parabolic = self.get_orbital_position2(sun.get_center(), 28, 35, omega_parabolic)
                
                # Interpolação suave
                return (1 - transition) * final_elliptical + transition * parabolic
            else:
                # Depois de 35s: órbita parabólica
                return self.get_orbital_position2(sun.get_center(), 28, 35, 0.3)
        
        earth.f_always.move_to(earth_orbit_smooth)
        
        # Adicionar rastro brilhante atrás da Terra
        earth_trail = TracingTail(earth, 50, 3, stroke_opacity=1.0, stroke_color=YELLOW)
        earth_trail.set_stroke(width=6)  # Linha mais grossa para simular glow
        
        # Rastro de glow (linha mais grossa e transparente)
        earth_trail_glow = TracingTail(earth, 50, 3, stroke_opacity=0.3, stroke_color=YELLOW)
        earth_trail_glow.set_stroke(width=12)  # Linha muito mais grossa para efeito glow
        self.add(earth_trail_glow)  # Adiciona o glow primeiro (atrás)
        self.add(earth_trail)  # Adiciona a linha principal por cima

        moon_trail = TracingTail(moon, 50, 3, stroke_opacity=1.0, stroke_color=TEAL_B)
        moon_trail.set_stroke(width=6)  # Linha mais grossa para simular glow
        
        # Rastro de glow (linha mais grossa e transparente)
        moon_trail_glow = TracingTail(moon, 50, 3, stroke_opacity=0.3, stroke_color=TEAL_B)
        moon_trail_glow.set_stroke(width=12)  # Linha muito mais grossa para efeito glow
        self.add(moon_trail_glow)  # Adiciona o glow primeiro (atrás)
        self.add(moon_trail)  # Adiciona a linha principal por cima
        
        moon.f_always.move_to(
            lambda: self.get_orbital_position(earth.get_center(), 3, 5, 3, tilt=5.5)
        )
        sun.f_always.move_to(
            lambda: self.get_orbital_position(ORIGIN, 0.1, 0.2, 0.6)
        )

        # adding plane curvature
        grid = TexturedSurface(
            ParametricSurface(
                lambda u, v: [u, v, 0], u_range=(-50, 50), v_range=(-50, 50)
            ),
            image_file=GRID,
            z_index=-99,
        ).move_to(1.5 * IN)

        grid.set_shading(reflectiveness=0.1, gloss=0.1)
        self.play(ShowCreation(grid))
        #self.wait(10)

        def update_grid_curvature(points):
            x = points[:, 0]
            y = points[:, 1]

            z_sun = self.warp_function((x, y), sun.get_center()[:2],  15, 45)
            z_earth = self.warp_function((x, y), earth.get_center()[:2], 2, 4)
            z_moon = self.warp_function((x, y), moon.get_center()[:2], 1.3, 2)



            points[:, 2] = -0.5 + z_sun + z_earth + z_moon
            return points

        grid.add_updater(lambda p: p.set_points(update_grid_curvature(p.get_points())))
        

        # Configuração da câmera para seguir a Terra
        frame.reorient(0, 50).set_width(15)
        frame.f_always.move_to(earth.get_center)
        
        # Primeira 
        #órbita elíptica - câmera próxima
        self.wait(3)

        # Segunda órbita - afasta a câmera
        self.play(
            frame.animate.set_width(70),
            run_time=3
        )

        self.play(
            frame.animate.reorient(0, 110).move_to(earth.get_center()),
            run_time=5
        )

        # Terceira órbita - movimentos mais dramáticos
        self.play(
            frame.animate.reorient(0, 60).move_to(earth.get_center() + RIGHT * 5),
            run_time=3
        )

        self.play(
            frame.animate.set_width(80),
            run_time=4
        )

        # Aguarda um pouco
        self.wait(3)
        
        # Volta para posição normal
        self.play(
            frame.animate.set_width(40),
            run_time=0.6
        )
        
        # Transição para frente da Terra (olhando para trás)
        self.play(
            frame.animate.reorient(180, 75
            ).move_to(earth.get_center() + UP * 5),
            run_time=4.5
        )

        # Aguarda o resto da animação
        self.wait(10)

    @staticmethod
    def warp_function(point, center, mass, radius):
        num = (center[0] - point[0])**2 + (center[1] - point[1])**2
        return -mass * np.exp(-num / radius)

    def get_orbital_position(self, center, a, b, omega, tilt=0):
        # I found out later that there's actually a 5 degree tilt
        # in the orbital plane of the moon that I forgot in the code.
        # So, here's the updated one!

        t = self.time
        orbit_position = rotate_vector(
            vector= np.array([a*math.cos(omega * t), b*math.sin(omega * t), 0]),
            angle=tilt * DEG,
            axis=UP,
        )
        return center + orbit_position

    def get_orbital_position2(self, center, a , b, omega, tilt=0):
        t = self.time 
        # Órbita parabólica: r = p/(1 + e*cos(theta))
        # Para simplicidade, vamos usar uma aproximação
        c = math.sqrt(abs(a**2-b**2))
        p= c/2
        y = (p/2)*(omega*t)**2
        x = p*(omega*t) + 28

        orbit_position = rotate_vector(
            vector= np.array([x, y, 0]),
            angle=tilt * DEG,
            axis=UP,
        )
        
        return center + orbit_position