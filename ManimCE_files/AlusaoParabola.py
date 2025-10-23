from manim import *
import numpy as np # Certifique-se de que numpy está importado

class AlusaoParabola(Scene):
    def construct(self):
        # 0. Setup inicial: Plano Cartesiano
        # Ajustando ranges para cobrir a diretriz no mesmo range X da parábola
        # e manter a "câmera mais próxima"
        axes = Axes(
            x_range=[-6, 6, 1],  # X_range ampliado para que a diretriz acompanhe a parábola
            y_range=[-2.5, 4.5, 1], # Y_range para "câmera mais próxima"
            x_length=12,        # Proporcional ao x_range
            y_length=7,         # Proporcional ao y_range
            axis_config={"color": GRAY},
            tips=False
        ).add_coordinates()

        # Desloca os eixos para cima para garantir que a diretriz esteja bem visível
        axes.shift(UP * 0.5) 

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(labels))
        self.wait(1)

        # 1. Ponto e Reta (Foco e Diretriz)
        focus_point_coords = (0, 2)
        focus_point = Dot(axes.coords_to_point(*focus_point_coords), color=RED).set_z_index(2)
        focus_label = MathTex("F", font_size=30).next_to(focus_point, UP, buff=0.1)
        
        directrix_y_coord = -2 # Coordenada Y da diretriz no sistema de eixos
        
        # Diretriz agora irá de -6 a 6 no eixo X, cobrindo o range da parábola
        directrix = Line(
            axes.coords_to_point(axes.x_range[0], directrix_y_coord), 
            axes.coords_to_point(axes.x_range[1], directrix_y_coord), 
            color=BLUE
        )
        # Posicionamento do label 'd' abaixo da diretriz
        directrix_label = MathTex("d", font_size=30).next_to(directrix, DOWN, buff=0.1) 

        self.play(FadeIn(focus_point, focus_label, directrix, directrix_label))
        self.wait(1)

        # 2. O ser bidimensional (a formiga) e a trajetória
        initial_point_coords = axes.coords_to_point(0, 0)
        
        moving_ant = ImageMobject("image2.png").scale(0.4).move_to(initial_point_coords).set_z_index(3)
        self.play(FadeIn(moving_ant))
        self.wait(2)

        # Label 'P' para a formiga (ponto genérico na parábola)
        point_p_label = MathTex("P", font_size=30).set_color(WHITE).set_z_index(4)
        point_p_label.add_updater(lambda m: m.next_to(moving_ant, UP + RIGHT, buff=0.0))
        self.add(point_p_label) # Adiciona o label à cena para que ele atualize

        # Expressão d(P, F) = d(P, d) no canto superior esquerdo, próximo ao eixo Y
        parabola_definition_text = MathTex("d(P, F) = d(P, d)", font_size=40, color=YELLOW)
        # Posiciona no canto superior esquerdo e desloca para a direita
        parabola_definition_text.to_corner(UP + LEFT).shift(RIGHT * 2.5) 
        self.play(Write(parabola_definition_text)) # Aparece quando a formiga começa a se mover
        self.wait(0.5)

        # Updater para as linhas de distância (formiga ao foco e formiga à diretriz)
        # e as pequenas marcas perpendiculares
        def get_distance_lines_and_marks():
            ant_center = moving_ant.get_center()
            current_x, _ = axes.point_to_coords(ant_center) 

            # Linha da formiga ao foco (ROSA)
            line_to_focus = Line(ant_center, focus_point.get_center(), color=PINK, stroke_width=2)
            
            # Linha da formiga à diretriz (perpendicular, VERDE)
            point_on_directrix = axes.coords_to_point(current_x, directrix_y_coord)
            line_to_directrix = Line(ant_center, point_on_directrix, color=GREEN, stroke_width=2)
            
            # --- Adicionando as pequenas retas perpendiculares ---
            mark_length = 0.2 # Comprimento da marca perpendicular
            
            # Marca para line_to_focus (ROSA)
            mid_focus = line_to_focus.get_center()
            # Pega o vetor unitário da linha e o rotaciona 90 graus para ser perpendicular
            vec_focus = line_to_focus.get_unit_vector()
            perp_vec_focus = rotate_vector(vec_focus, PI / 2) # Rotaciona por 90 graus (PI/2 radianos)
            mark_focus = Line(mid_focus - perp_vec_focus * mark_length / 2, 
                              mid_focus + perp_vec_focus * mark_length / 2, 
                              color=PINK, stroke_width=2)

            # Marca para line_to_directrix (VERDE)
            mid_directrix = line_to_directrix.get_center()
            # A linha para a diretriz é vertical, então a perpendicular é horizontal
            # Ou, de forma geral, pega o vetor unitário da linha e rotaciona
            vec_directrix = line_to_directrix.get_unit_vector()
            perp_vec_directrix = rotate_vector(vec_directrix, PI / 2)
            mark_directrix = Line(mid_directrix - perp_vec_directrix * mark_length / 2, 
                                  mid_directrix + perp_vec_directrix * mark_length / 2, 
                                  color=GREEN, stroke_width=2)

            return VGroup(line_to_focus, line_to_directrix, mark_focus, mark_directrix)

        distance_lines = always_redraw(get_distance_lines_and_marks)
        self.add(distance_lines) # Adiciona as linhas e marcas para que acompanhem a formiga

        # A trajetória (parábola) - AGORA AMARELA
        parabola_path = TracedPath(moving_ant.get_center, stroke_color=YELLOW, stroke_width=3)
        self.add(parabola_path)

        # Função da parábola: y = x^2 / (4p)
        # O foco está em (0, 2) e a diretriz em y=-2. O vértice está em (0,0).
        # A distância do vértice ao foco é p. Então p = 2.
        # Equação da parábola: x^2 = 4py => y = x^2 / (4p)
        # y = x^2 / (4 * 2) = x^2 / 8
        def func_parabola(x):
            return x**2 / 8 

        # 3. Animações de Movimento Aprimoradas

        # Animação 1: Indo para a direita (da origem até x=5.5)
        path_right = axes.plot(func_parabola, x_range=[0, 5.5]).copy()
        self.play(
            MoveAlongPath(moving_ant, path_right),
            run_time=5,
            rate_func=linear
        )
        self.wait(0.5)

        # Animação 2: Indo da direita (x=5.5) até a esquerda (x=-5.5) pela parábola
        # Primeiro, de 5.5 a 0 (invertendo o caminho de 0 a 5.5)
        path_from_right_to_origin = axes.plot(func_parabola, x_range=[0, 5.5]).copy()
        path_from_right_to_origin.reverse_points() # Agora vai de 5.5 para 0

        # Segundo, de 0 a -5.5 (invertendo o caminho de -5.5 a 0)
        path_from_origin_to_left = axes.plot(func_parabola, x_range=[-5.5, 0]).copy()
        path_from_origin_to_left.reverse_points() # Agora vai de 0 para -5.5

        # Concatenamos os dois caminhos de forma robusta em um único VMobject
        full_path_right_to_left = VMobject()
        full_path_right_to_left.set_points_as_corners(
            np.concatenate([path_from_right_to_origin.points, path_from_origin_to_left.points])
        )

        self.play(
            MoveAlongPath(moving_ant, full_path_right_to_left),
            run_time=10, # Tempo total para o trajeto completo de 5.5 a -5.5
            rate_func=linear
        )
        self.wait(0.5)

        # Animação 3: Voltando da esquerda (x=-5.5) para a origem (x=0) pela parábola
        path_back_from_left_to_origin = axes.plot(func_parabola, x_range=[-5.5, 0]).copy()
        self.play(
            MoveAlongPath(moving_ant, path_back_from_left_to_origin),
            run_time=5, # Tempo similar ao primeiro movimento
            rate_func=linear
        )
        self.wait(1)

        # Limpeza final: Fade out de todos os elementos
        self.play(
            FadeOut(moving_ant, distance_lines, parabola_path, focus_point, focus_label, 
                    directrix, directrix_label, point_p_label, parabola_definition_text,
                    axes, labels), 
            run_time=3
        )
        self.wait(1) # Pequena pausa após tudo desaparecer