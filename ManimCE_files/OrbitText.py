from manim import *

class Deformation(ThreeDScene):
    def construct(self):
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
        self.add(axes,gauss_plane)
        self.move_camera(2*PI/5,PI/5, focal_distance=8, run_time=1)
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.begin_ambient_camera_rotation(rate=0.5, about='theta')
        self.wait(8)

class OrbText(Scene):
    def construct(self):
        src = Text("Lançamento Oblíquo", color = YELLOW, font_size=60, slant=ITALIC)
        self.play(Write(src))
        self.wait(1)
        self.wait(1)
        self.play(FadeOut(src))
        
        text0 = MathTex("x = x_0 + V_0 \\cdot cos \\theta \\cdot t")
        texte = MathTex("e")
        text1 = MathTex("y = y_0 + V_0 \\cdot sin \\theta \\cdot t - \\frac{g \\cdot t^2}{2}")

        self.play(Write(text0))
        self.play(text0.animate.shift(UP*2))
        framebox1 = SurroundingRectangle(text0, buff = .1, color = BLUE)
        self.play(Create(framebox1))
        self.wait(1)
        self.play(Write(texte))
        self.play(texte.animate.shift(LEFT*5))
        
        self.play(Write(text1))
        self.play(text1.animate.shift(DOWN*2))
        framebox2 = SurroundingRectangle(text1, buff = .1, color = BLUE)
        self.play(Create(framebox2))
        self.play(texte.animate.move_to(ORIGIN))
        self.wait(1)
        textop = MathTex("t = \\frac{V_0 \\cdot cos \\theta}{x-x_0} ")
        self.play(FadeOut(framebox1))
        textop.shift(UP*2)
        framebox3 = SurroundingRectangle(textop, buff = .1, color = BLUE)
        self.play(TransformMatchingShapes(text0, textop, path_arc=PI/2), run_time=1)
        self.play(Create(framebox3))
        my_group = VGroup(textop, text1, texte)

        text2 = MathTex("y = \\frac{(x-x_0)^2 \\cdot g \\cdot \\sec^2\\theta}{2V_0} - (x-x_0) \\cdot \\tan\\theta + y_0")
        self.play(FadeOut(framebox2, framebox3))
        self.play(my_group.animate.shift(LEFT*4))

        self.play(TransformMatchingShapes(my_group, text2, path_arc=PI/2), run_time=1)
        framebox4 = SurroundingRectangle(text2, buff = .1)
        self.play(Create(framebox4))
        self.wait(2)