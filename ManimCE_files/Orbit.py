from manim import *

class OrbitScene(Scene):
    def construct(self):

        # Título de introdução
        initial_title = Text("Órbitas", font_size=60, color=BLUE).move_to(ORIGIN)

        self.play(Write(initial_title))
        self.wait(2)
        self.play(FadeOut(initial_title))

        # Introdução da Energia Mecânica Total
        energy_title = Text("Energia Mecânica Total", font_size=40, color=WHITE).to_edge(UP, buff=0.5)
        energy_eq_k_u = MathTex("E = K + U", font_size=40).next_to(energy_title, DOWN, buff=0.5)
        energy_k = MathTex("K = \\frac{1}{2}mv^2", font_size=30).next_to(energy_eq_k_u, DOWN, buff=0.5).align_to(energy_eq_k_u, LEFT)
        energy_u = MathTex("U = -\\frac{GMm}{r}", font_size=30).next_to(energy_k, DOWN).align_to(energy_k, LEFT)
        energy_total = MathTex("E = \\frac{1}{2}mv^2 - \\frac{GMm}{r}", font_size=40).next_to(energy_u, DOWN, buff=0.7)

        self.play(Write(energy_title))
        self.play(Write(energy_eq_k_u))
        self.play(Write(energy_k), Write(energy_u))
        self.play(Write(energy_total))
        self.wait(2)
        self.play(FadeOut(energy_title, energy_eq_k_u, energy_k, energy_u, energy_total))

        # Configuração do plano 2D
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE},
        ).to_edge(LEFT, buff=0.0).shift(LEFT * 2.0) # Ajustado shift para mover ainda mais para a esquerda

        # Título para o lado das órbitas
        orbits_title = Text("Órbitas", font_size=48, color=WHITE).next_to(axes, UP, buff=0.5)

        # Órbita Circular
        circular_orbit = Circle(radius=1.5, color=WHITE).move_to(axes.c2p(0, 0))
        dot = Dot(circular_orbit.get_top(), color=RED)

        # Texto explicativo à direita
        text_title = Text("Tipos de Órbitas", font_size=48, color=WHITE).to_edge(RIGHT, buff=1.0).to_edge(UP, buff=0.5) # Ajustado buff para mover mais para a direita

        # Variável para o texto que será transformado
        # 1. Órbita Circular
        circular_line1 = MathTex("1. \\; \\text{Órbita Circular}:", font_size=32, color=YELLOW) # Aumentado fonte
        circular_line2 = MathTex("- \\; \\text{Órbita fechada e periódica}", font_size=32, color=YELLOW) # Aumentado fonte
        circular_line3 = MathTex("- \\; E < 0 \\text{ e } E = -\\frac{GMm}{2r}", font_size=32, color=YELLOW) # Aumentado fonte
        current_description_text = VGroup(circular_line1, circular_line2, circular_line3).arrange(DOWN, buff=0.3).next_to(text_title, DOWN, buff=0.5).align_to(text_title, LEFT)

        self.play(Create(axes), Write(orbits_title))
        self.play(Create(circular_orbit), Create(dot))
        self.play(Write(text_title), Write(current_description_text))
        self.play(MoveAlongPath(dot, circular_orbit), run_time=5, rate_func=linear)
        self.wait(1)

        # Transição para a Órbita Elíptica
        self.play(
            FadeOut(circular_orbit, dot),
            run_time=1
        )

        # Órbita Elíptica
        # `width` é 2*semi_eixo_maior, `height` é 2*semi_eixo_menor
        # O centro é deslocado em `c` para que um foco esteja na origem
        elliptical_orbit = Ellipse(width=6, height=5.196, color=WHITE).move_to(axes.c2p(1.5, 0))
        # Dot criado no afélio
        dot_elliptical = Dot(elliptical_orbit.get_right(), color=RED) # Ponto inicial no afélio

        # Texto explicativo para a Órbita Elíptica (objeto alvo para transformação)
        # 2. Órbita Elíptica
        elliptical_line1 = MathTex("2. \\; \\text{Órbita Elíptica}:", font_size=32, color=YELLOW) # Aumentado fonte
        elliptical_line2 = MathTex("- \\; \\text{Órbita fechada e periódica}", font_size=32, color=YELLOW) # Aumentado fonte
        elliptical_line3 = MathTex("- \\; E < 0 \\text{ e } E = -\\frac{GMm}{2a}", font_size=32, color=YELLOW) # Aumentado fonte
        elliptical_text_target = VGroup(elliptical_line1, elliptical_line2, elliptical_line3).arrange(DOWN, buff=0.3).next_to(text_title, DOWN, buff=0.5).align_to(text_title, LEFT)

        self.play(Create(elliptical_orbit), Create(dot_elliptical))
        self.play(Transform(current_description_text, elliptical_text_target))
        self.play(MoveAlongPath(dot_elliptical, elliptical_orbit), run_time=7, rate_func=linear)
        self.wait(1)

        # Transição para a Órbita Parabólica
        self.play(
            FadeOut(elliptical_orbit, dot_elliptical),
            run_time=1
        )

        # Órbita Parabólica
        parabolic_orbit = ParametricFunction(
            lambda t: axes.c2p(1.5 * t**2 - 1.5, 3 * t),  # x = p*t^2 - p, y = 2*p*t com p=1.5
            t_range=[-2.5, 2.5],
            color=WHITE,
        )
        dot_parabolic = Dot(axes.c2p(-1.5, 0), color=RED) # Ponto inicial no vértice/periélio

        # Texto explicativo para a Órbita Parabólica (objeto alvo para transformação)
        # 3. Órbita Parabólica
        parabolic_line1 = MathTex("3. \\; \\text{Órbita Parabólica}:", font_size=32, color=YELLOW) # Aumentado fonte
        parabolic_line2 = MathTex("- \\; \\text{Órbita aberta (escape)}", font_size=32, color=YELLOW) # Aumentado fonte
        parabolic_line3 = MathTex("- \\; \\text{Energia mecânica total: } E = 0", font_size=32, color=YELLOW) # Aumentado fonte
        parabolic_text_target = VGroup(parabolic_line1, parabolic_line2, parabolic_line3).arrange(DOWN, buff=0.3).next_to(text_title, DOWN, buff=0.5).align_to(text_title, LEFT)

        self.play(Create(parabolic_orbit), Create(dot_parabolic))
        self.play(Transform(current_description_text, parabolic_text_target))
        self.play(MoveAlongPath(dot_parabolic, parabolic_orbit), run_time=7, rate_func=linear)
        self.wait(1)

        # Transição para a Órbita Hiperbólica
        self.play(
            FadeOut(parabolic_orbit, dot_parabolic),
            run_time=1
        )

        # Órbita Hiperbólica
        # Foco em (0,0), vértice em (-1.5, 0), similar ao periélio
        # x = a*cosh(t) - c, y = b*sinh(t) onde a=1.5, b=2, c=2.5
        hyperbolic_orbit = ParametricFunction(
            lambda t: axes.c2p(1.5 * np.cosh(t) - 2.5, 2 * np.sinh(t)),
            t_range=[-2, 2], # Ajustar o range para ver a curva
            color=WHITE,
        )
        dot_hyperbolic = Dot(axes.c2p(-1.0, 0), color=RED) # Ponto inicial no vértice (corrigido)

        # Texto explicativo para a Órbita Hiperbólica (objeto alvo para transformação)
        # 4. Órbita Hiperbólica
        hyperbolic_line1 = MathTex("4. \\; \\text{Órbita Hiperbólica}:", font_size=32, color=YELLOW) # Aumentado fonte
        hyperbolic_line2 = MathTex("- \\; \\text{Órbita aberta (escape)}", font_size=32, color=YELLOW) # Aumentado fonte
        hyperbolic_line3 = MathTex("- \\; \\text{Energia mecânica total: } E > 0", font_size=32, color=YELLOW) # Aumentado fonte
        hyperbolic_text_target = VGroup(hyperbolic_line1, hyperbolic_line2, hyperbolic_line3).arrange(DOWN, buff=0.3).next_to(text_title, DOWN, buff=0.5).align_to(text_title, LEFT)

        self.play(Create(hyperbolic_orbit), Create(dot_hyperbolic))
        self.play(Transform(current_description_text, hyperbolic_text_target))
        self.play(MoveAlongPath(dot_hyperbolic, hyperbolic_orbit), run_time=7, rate_func=linear)
        self.wait(1)