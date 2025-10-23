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
        axes2d = Axes(x_range=[-5,5,1], y_range=[-5,5,1], tips=True)
        parab2d = ParametricFunction(lambda u: np.array([u,u**2]), u_range=[-TAU,TAU], v_range=[-TAU,TAU],
            checkerboard_colors=[BLUE_D, BLUE_E], resolution=(3, 3),
        )
        self.add(axes2d,parab2d)
        def rotate(x):
            self.play(Rotate(parab2d, angle=x, 
                about_point=ORIGIN, rate_func=linear)
            )
        
        self.play(axes2d.animate.rotate(-PI/2))
        rotate()
        self.wait(2)
        
        axes = ThreeDAxes(**axis_config)

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
       
        parab = Surface(lambda u,v: np.array([1*u*(np.sin(v)), 1*u*(np.cos(v)), u**2]), u_range=[-5,5], v_range=[-5,5],
            checkerboard_colors=[BLUE_D, BLUE_E], resolution=(3, 3),
        )

        self.set_camera_orientation(phi=0, theta=0,distance=3)
        self.add(labels)
        self.play(TransformMatchingShapes(axes2d,axes))

        self.move_camera(2*PI/5,PI/5, focal_distance=8, run_time=1)
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(2)
        self.play(Transform(parab2d,parab), run_time=6)
        self.wait(6)


class Hyperbolic(ThreeDScene):
    def construct(self):
        axis_config = {
        "x_range": [-5,5,1],
        "y_range": [-5,5,1],
        "z_range": [-5,5,1]
        }
        axes2d = Axes(x_range=[-5,5,1], y_range=[-5,5,1], tips=True)
        linear = axes2d.plot(
            lambda x:  x,
            color=RED,
        )

        linear3d = ParametricFunction(lambda t: np.array([
            t, t, 0
            ]), color=YELLOW, t_range=[-TAU, TAU, 0.1]
        )
        
        def rotate(x):
            self.play(Rotate(linear, angle=x, 
                about_point=ORIGIN, rate_func=smooth)
            )

        self.add(axes2d,linear)
        self.play(axes2d.animate.rotate(-PI/2))
        rotate(-PI/2)
        self.play(axes2d.animate.scale(3))

        self.wait(2)
        
        axes = ThreeDAxes(**axis_config)

        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )

        def cosh(v,u,x):
            return (np.sqrt(x)*u)*(math.exp(v)+math.exp(-v))/2
        def sinh(v,u,x):
            return (np.sqrt(x)*u)*(math.exp(v)-math.exp(-v))/2

        self.set_camera_orientation(phi=0, theta=0, distance = 8)
        self.add(labels)
        self.play(Transform(linear,linear3d,run_time=1))
        self.play(TransformMatchingShapes(axes2d,axes))
        

        self.wait(2)


        hyper = Surface(lambda u,v: np.array([
            u, v, u*v 
            ]), u_range=[-5,5], v_range=[-5,5],resolution=(15,32),
            checkerboard_colors=[BLUE_D, BLUE_E], 
        )

        self.move_camera(2*PI/5,PI/5, focal_distance=8, run_time=1)
        self.renderer.camera.light_source.move_to(3*IN) # changes the source of the light
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(2)
        self.play(Transform(linear3d,hyper), run_time=6)
        self.wait(6)