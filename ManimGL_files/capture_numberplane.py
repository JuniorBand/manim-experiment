from manimlib import *
import os

class CaptureNumberPlane(Scene):
    def construct(self):
        # Criar o NumberPlane
        number_plane = NumberPlane(
            x_range=(-10, 10, 1),
            y_range=(-10, 10, 1),
            x_length=20,
            y_length=20,
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
                "stroke_opacity": 0.6,
            },
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2,
                "include_tip": True,
            }
        )
        
        # Adicionar labels nos eixos
        labels = number_plane.get_axis_labels(x_label="x", y_label="y")
        
        # Criar o grupo completo
        plane_with_labels = VGroup(number_plane, labels)
        
        # Centralizar na tela
        plane_with_labels.move_to(ORIGIN)
        
        # Adicionar à cena
        self.add(plane_with_labels)
        
        # Aguardar um pouco para garantir que tudo foi renderizado
        self.wait(0.1)

if __name__ == "__main__":
    print("Para renderizar a imagem do NumberPlane, execute:")
    print("manimgl capture_numberplane.py CaptureNumberPlane -s")
    print("Isso irá gerar uma imagem PNG na pasta media/") 