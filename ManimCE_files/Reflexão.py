from manim import *
import numpy as np
import math 

class ParabolicReflector(Scene):
    def construct(self):
        src = Text("Reflexão", color = BLUE_A, font_size=60, slant=ITALIC)
        self.play(Write(src))
        self.wait(1)
        self.play(FadeOut(src))

        # 1. Setup Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=6,
            axis_config={"color": GREY},
            tips=False
        ).add_coordinates()
        self.add(axes)

        # 2. Define the horizontal parabola (x = 0.5 * y^2)
        parabola_a = 0.5 
        focus_val = 1 / (4 * parabola_a) # Focus at (0.5, 0)
        directrix_x = -focus_val         # Directrix at x = -0.5

        parabola = ParametricFunction(
            lambda t: axes.coords_to_point(parabola_a * t**2, t),
            t_range=[-2.5, 2.5, 0.01],
            color=BLUE,
            stroke_width=4
        )
        self.play(Create(parabola), run_time=2)
        self.wait(0.5)

        # 3. Add Focus and Directrix
        focus_point_coords = axes.coords_to_point(focus_val, 0)
        focus_dot = Dot(point=focus_point_coords, color=RED, radius=0.08)
        focus_label = MathTex("F").next_to(focus_dot, DOWN + RIGHT * 0.5).scale(0.8)
        self.play(Create(focus_dot), FadeIn(focus_label, shift=UP))
        self.wait(0.5)

        directrix_line = DashedLine(
            start=axes.coords_to_point(directrix_x, axes.y_range[0]),
            end=axes.coords_to_point(directrix_x, axes.y_range[1]),
            color=GREEN,
            stroke_width=2
        )
        directrix_label = MathTex("D").next_to(directrix_line, LEFT).scale(0.8).shift(UP)
        self.play(Create(directrix_line), FadeIn(directrix_label, shift=RIGHT))
        self.wait(1)

        # 4. Generate light rays, reflections, normals and angles
        incident_rays_group = VGroup()
        reflected_rays_group = VGroup()
        normals_group = VGroup()
        angles_group = VGroup() 

        y_values = np.linspace(-2, 2, 5) 

        for y_coord in y_values:
            x_parabola = parabola_a * y_coord**2
            hit_point = axes.coords_to_point(x_parabola, y_coord)
            
            incident_ray_start = axes.coords_to_point(axes.x_range[1], y_coord)
            incident_ray = Line(incident_ray_start, hit_point, color=YELLOW, stroke_width=3)
            incident_rays_group.add(incident_ray)

            reflected_ray = Line(hit_point, focus_dot.get_center(), color=ORANGE, stroke_width=3)
            reflected_rays_group.add(reflected_ray)

            # --- Cálculo e Desenho da Linha Normal Bidirecional ---
            # A normal aponta para fora da parábola (componente X negativa).
            # Para y > 0, m_normal é negativo, -m_normal é positivo -> normal_direction aponta para (-X, +Y)
            # Para y < 0, m_normal é positivo, -m_normal é negativo -> normal_direction aponta para (-X, -Y)
            m_normal = -y_coord/(2 * parabola_a) 
            normal_direction = normalize(np.array([-1, -m_normal, 0])) 
            
            if y_coord == 0: # Caso especial para o vértice
                normal_direction = LEFT 

            normal_length = 1.0 
            normal_line = DashedLine(
                start=hit_point - normal_direction * normal_length / 2,
                end=hit_point + normal_direction * normal_length / 2,
                color=WHITE,
                stroke_width=2
            )
            normals_group.add(normal_line)

            # --- Desenho dos Ângulos ---
            if abs(y_coord) > 0.01: # Evita o vértice para ângulos (onde as linhas são colineares)
                angle_vector_length = 0.7 
                angle_radius = 0.4 

                # Vetores auxiliares, **apontando do hit_point na direção correta**
                # Não use o `-` antes do ponto de destino!
                normal_vector_for_angle = Line(hit_point, -(hit_point + normal_direction * angle_vector_length))
                normal_vector_for_angle.set_opacity(0) 

                # Vetor do Raio Incidente (saindo do hit_point na direção *contrária* ao raio incidente que chega)
                # Raio incidente vem de incident_ray_start (X positivo) para hit_point (X da parábola)
                # Então, o vetor que aponta *para onde o raio veio* é (start - end)
                incident_vector_for_angle = Line(hit_point, hit_point + normalize(incident_ray_start - hit_point) * angle_vector_length)
                incident_vector_for_angle.set_opacity(0) 

                # Vetor do Raio Refletido (saindo do hit_point para o foco)
                reflected_vector_for_angle = Line(hit_point, hit_point + normalize(focus_dot.get_center() - hit_point) * angle_vector_length)
                reflected_vector_for_angle.set_opacity(0) 
                
                # --- Lógica Condicional para a Ordem das Linhas no Ângulo ---
                # Esta é a parte crítica para versões mais antigas do Manim
                # A intenção é que o arco fique no lado "côncavo" da parábola.
                
                if y_coord > 0: # Para pontos na metade superior da parábola
                    # Ângulo de Incidência ($\theta_i$): entre o raio incidente e a normal
                    # Queremos o arco que está 'abaixo' do raio incidente e 'acima' da normal (do lado esquerdo da normal)
                    # A ordem (normal -> incidente) no sentido anti-horário deve cobrir o lado de fora.
                    # A ordem (incidente -> normal) no sentido anti-horário deve cobrir o lado de dentro.
                    angle_i = Angle(
                        line2=incident_vector_for_angle, # Começa do raio incidente
                        line1=normal_vector_for_angle,   # Vai para a normal
                        radius=angle_radius,
                        color=PURPLE,
                        stroke_width=2,
                        # Não use `invert` se a versão não suporta
                    )
                    
                    # Ângulo de Reflexão ($\theta_r$): entre a normal e o raio refletido
                    # Queremos o arco que está 'abaixo' da normal e 'acima' do raio refletido (do lado direito da normal)
                    # A ordem (normal -> refletido) no sentido anti-horário deve cobrir o lado de dentro.
                    angle_r = Angle(
                        line2=normal_vector_for_angle,    # Começa da normal
                        line1=reflected_vector_for_angle, # Vai para o raio refletido
                        radius=angle_radius,
                        color=TEAL,
                        stroke_width=2,
                    )

                else: # Para pontos na metade inferior da parábola (y_coord < 0)
                    # Ângulo de Incidência ($\theta_i$): entre o raio incidente e a normal
                    # Queremos o arco que está 'acima' do raio incidente e 'abaixo' da normal (do lado esquerdo da normal)
                    # A ordem (normal -> incidente) no sentido anti-horário deve cobrir o lado de dentro.
                    angle_i = Angle(
                        line2=normal_vector_for_angle,   # Começa da normal
                        line1=incident_vector_for_angle, # Vai para o raio incidente
                        radius=angle_radius,
                        color=PURPLE,
                        stroke_width=2,
                    )
                    
                    # Ângulo de Reflexão ($\theta_r$): entre a normal e o raio refletido
                    # Queremos o arco que está 'acima' da normal e 'abaixo' do raio refletido (do lado direito da normal)
                    # A ordem (refletido -> normal) no sentido anti-horário deve cobrir o lado de dentro.
                    angle_r = Angle(
                        line2=reflected_vector_for_angle, # Começa do raio refletido
                        line1=normal_vector_for_angle,    # Vai para a normal
                        radius=angle_radius,
                        color=TEAL,
                        stroke_width=2,
                    )
                
                # Posicionar os rótulos no meio do arco
                label_i = MathTex("\\theta_i").set(width=0.3).move_to(angle_i.point_from_proportion(0.5)).set_color(PURPLE)
                label_i.shift(normalize(angle_i.point_from_proportion(0.5) - hit_point) * 0.05)

                label_r = MathTex("\\theta_r").set(width=0.3).move_to(angle_r.point_from_proportion(0.5)).set_color(TEAL)
                label_r.shift(normalize(angle_r.point_from_proportion(0.5) - hit_point) * 0.05)
                
                angles_group.add(angle_i, label_i, angle_r, label_r)


        # Animar a criação dos raios incidentes (amarelos)
        self.play(Create(incident_rays_group, lag_ratio=0.1, run_time=2))
        self.wait(0.5)

        # Animar as linhas normais
        self.play(Create(normals_group, lag_ratio=0.1, run_time=1.5))
        self.wait(0.5)

        # Animar os raios refletidos (laranjas) crescendo do ponto de impacto para o foco
        self.play(
            LaggedStart(
                *[
                    GrowFromPoint(ray, ray.get_start())
                    for ray in reflected_rays_group
                ],
                lag_ratio=0.1,
                run_time=2
            )
        )
        self.wait(0.5)

        # Animar os ângulos e seus rótulos
        self.play(Create(angles_group, lag_ratio=0.1, run_time=2))
        self.wait(2)

        # Limpeza
        self.play(FadeOut(VGroup(incident_rays_group, reflected_rays_group, 
                                 normals_group, angles_group))) 
        self.wait(0.5)

        self.play(
            FadeOut(parabola),
            FadeOut(focus_dot),
            FadeOut(focus_label),
            FadeOut(directrix_line),
            FadeOut(directrix_label),
            FadeOut(axes)
        )
        self.wait(1)

                # --- INÍCIO DA SEÇÃO DAS EQUAÇÕES ---

        # 1. Inclinações da Tangente e da Normal
        # Equação da parábola para referência inicial
        eq_parabola_ref = MathTex(r"y^2 = 4ax", font_size=45).to_edge(UP)
        self.play(Write(eq_parabola_ref))
        self.wait(1)

        # Derivada implícita
        eq_deriv_step = MathTex(r"2y \frac{dy}{dx} = 4a", font_size=40).next_to(eq_parabola_ref, DOWN, buff=0.5)
        self.play(TransformMatchingShapes(eq_parabola_ref, eq_deriv_step)) # Transforma a ref na derivada
        self.wait(1)

        # Inclinação da Tangente
        eq_mt = MathTex(r"m_T = \frac{dy}{dx}\bigg|_{(x_0, y_0)} = \frac{2a}{y_0}", font_size=40).next_to(eq_deriv_step, DOWN, buff=0.5)
        self.play(Write(eq_mt))
        self.wait(1)

        # Inclinação da Normal
        eq_mn = MathTex(r"m_N = -\frac{1}{m_T} = -\frac{y_0}{2a}", font_size=40).next_to(eq_mt, DOWN, buff=0.5)
        self.play(Write(eq_mn))
        self.wait(2)
        self.play(FadeOut(eq_deriv_step, eq_mt, eq_mn)) # Remove as equações de inclinação


        # 2. Inclinações dos Raios Incidente e Refletido
        eq_mip = MathTex(r"m_{IP} = 0", font_size=40).shift(UP)
        self.play(Write(eq_mip))
        self.wait(1)

        eq_mpf = MathTex(r"m_{PF} = \frac{y_0 - 0}{x_0 - a} = \frac{y_0}{x_0 - a}", font_size=40).next_to(eq_mip, DOWN, buff=0.8)
        self.play(Write(eq_mpf))
        self.wait(2)
        self.play(FadeOut(eq_mip, eq_mpf))


        # 3. Lei da Reflexão: Cálculo de tan theta_i
        tan_theta_i_l1 = MathTex(r"\tan \theta_i = \left| \frac{m_{IP} - m_N}{1 + m_{IP} m_N} \right|", font_size=40).shift(UP)
        self.play(Write(tan_theta_i_l1))
        self.wait(1)

        tan_theta_i_l2 = MathTex(r"= \left| \frac{0 - (-\frac{y_0}{2a})}{1 + 0 \cdot m_N} \right|", font_size=40).next_to(tan_theta_i_l1, DOWN, aligned_edge=tan_theta_i_l1.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_i_l1, tan_theta_i_l2)) # Transforma para a próxima linha
        self.wait(1)

        tan_theta_i_l3 = MathTex(r"= \frac{|y_0|}{2a}", font_size=40).next_to(tan_theta_i_l2, DOWN, aligned_edge=tan_theta_i_l2.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_i_l2, tan_theta_i_l3)) # Transforma para a próxima linha
        self.wait(2)
        self.play(FadeOut(tan_theta_i_l3)) # Remove a última linha, as anteriores já foram transformadas


        # 4. Lei da Reflexão: Cálculo de tan theta_r
        tan_theta_r_l1 = MathTex(r"\tan \theta_r = \left| \frac{m_{PF} - m_N}{1 + m_{PF} m_N} \right|", font_size=40).to_edge(UP)
        self.play(Write(tan_theta_r_l1))
        self.wait(1)

        tan_theta_r_l2 = MathTex(r"= \left| \frac{\frac{y_0}{x_0 - a} - (-\frac{y_0}{2a})}{1 + \frac{y_0}{x_0 - a} (-\frac{y_0}{2a})} \right|", font_size=40).next_to(tan_theta_r_l1, DOWN, aligned_edge=tan_theta_r_l1.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l1, tan_theta_r_l2))
        self.wait(0.5)

        tan_theta_r_l3 = MathTex(r"= \left| \frac{\frac{y_0(2a) + y_0(x_0 - a)}{2a(x_0 - a)}}{\frac{2a(x_0 - a) - y_0^2}{2a(x_0 - a)}} \right|", font_size=40).next_to(tan_theta_r_l2, DOWN, aligned_edge=tan_theta_r_l2.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l2, tan_theta_r_l3))
        self.wait(0.5)

        tan_theta_r_l4 = MathTex(r"= \left| \frac{y_0(2a + x_0 - a)}{2ax_0 - 2a^2 - y_0^2} \right|", font_size=40).next_to(tan_theta_r_l3, DOWN, aligned_edge=tan_theta_r_l3.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l3, tan_theta_r_l4))
        self.wait(0.5)

        # Linha com a substituição y_0^2 = 4ax_0
        tan_theta_r_l5 = MathTex(r"= \left| \frac{y_0(x_0 + a)}{2ax_0 - 2a^2 - 4ax_0} \right|", font_size=40).next_to(tan_theta_r_l4, DOWN, aligned_edge=tan_theta_r_l4.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l4, tan_theta_r_l5))
        self.wait(0.5)

        tan_theta_r_l6 = MathTex(r"= \left| \frac{y_0(x_0 + a)}{-2ax_0 - 2a^2} \right|", font_size=40).next_to(tan_theta_r_l5, DOWN, aligned_edge=tan_theta_r_l5.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l5, tan_theta_r_l6))
        self.wait(0.5)

        tan_theta_r_l7 = MathTex(r"= \left| \frac{y_0(x_0 + a)}{-2a(x_0 + a)} \right|", font_size=40).next_to(tan_theta_r_l6, DOWN, aligned_edge=tan_theta_r_l6.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l6, tan_theta_r_l7))
        self.wait(0.5)

        tan_theta_r_l8 = MathTex(r"= \left| -\frac{y_0}{2a} \right| = \frac{|y_0|}{2a}", font_size=40).next_to(tan_theta_r_l7, DOWN, aligned_edge=tan_theta_r_l7.get_part_by_tex('=').get_left())
        self.play(TransformMatchingShapes(tan_theta_r_l7, tan_theta_r_l8))
        self.wait(2)
        self.play(FadeOut(tan_theta_r_l8)) # Remove a última linha


        # 5. Conclusão Final
        eq_conclusion = MathTex(r"\tan \theta_i = \frac{|y_0|}{2a} \quad \text{e} \quad \tan \theta_r = \frac{|y_0|}{2a}", font_size=40).shift(UP)
        self.play(Write(eq_conclusion))
        self.wait(1.5)

        eq_conclusion_final = MathTex(r"\implies \theta_i = \theta_r", font_size=40).next_to(eq_conclusion, DOWN, buff=0.8)
        self.play(Write(eq_conclusion_final))
        self.wait(3)
        self.play(FadeOut(eq_conclusion, eq_conclusion_final))

        self.wait(1) # Aguarda antes de finalizar a cena