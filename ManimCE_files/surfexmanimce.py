from manim import *
import numpy as np

class SurfaceExample(ThreeDScene):
    def construct(self):
        # Texto
        surface_text = Text("Para cenas 3D, tente usar superfícies")
        surface_text.to_edge(UP)
        self.add(surface_text)

        self.wait(0.1)

        # Superfícies
        torus1 = Surface(
            lambda u, v: np.array([
                (1 + 0.5 * np.cos(v)) * np.cos(u),
                (1 + 0.5 * np.cos(v)) * np.sin(u),
                0.5 * np.sin(v)
            ]),
            u_range=[0, TAU], v_range=[0, TAU],
            resolution=(20, 20),
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        torus2 = Surface(
            lambda u, v: np.array([
                (3 + 0.5 * np.cos(v)) * np.cos(u),
                (3 + 0.5 * np.cos(v)) * np.sin(u),
                0.5 * np.sin(v)
            ]),
            u_range=[0, TAU], v_range=[0, TAU],
            resolution=(20, 20),
            checkerboard_colors=[RED_D, RED_E]
        )
        sphere = Surface(
            lambda u, v: np.array([
                3 * np.cos(u) * np.sin(v),
                3 * np.sin(u) * np.sin(v),
                3 * np.cos(v)
            ]),
            u_range=[0, TAU], v_range=[0, PI],
            resolution=(20, 20),
            checkerboard_colors=[GREEN_D, GREEN_E]
        )

        surfaces = [sphere, torus1, torus2]
        for mob in surfaces:
            mob.shift(IN)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES, distance=10)
        surface = surfaces[0]

        self.play(FadeIn(surface), run_time=1)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)
        self.play(Transform(surface, surfaces[1]), run_time=3)
        self.play(Transform(surface, surfaces[2]), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.1, about='theta')

        # Texto sobre a fonte de luz
        light_text = Text("Você pode mover a fonte de luz")
        light_text.move_to(surface_text)
        self.play(Transform(surface_text, light_text))
        self.renderer.camera.light_source.move_to(3 * IN)
        self.wait(2)
        self.renderer.camera.light_source.move_to(3 * OUT)
        self.wait(2)

        # Texto final
        drag_text = Text("Tente mover o mouse enquanto pressiona d ou s")
        drag_text.move_to(light_text)
        self.play(Transform(light_text, drag_text))
        self.wait(3)
        self.stop_ambient_camera_rotation() 