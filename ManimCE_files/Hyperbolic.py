from manim import *
import math
import numpy as np


class Hyperbolic(ThreeDScene):
    def construct(self):
        axis_config = {
        "x_range": [-5,5,1],
        "y_range": [-5,5,1],
        "z_range": [-5,5,1]
        }
        
        # Eixos 2D e hipérbole 2D
        axes2d = Axes(x_range=[-3,3,1], y_range=[-3,3,1], tips=True)
        
        # Hipérbole 2D (separada em duas partes para evitar divisão por zero)
        hyper2dr = axes2d.plot(
            lambda x: 1/x,
            x_range=[0.1, 3, 0.1],
            color=YELLOW
        )
        hyper2dl = axes2d.plot(
            lambda x: 1/x,
            x_range=[-3, -0.1, 0.1],
            color=GREEN
        )
        
        # Criar grupo com as duas partes da hipérbole
        hyper2d_group = VGroup(hyper2dr, hyper2dl)
        self.add(axes2d)
        self.play(Create(hyper2d_group))
        
        # Rotação dos eixos 2D
        self.play(axes2d.animate.rotate(-PI/2))
        self.play(Rotate(hyper2d_group, angle=-PI/2, about_point=ORIGIN))
        self.wait(2)
        
        # Eixos 3D
        axes = ThreeDAxes(**axis_config)
        labels = axes.get_axis_labels(
            Text("x-axis").scale(0.7), Text("y-axis").scale(0.45), Text("z-axis").scale(0.45)
        )
       
        # Hipérbole 3D (superfície hiperbólica)
        hyper = Surface(
            lambda u,v: np.array([u, v, u*v]), 
            u_range=[-3,3], v_range=[-3,3],
            checkerboard_colors=[BLUE_D, BLUE_E], resolution=(32, 32)
        )

        # Configuração da câmera
        self.set_camera_orientation(phi=0, theta=-PI/2, distance=8)
        self.add(labels)
        self.play(TransformMatchingShapes(axes2d, axes))

        # Movimento suave da câmera
        self.move_camera(2*PI/5, PI/5, focal_distance=8, run_time=1)
        self.renderer.camera.light_source.move_to(3*IN)
        self.begin_ambient_camera_rotation(rate=0.5, about='theta')
        
        self.wait(2)
        
        # Transformação para a superfície 3D
        self.play(Transform(hyper2d_group, hyper), run_time=6)
        self.begin_ambient_camera_rotation(rate=0.5, about='phi')
        self.wait(15)