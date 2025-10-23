from manim import *

class HelloWorld(Scene):
    def construct(self):
                
        src = Text("Parábola de Segurança", color = BLUE, font_size=60, slant=ITALIC)
        self.play(Write(src))
        self.wait(1)
        self.play(FadeOut(src))
        ja = Tex("Já sabemos que a equação do lançamento oblíquo é:").shift(UP*2)
        text0 = MathTex("y_{(x)}= -\\frac{(x-x_0)^2 \\cdot g \\cdot \\sec^2\\theta}{2V_0} - (x-x_0) \\cdot \\tan\\theta + y_0")
        self.wait(2)
        text1 =Tex("$\\sec^2\\theta = 1 + \\tan^2\\theta$ com $x_0 = 0$ e $y_0 = 0$:").next_to(ja, ORIGIN, buff=0.0)   
        complete_text2 = MathTex("y_{(x)} = -\\frac{x^2 \\cdot g \\cdot (1 + \\tan^2\\theta)}{2V_0} - x \\cdot \\tan\\theta", font_size=35).next_to(text0, ORIGIN, buff=0.0)
        
        self.play(Write(ja))
        self.play(Write(text0))
        self.wait(2)
        self.play(Transform(ja, text1))
        self.wait(1)
        self.play(TransformMatchingShapes(text0, complete_text2))
        self.wait(2)
        self.play(FadeOut(text1))

