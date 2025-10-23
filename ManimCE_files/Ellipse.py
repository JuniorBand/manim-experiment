from manim import *
import math
import numpy as np


class Ellipse(ThreeDScene):
    def construct(self):
        axis_config = {
            "x_range": [-5,5,1],
            "y_range": [-5,5,1],
            "z_range": [-5,5,1]
        }

        elli2d = ParametricFunction(lambda t: np.array([(math.cos(t))*3, (math.sin(t))*2, 0]), t_range=[0,TAU],
            color=BLUE
        )
        axes = ThreeDAxes(**axis_config)
        
        linear2dr = axes.plot(
            lambda x:  1/x,
            x_range=[-TAU,-0.001,0.001],
            color=RED,
        )
        linear2dl = axes.plot(
            lambda x:  1/x,
            x_range=[0.001,TAU,0.001],
            color=RED,
        )

        linear3dr = ParametricFunction(lambda t: np.array([
            t, 1/t, 0
            ]), color=YELLOW, t_range=[0.001,4.99, 0.001]
        )
        linear3dl = ParametricFunction(lambda t: np.array([
            t, 1/t, 0
            ]), color=YELLOW, t_range=[-4.99, -0.001, 0.001]
        )
        
        

        self.add(axes,elli2d,linear2dr,linear2dl)
        self.move_camera(2*PI/5,PI/5, focal_distance=8, run_time=1)
        self.wait(2)
        self.play(Transform(linear2dr,linear3dr),Transform(linear2dl,linear3dl))
        