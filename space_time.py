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
        self.wait(10)

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
            glow_factor=1.5,
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
        earth.f_always.move_to(
            lambda: self.get_orbital_position(sun.get_center(), 25, 0.5, 0.1)
        )
        moon.f_always.move_to(
            lambda: self.get_orbital_position(earth.get_center(), 3, 5.15, 1)
        )
        sun.f_always.move_to(
            lambda: self.get_orbital_position(sun.get_center(), 0, 7.5, 0)
        )

        # adding plane curvature
        grid = TexturedSurface(
            ParametricSurface(
                lambda u, v: [u, v, 0], u_range=(-40, 40), v_range=(-40, 40)
            ),
            image_file=GRID,
            z_index=-99,
        ).move_to(1.5 * IN)

        grid.set_shading(reflectiveness=0.1, gloss=0.1)
        self.play(ShowCreation(grid))
        self.wait(10)

        def update_grid_curvature(points):
            x = points[:, 0]
            y = points[:, 1]

            z_sun = self.warp_function((x, y), sun.get_center()[:2],  15, 45)
            z_earth = self.warp_function((x, y), earth.get_center()[:2], 2, 4)
            z_moon = self.warp_function((x, y), moon.get_center()[:2], 1.3, 2)



            points[:, 2] = -0.5 + z_sun + z_earth + z_moon
            return points

        grid.add_updater(lambda p: p.set_points(update_grid_curvature(p.get_points())))
        

        # frame following the earth
        frame = self.frame
        frame.reorient(0, 60).set_width(10)
        frame.f_always.move_to(earth.get_center)
        frame.f_always.set_theta(lambda: angle_of_vector(earth.get_center()) + PI / 8)
          
        self.wait(60)

    @staticmethod
    def warp_function(point, center, mass, radius):
        num = (center[0] - point[0])**2 + (center[1] - point[1])**2
        return -mass * np.exp(-num / radius)

    def get_orbital_position(self, center, radius, omega, tilt=0):
        # I found out later that there's actually a 5 degree tilt
        # in the orbital plane of the moon that I forgot in the code.
        # So, here's the updated one!

        t = self.time
        orbit_position = rotate_vector(
            vector=radius * np.array([math.cos(omega * t), math.sin(omega * t), 0]),
            angle=tilt * DEG,
            axis=UP,
        )
        return center + orbit_position