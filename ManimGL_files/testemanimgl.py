from manimlib import *

print('Iai')

class OpeningManimExample(Scene):
    def construct(self):
        # Add Scene
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()
        circle.add()
        square.add()

        self.wait()

        # Testing

        self.play(ShowCreation(circle))
        self.play(circle.animate.shift(2*RIGHT))
        
        

        
        # Text
        
        text = Text("Bem-vindo ao ManimGL!")
        self.play(Write(text))
        self.wait(1)
        #self.play(Rotate(square, PI / 4))    
        self.add(ThreeDAxes())
    
        
        


