from manim import *

class Depression(ThreeDScene):
    def construct(self):

        # Subtítulo
        subtitle = Text("Criando a Depressão em 3D", font_size=40, color=WHITE).move_to(ORIGIN)
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # Fórmula da depressão
        formula = MathTex("F(x,y) = -M \\cdot \\mathrm{e}^{\\frac{-(x^2+y^2)}{r}}", font_size=40, color=WHITE).move_to(ORIGIN)
        self.play(Write(formula))
        self.wait(3)
        self.play(FadeOut(formula))

        resolution_fa = 24

        

        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_gauss(u, v):
            x = u
            y = v
            sigma, mu = 0.4, [0.0, 0.0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = -np.exp(-(d ** 2 / (2.0 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, +2],
            u_range=[-2, +2]
        )

        gauss_plane.scale(2, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.play(Create(axes), Create(gauss_plane)) # Anima a criação dos eixos e da superfície
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.begin_ambient_camera_rotation(rate=0.5, about='theta')
        self.wait(7) # Espera 5 segundos para o gráfico ser visível