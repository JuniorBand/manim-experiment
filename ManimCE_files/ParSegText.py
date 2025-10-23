from manim import *
import numpy as np
import math 

class ParSegText(Scene):
    def construct(self):
        src = Text("Parábola de Segurança", color = BLUE, font_size=60, slant=ITALIC)
        self.play(Write(src))
        self.wait(1)
        self.wait(1)
        self.play(FadeOut(src))
        ja = Tex ("Já sabemos que a equação da parábola é:")
        ja.shift(UP*2)
        self.play(Write(ja))
        text0 = MathTex("y = -\\frac{(x-x_0)^2 \\cdot g \\cdot \\sec^2\\theta}{2V_0} - (x-x_0) \\cdot \\tan\\theta + y_0")
        texte = MathTex("\\sec^2\\theta = 1 + \\tan^2\\theta e com x_0 = 0 e y_0 = 0:")
        text1 = MathTex("y = -\\frac{x^2 \\cdot g \\cdot (1 + \\tan^2\\theta)}{2V_0} - x \\cdot \\tan\\theta")
        text2 = MathTex("-\\frac{x_p^2 \\cdot g \\cdot m^2}{2V_0} - x_p \\cdot m + (y_p + \\frac{g \\cdot x_p^2}{2V_0})")
        
        
        self.play(Write(text0))
        self.play(text0.animate.shift(UP*2))
        framebox1 = SurroundingRectangle(text0, buff = .1, color = BLUE)
        self.play(Create(framebox1))
        self.wait(1)
        self.play(Write(texte))
        self.play(texte.animate.shift(LEFT*5))
        self.play(FadeOut(framebox1, ja))
        
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