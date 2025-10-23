from manim import *
import numpy as np
import math 

class LancOblText(Scene):
    def construct(self):
        src = Text("Lançamento Oblíquo", color = YELLOW, font_size=60, slant=ITALIC)
        self.play(Write(src))
        self.wait(1)
        self.play(FadeOut(src))
        
        # Mover equações para a direita para dar espaço à animação
        text0 = MathTex("x = x_0 + V_0 \\cdot cos \\theta \\cdot t")
        self.play(Write(text0))
        self.play(text0.animate.shift(UP*2))

        texte = MathTex("e")
        self.play(Write(texte))
        self.play(texte.animate.shift(LEFT*5))

        text1 = MathTex("y = y_0 + V_0 \\cdot sin \\theta \\cdot t - \\frac{g \\cdot t^2}{2}")
        self.play(Write(text1))
        self.play(text1.animate.shift(DOWN*2))

        self.play(texte.animate.move_to(ORIGIN)) # Ajustado para o meio
        self.wait(1)
        
        framebox1 = SurroundingRectangle(text0, buff = .1, color = BLUE)
        self.play(Create(framebox1))
        self.wait(1)
        # self.play(Write(texte)) # Já foi escrito
        # self.play(texte.animate.shift(LEFT*5)) # Já foi animado
        
        # self.play(Write(text1)) # Já foi escrito
        # self.play(text1.animate.shift(DOWN*2)) # Já foi animado
        framebox2 = SurroundingRectangle(text1, buff = .1, color = BLUE)
        self.play(Create(framebox2))
        # self.play(texte.animate.move_to(text0.get_center() - UP*0.75 + LEFT*2)) # Ajustar posição 'e' - REMOVIDO/SUBSTITUIDO
        # self.wait(1) # Já foi animado
        textop = MathTex("t = \\frac{V_0 \\cdot cos \\theta}{x-x_0} ")
        self.play(FadeOut(framebox1))
        textop.move_to(text0.get_center()) # Mover para a posição de text0
        framebox3 = SurroundingRectangle(textop, buff = .1, color = BLUE)
        self.play(TransformMatchingShapes(text0, textop, path_arc=PI/2), run_time=1)
        self.play(Create(framebox3))
        self.wait(1)
        my_group = VGroup(textop, text1, texte) # 'texte' agora está no ORIGIN

        text2 = MathTex("y = -\\frac{(x-x_0)^2 \\cdot g \\cdot \\sec^2\\theta}{2V_0} + (x-x_0) \\cdot \\tan\\theta + y_0").move_to(ORIGIN) # Equação final posicionada no ORIGIN
        self.play(FadeOut(framebox2, framebox3))
        self.play(my_group.animate.shift(LEFT * 4)) # Mover o grupo para a esquerda
        # text2.next_to(my_group, DOWN).to_edge(RIGHT, buff=1.0) # Removido, pois text2 já está no ORIGIN

        self.play(TransformMatchingShapes(my_group, text2, path_arc=PI/2), run_time=1)
        framebox4 = SurroundingRectangle(text2, buff = .1)
        self.play(Create(framebox4))
        self.wait(2)
        self.play(FadeOut(framebox4, text2))

        # --- Início da Animação do Lançamento Oblíquo ---

        # Parâmetros físicos
        v0 = 20 # Aumentado V0 para maior alcance e altura
        g = 9.8
        theta = PI/4
        vector_length_factor = 0.5 # Fator para ajustar o comprimento visual dos vetores
        dot_radius = 0.25 # Aumentado o raio da bolinha do projétil para torná-la maior

        # Eixos do plano 2D
        axes = Axes(
            x_range=[0, 50, 5], # Aumentado o x_range para acomodar a trajetória completa
            y_range=[0, 25, 5], # Aumentado o y_range para acomodar a trajetória completa
            x_length=12, # Aumentado o comprimento X
            y_length=7, # Aumentado o comprimento Y
            axis_config={
                "color": GRAY,
                "include_numbers": True # Adicionado para exibir os números nos eixos
            },
            tips=False
        ).to_edge(DOWN, buff=0.5).shift(LEFT * 0.5) # Ajustado para centralizar mais

        # Origem do lançamento
        origin_dot = Dot(axes.c2p(0, 0), color=WHITE)

        # Função da trajetória
        def trajectory_func(t):
            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2
            return axes.c2p(x, y)

        # Ponto (círculo) que segue a trajetória
        dot_projectile = Dot(trajectory_func(0), color=BLUE, radius=dot_radius) # Aumentado o raio da bolinha

        # Tracker para o tempo na trajetória
        time_tracker = ValueTracker(0)

        # Função de atualização para o ponto do projétil
        def update_dot_projectile_position(mobject):
            mobject.move_to(trajectory_func(time_tracker.get_value()))

        # Vetores Vx e Vy dinâmicos
        def get_current_vx_vector():
            x_comp = v0 * np.cos(theta)
            start_point = dot_projectile.get_center()
            end_point = axes.c2p(axes.p2c(start_point)[0] + x_comp * vector_length_factor, axes.p2c(start_point)[1])
            vec = Arrow(start_point, end_point, buff=0, color=GREEN, stroke_width=10) # Removidos os parâmetros de proporção para manter o visual de V0
            return vec

        def get_current_vy_vector():
            y_comp = v0 * np.sin(theta) - g * time_tracker.get_value()
            start_point = dot_projectile.get_center()
            end_point = axes.c2p(axes.p2c(start_point)[0], axes.p2c(start_point)[1] + y_comp * vector_length_factor)
            vec = Arrow(start_point, end_point, buff=0, color=RED, stroke_width=10) # Removidos os parâmetros de proporção para manter o visual de V0
            return vec

        vx_vector = always_redraw(get_current_vx_vector)
        vy_vector = always_redraw(get_current_vy_vector)

        # Labels dinâmicas para os vetores
        vx_label = always_redraw(lambda: MathTex("\\vec{V}_x").next_to(vx_vector.get_end(), DOWN))
        vy_label = always_redraw(lambda: MathTex("\\vec{V}_y").next_to(vy_vector.get_end(), RIGHT))

        # Mostradores de valor para Vx e Vy
        vx_value_display = always_redraw(
            lambda: MathTex(f"\\vec{{V}}_x = {v0 * np.cos(theta):.2f}", font_size=30, color=GREEN) # Cor e formato alterados para V_x
            .move_to(ORIGIN).shift(UP * 1.5 + LEFT * 1.5) # Posicionado no topo e centralizado com V0
        )
        vy_value_display = always_redraw(
            lambda: MathTex(f"\\vec{{V}}_y = {v0 * np.sin(theta) - g * time_tracker.get_value():.2f}", font_size=30, color=RED) # Cor e formato alterados para V_y
            .next_to(vx_value_display, RIGHT, buff=1.0) # Posicionado ao lado de Vx
        )

        # Frameboxes para os mostradores de valor
        vx_value_framebox = always_redraw(lambda: SurroundingRectangle(vx_value_display, buff = .1, color = YELLOW))
        vy_value_framebox = always_redraw(lambda: SurroundingRectangle(vy_value_display, buff = .1, color = YELLOW))

        # Vetor de gravidade
        gravity_vector = Arrow(ORIGIN, DOWN * 3, buff=0, color=BLUE, stroke_width=7, max_tip_length_to_length_ratio=0.3).to_edge(RIGHT, buff=0.5).set_y(0) # Posicionado na direita, no meio
        gravity_label = MathTex("\\vec{g}").next_to(gravity_vector, RIGHT) # Adicionado símbolo de vetor

        # Valor de V0 inicial
        v0_initial_value_display = MathTex(f"\\vec{{V}}_0 = {v0:.2f}", font_size=40, color=PINK).move_to(ORIGIN).shift(UP * 1.5) # Cor alterada para PINK, Posicionado no centro, um pouco para cima
        v0_initial_value_framebox = always_redraw(lambda: SurroundingRectangle(v0_initial_value_display, buff = .1, color = YELLOW)) # Framebox para V0
        
        # Vetor V0 inicial para demonstração
        v0_initial_vector = Arrow(axes.c2p(0,0), axes.c2p(v0 * np.cos(theta) * vector_length_factor, v0 * np.sin(theta) * vector_length_factor), buff=0, color=PINK, stroke_width=10).set_z_index(-1) # Cor alterada para PINK, e z_index para ficar abaixo da bolinha
        v0_initial_label = MathTex("\\vec{V}_0").next_to(v0_initial_vector.get_end(), UP+RIGHT) # Adicionado símbolo de vetor

        # Ângulo theta inicial
        angle = Angle(axes.get_x_axis(), v0_initial_vector, radius=0.5, quadrant=(1,1), color=WHITE) # Usar axes.get_x_axis() para o ângulo
        angle_label = MathTex("\\frac{\\pi}{4}").next_to(angle, RIGHT*0.5) # Alterado para o valor numérico do ângulo

        self.play(Create(axes), Create(origin_dot))
        self.add(dot_projectile) # Bolinha adicionada para aparecer desde o início
        # Removidas as animações dos vetores iniciais e ângulo

        # Animação inicial do V0
        self.play(Write(v0_initial_value_display), Create(v0_initial_value_framebox), Create(v0_initial_vector), Write(v0_initial_label), Create(angle), Write(angle_label)) # Adicionado ângulo na animação
        self.wait(2)
        self.play(FadeOut(v0_initial_value_display, v0_initial_value_framebox, v0_initial_vector, v0_initial_label, angle, angle_label)) # Adicionado FadeOut para o ângulo

        # Trajetória (parábola) que aparece conforme o ponto se move
        trajectory_path = always_redraw(
            lambda: ParametricFunction( 
                trajectory_func,
                t_range=[0, time_tracker.get_value()],
                color=YELLOW # Cor alterada para AMARELO
            )
        )

        # Atualizar a posição do círculo e os vetores Vx e Vy
        dot_projectile.add_updater(update_dot_projectile_position)

        self.add(trajectory_path, vx_vector, vy_vector, vx_label, vy_label, vx_value_display, vy_value_display, vx_value_framebox, vy_value_framebox, gravity_vector, gravity_label, dot_projectile) # Adicionado dot_projectile por último para aparecer por cima

        # Animar o lançamento até y=0
        # Calcular o tempo total de voo (t_final quando y=0)
        t_final = (2 * v0 * np.sin(theta)) / g

        # Calcular tempo até a altura máxima
        t_peak = v0 * np.sin(theta) / g

        # Animar o lançamento até a altura máxima
        self.play(time_tracker.animate.set_value(t_peak), run_time=(t_peak / t_final) * 5, rate_func=linear) # Ajustar run_time
        
        # Reta tracejada da altura máxima até o eixo Y
        max_height_point_coords = trajectory_func(t_peak) # Coordenadas do ponto de altura máxima
        dashed_line_to_y_axis = DashedLine(axes.c2p(0, axes.p2c(max_height_point_coords)[1]), max_height_point_coords, color=WHITE)
        self.play(Create(dashed_line_to_y_axis))
        
        self.wait(2) # Pausa na altura máxima

        # Animar o lançamento do pico até y=0
        self.play(time_tracker.animate.set_value(t_final), run_time=((t_final - t_peak) / t_final) * 5, rate_func=linear) # Ajustar run_time
        self.wait(1)

        # Remover updaters e objetos da animação para transição suave
        dot_projectile.remove_updater(update_dot_projectile_position)
        self.play(
            FadeOut(dot_projectile),
            FadeOut(trajectory_path),
            FadeOut(vx_vector),
            FadeOut(vy_vector),
            FadeOut(vx_label),
            FadeOut(vy_label),
            FadeOut(vx_value_display),
            FadeOut(vy_value_display),
            FadeOut(vx_value_framebox),
            FadeOut(vy_value_framebox),
            FadeOut(gravity_vector),
            FadeOut(gravity_label),
            FadeOut(dashed_line_to_y_axis), # Adicionado FadeOut para a linha tracejada
            # Removidas as linhas de FadeOut para os vetores iniciais e ângulo
            FadeOut(axes),
            FadeOut(origin_dot),
            run_time=2
        )
        self.wait(1)
        
