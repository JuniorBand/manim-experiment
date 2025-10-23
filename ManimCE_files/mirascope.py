from manim import *
import numpy as np

class MirascopeAnimation(Scene):
    def construct(self):
        # --- 1. CONFIGURAÇÃO DA GEOMETRIA DO MIRASCÓPIO ---
        # Baseado na sua imagem (image_07cad8.png) e pedidos:
        # - Focos dentro das suas respectivas parábolas.
        # - Mais espaço interno.
        # - Imagem virtual em cima.
        # - Vértice da parábola inferior na origem da cena (CORRIGIDO).

        # p_value: Define a distância do vértice ao foco para cada parábola.
        p_value = 2.5  # Aumentado para fazer as parábolas mais "planas" e o mirascópio maior.
        parabola_a = 1 / (4 * p_value) # a = 1 / (4 * 2.5) = 1/10 = 0.1

        # Configuração dos eixos para posicionar o mirascópio e enquadrar a animação.
        # AJUSTE CRUCIAL: y_range ajustado para que o 0 do Y esteja no centro da tela quando axes.move_to(ORIGIN).
        axes = Axes(
            x_range=[-6.5, 6.5, 1], # Mais largo para parábolas maiores.
            y_range=[-3.0, 7.0, 1], # Ajustado para que o 0 do Y esteja no centro da tela.
            x_length=13,
            y_length=10, # Altura total do y_range (7.0 - (-3.0) = 10)
            axis_config={"color": GRAY_A},
            tips=False
        ).add_coordinates()
        # Posiciona o centro do objeto axes na origem da cena.
        # Com o y_range simétrico em relação ao centro (mas não ao 0), o ponto (0,0) do axes
        # estará no centro da tela.
        axes.move_to(ORIGIN) 

        self.add(axes) # Adiciona os eixos para referência.

        # Espelho Inferior (abre para cima):
        # Vértice fixado na origem do axes (0,0), que agora estará no centro da tela.
        lower_mirror_vertex_y = 0.0 
        lower_mirror_func = lambda x: parabola_a * x**2 + lower_mirror_vertex_y
        lower_mirror = FunctionGraph(
            lower_mirror_func,
            x_range=[-5.5, 5.5], # Largura do espelho inferior.
            color=BLUE_A,
            stroke_width=5
        )
        # Foco do Espelho Inferior (F1): Onde o OBJETO (Sapo) será colocado.
        F1_pos = axes.coords_to_point(0, p_value + lower_mirror_vertex_y) # (0, 2.5)
        lower_mirror_focus = Dot(F1_pos, color=RED, radius=0.08)
        lower_focus_label = MathTex("F_1", font_size=30).next_to(lower_mirror_focus, DOWN)

        # Espelho Superior (abre para baixo):
        # Vértice posicionado para criar um bom "espaço interno" entre os espelhos.
        upper_mirror_vertex_y = 7.0 # Vértice do espelho superior elevado para mais espaço.
        upper_mirror_func = lambda x: -parabola_a * x**2 + upper_mirror_vertex_y
        upper_mirror = FunctionGraph(
            upper_mirror_func,
            x_range=[-5.5, 5.5], # Largura do espelho superior.
            color=BLUE_A,
            stroke_width=5
        )
        # Foco do Espelho Superior (F2): LOCAL DA IMAGEM VIRTUAL.
        F2_pos = axes.coords_to_point(0, upper_mirror_vertex_y - p_value) # (0, 7.0 - 2.5) = (0, 4.5)
        upper_mirror_focus = Dot(F2_pos, color=RED, radius=0.08)
        upper_focus_label = MathTex("F_2", font_size=30).next_to(upper_mirror_focus, UP)

        # Anima a criação dos elementos principais.
        self.play(Create(lower_mirror), Create(upper_mirror))
        self.play(FadeIn(lower_mirror_focus, lower_focus_label), FadeIn(upper_mirror_focus, upper_focus_label))
        self.wait(0.5)

        # --- 2. POSICIONAMENTO DO OBJETO (SAPO) ---
        # Sapo colocado no Foco F1 do espelho INFERIOR.
        frog = ImageMobject("image3.png").scale(0.18) # Tamanho do sapo reduzido.
        frog.move_to(F1_pos) # Sapo no Foco F1.
        frog.set_z_index(1) 

        self.play(FadeIn(frog))
        self.wait(1)

        # --- 3. TRAÇADO DOS RAIOS DE LUZ ---
        num_rays = 5 # Número de raios para simular.
        ray_color = YELLOW
        ray_stroke_width = 3

        # Coordenadas X de onde os raios incidem nos espelhos.
        x_coords_for_rays = np.linspace(-5.0, 5.0, num_rays) # Garante que os raios fiquem "dentro das parabolas".

        all_rays = VGroup() # Grupo para manter todos os segmentos de raios visíveis na tela.

        for x_val in x_coords_for_rays:
            # Ponto de incidência no espelho inferior para o raio atual.
            point_on_lower_mirror = axes.coords_to_point(x_val, lower_mirror_func(x_val)) 

            # Fase 1: Raio do sapo (F1) para o espelho inferior.
            ray_to_lower = Line(frog.get_center(), point_on_lower_mirror, color=ray_color, stroke_width=ray_stroke_width)
            self.play(Create(ray_to_lower), run_time=0.8)
            all_rays.add(ray_to_lower)

            # Fase 2: Raio refletido do espelho inferior (paralelo e subindo) para o espelho superior.
            point_on_upper_mirror = axes.coords_to_point(x_val, upper_mirror_func(x_val)) 
            ray_parallel_up = Line(point_on_lower_mirror, point_on_upper_mirror, color=ray_color, stroke_width=ray_stroke_width)
            self.play(Create(ray_parallel_up), run_time=0.8)
            all_rays.add(ray_parallel_up)

            # Fase 3: Raio refletido do espelho superior para o foco F2 (local da IMAGEM VIRTUAL).
            ray_to_focus_image = Line(point_on_upper_mirror, F2_pos, color=ray_color, stroke_width=ray_stroke_width)
            self.play(Create(ray_to_focus_image), run_time=0.8)
            all_rays.add(ray_to_focus_image)
            self.wait(0.2)

        self.wait(1)

        # --- 4. EXIBIÇÃO DA IMAGEM VIRTUAL (EM CIMA) ---
        virtual_frog = frog.copy().scale(0.08) # Imagem virtual é menor que o objeto original.
        virtual_frog.move_to(F2_pos) # Imagem virtual em F2 (que está "em cima").
        virtual_frog.set_z_index(2)

        image_label = Text("Imagem Virtual", font_size=30, color=WHITE).next_to(virtual_frog, UP)

        self.play(FadeIn(virtual_frog, shift=UP*0.5), Write(image_label))
        self.wait(2)

        # --- 5. LIMPEZA FINAL ---
        self.play(
            FadeOut(
                lower_mirror, upper_mirror, frog, all_rays,
                virtual_frog, image_label, axes,
                lower_mirror_focus, lower_focus_label, upper_mirror_focus, upper_focus_label
            ),
            run_time=3
        )
        self.wait(1)
