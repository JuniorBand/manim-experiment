from manim import *
import numpy as np
import math 

class LancOblText(Scene):
    def construct(self):
        src = Tex("Lançamento Oblíquo")
        #tar = Tex("Parábolas")
        self.play(Write(src))
        self.wait(1)
        #self.play(TransformMatchingShapes(src, tar, path_arc=PI/2))
        self.wait(1)
        self.play(FadeOut(src))
        
        text0 = Tex("$x =\; V_0 \cdot cos \theta \cdot t$")
        texte = Tex("e")
        text1 = Tex("$y =\; V_0 \cdot sin \theta \cdot t - \\frac{g \cdot t^2}{2}$")
        text = MathTex(
            "x^2= 2py",
            "(x-x_{0})^2 = 2p(y-y_{0})",
        )

        self.play(Write(text0))
        self.play(text0.animate.move_to(UP))
        framebox1 = SurroundingRectangle(text0, buff = .1)
        self.play(Create(framebox1))
        self.wait(1)
        self.play(Write(texte))
        self.play(texte.animate.move_to(LEFT*5))
    
        #self.play(FadeOut(framebox1))
        #self.play(TransformMatchingShapes(text0, text[0], path_arc=PI/2))
        self.play(Write(text1))
        self.play(text1.animate.move_to(DOWN))
        framebox2 = SurroundingRectangle(text1, buff = .1)
        self.play(Create(framebox2))
        self.wait(1)
        #self.play(TransformMatchingShapes(text[0], text[1], path_arc=PI/2))
        #self.play(text[1].animate.move_to(ORIGIN))
        #self.wait(0.5)
        #self.play(Create(framebox2))
        #self.wait(1)
        #self.play(FadeOut(text[1], framebox2))