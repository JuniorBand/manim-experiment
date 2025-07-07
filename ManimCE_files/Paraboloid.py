from manim import *
import math
import numpy as np


class Paraboloid(ThreeDScene):
    def construct(self):
        axis_config = {
        "x_range": [-5,5,1],
        "y_range": [-5,5,1],
        "z_range": [-5,5,1]
        }
        axes2d = Axes(x_range=(-3,3,1), y_range=(-3,3,1), tips=True)
        parab2d = ParametricFunction(lambda t: np.array([t,t**2,0]), t_range=(-2,2,1),
            color=PINK
        )
        self.add(axes2d)
        self.play(Create(parab2d))
        def rotate(x):
            self.play(Rotate(parab2d, angle=x, 
                about_point=ORIGIN, rate_func=linear)
            )
        
        self.play(axes2d.animate.rotate(-PI/2))
        rotate(-PI/2)
        self.wait(2)
        
        axes = ThreeDAxes(**axis_config)

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
       
        parab = Surface(lambda u,v: np.array([u**2, 1*u*(math.cos(v)), 1*u*(math.sin(v))]), 
            u_range=(-3,3), v_range=(-3,3),
            checkerboard_colors=[BLUE_D, BLUE_E], resolution=(32, 32)
        )

        self.set_camera_orientation(phi=0, theta=-PI/2,distance=5)
        self.add(labels)
        self.play(TransformMatchingShapes(axes2d,axes))

        self.move_camera(2*PI/5,PI/5, focal_distance=8, run_time=1)
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.begin_ambient_camera_rotation(rate=0.5, about='theta')
        self.wait(2)
        self.play(Transform(parab2d,parab), run_time=6)
        self.move_camera(-2*PI/5,-PI/5, focal_distance=8, run_time=1)
        self.stop_ambient_camera_rotation(about='theta')
        
        # Reorientar a câmera para que o eixo x apareça como "para cima"
        self.set_camera_orientation(phi=9*PI/10, theta=-PI/4, distance=8, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.5, about='phi')
        self.begin_ambient_camera_rotation(rate=0.5, about='theta')
        
        self.wait(15)

