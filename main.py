from manim import *
import time
import random
import math
import numpy as np

class BlackScreen(Scene):
    def construct(self):
        dot = Dot(point=ORIGIN, radius=DEFAULT_DOT_RADIUS, color=RED)
        self.wait(10)


class MonteCarloPiExplanation(Scene):
    def construct(self):
        circle = Circle(radius=3.5, color=RED)
        dot = Dot(point=ORIGIN, radius=DEFAULT_DOT_RADIUS, color=RED)

        line = Line(start=dot.get_center(), end=circle.get_right(), color=RED)

        brace = Brace(line, UP)

        brace_text = brace.get_text("1")

        self.play(Create(circle))

        self.wait(1)

        self.play(
            Create(dot),
            Create(line),
            Create(brace),
            Create(brace_text)
        )

        self.play(FadeOut(dot, line, brace, brace_text))

        self.wait(1)

        self.play(circle.animate.set_fill(color=RED, opacity=1))

        self.wait(1)

        self.play(circle.animate.set_fill(opacity=0))

        self.wait(1)

        square = Square(side_length=circle.radius * 2, color=RED)

        self.play(Create(square))

        self.wait(1)

        inside_circle_dot_vgroup = VGroup()
        outside_circle_dot_vgroup = VGroup()

        for i in range(1000):
            
            dot_max_x = float(square.get_right()[0])
            dot_min_x = float(square.get_left()[0])
            dot_max_y = float(square.get_top()[1])
            dot_min_y = float(square.get_bottom()[1])

            # dot_x = (random.random() * ((dot_max_x - 0.1) - (dot_min_x + 0.1))) + (dot_min_x + 0.1)
            # dot_y = (random.random() * ((dot_max_y - 0.1) - (dot_min_y + 0.1))) + (dot_min_y + 0.1)

            dot_x = (random.random() * ((dot_max_x) - (dot_min_x))) + (dot_min_x)
            dot_y = (random.random() * ((dot_max_y) - (dot_min_y))) + (dot_min_y)

            # TODO find out how to check if the dot is inside of the circle or outside. Add to two separate VGroups and color
            # then estimate pi by displaying ratio on the right side of the screen.

            circle_center = circle.get_center()

            distance_from_circle_center_to_point = math.sqrt(((dot_x-circle_center[0])**2)+((dot_y-circle_center[1])**2))

            # if inside of the circle
            if distance_from_circle_center_to_point < circle.radius:
                inside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=GREEN, radius=0.05))
            # otherwise, if outside of the circle
            else:
                outside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=RED, radius=0.05))
        
        self.play(
            Create(inside_circle_dot_vgroup),
            Create(outside_circle_dot_vgroup)
        )

        self.wait(1)

        def shrink_and_move_left(mob):
            mob.scale(0.75)
            mob.shift(LEFT*3)
            return mob

        self.play(
            ApplyFunction(shrink_and_move_left, circle),
            ApplyFunction(shrink_and_move_left, square),
            ApplyFunction(shrink_and_move_left, inside_circle_dot_vgroup),
            ApplyFunction(shrink_and_move_left, outside_circle_dot_vgroup)
        )

        self.wait(1)

        inside_copy_for_ratio = inside_circle_dot_vgroup.copy()
        second_inside_copy_for_ratio = inside_circle_dot_vgroup.copy()
        outside_copy_for_ratio = outside_circle_dot_vgroup.copy()

        all_dots = VGroup(second_inside_copy_for_ratio, outside_copy_for_ratio)

        self.add(
            inside_copy_for_ratio,
            second_inside_copy_for_ratio,
            outside_copy_for_ratio
        )
        
        def shrink_and_move_up_and_right(mob):
            mob.scale(0.5)
            mob.shift(RIGHT*5, UP*2)
            return mob
        
        def shrink_and_move_down_and_right(mob):
            mob.scale(0.5)
            mob.shift(RIGHT*5, DOWN*1)
            return mob

        self.play(ApplyFunction(shrink_and_move_up_and_right, inside_copy_for_ratio))
        
        line_start = np.array([inside_copy_for_ratio.get_left()[0], inside_copy_for_ratio.get_left()[1] - 1.5, inside_copy_for_ratio.get_left()[2]])
        line_end = np.array([inside_copy_for_ratio.get_right()[0], inside_copy_for_ratio.get_right()[1] - 1.5, inside_copy_for_ratio.get_right()[2]])

        line = Line(line_start, line_end)

        self.play(Create(line))

        self.play(ApplyFunction(shrink_and_move_down_and_right, all_dots))

        self.wait(1)

        num_dots_inside = len(inside_circle_dot_vgroup.submobjects)

        num_dots_outside = len(outside_circle_dot_vgroup.submobjects)

        pi = (num_dots_inside / (num_dots_inside + num_dots_outside)) * 4

        times_four = Tex(r'$\times 4 = $').next_to(line, RIGHT)

        pi_value = DecimalNumber(pi).next_to(times_four)

        self.play(Create(times_four))

        self.wait(1)

        self.play(Write(pi_value))

        self.clear()

        self.wait(5)

class PiEstimationDemonstration(Scene):
    def construct(self):

        circle = Circle(radius=3.5, color=RED)

        square = Square(side_length=circle.radius * 2, color=RED)

        def shrink_and_move_left(mob):
            mob.scale(0.75)
            mob.shift(LEFT*3)
            return mob

        self.play(
            Create(circle),
            Create(square),
        )

        self.play(
            ApplyFunction(shrink_and_move_left, circle),
            ApplyFunction(shrink_and_move_left, square)
        )

        pi_text, pi_value = pi_label = VGroup(
            Text("Pi: "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=4
            )
        )

        total_dots_text, total_dots = total_label = VGroup(
            Text("Total dots: "),
            DecimalNumber(
                0,
                num_decimal_places=0
            )
        )

        in_circle_text, in_circle = in_circle_label = VGroup(
            Text("Dots in circle: "),
            DecimalNumber(
                0,
                num_decimal_places=0
            )
        )

        pi_label.arrange(RIGHT)
        total_label.arrange(RIGHT)
        in_circle_label.arrange(RIGHT)

        pi_label.move_to((3, 1, 0))
        total_label.move_to((3, 0, 0))
        in_circle_label.move_to((3, -1, 0))

        self.add(pi_label, total_label, in_circle_label)

        self.wait(1)

        total_dots_num = 0
        in_circle_num = 0
        pi = 0

        pi_value.add_updater(lambda m: m.set_value(pi))
        total_dots.add_updater(lambda m: m.set_value(total_dots_num))
        in_circle.add_updater(lambda m: m.set_value(in_circle_num))

        inside_circle_dot_vgroup = VGroup()
        outside_circle_dot_vgroup = VGroup()

        random.seed(1)

        for i in range(5001):
            total_dots_num += 1

            dot_max_x = float(square.get_right()[0])
            dot_min_x = float(square.get_left()[0])
            dot_max_y = float(square.get_top()[1])
            dot_min_y = float(square.get_bottom()[1])

            dot_x = (random.random() * ((dot_max_x) - (dot_min_x))) + (dot_min_x)
            dot_y = (random.random() * ((dot_max_y) - (dot_min_y))) + (dot_min_y)

            circle_center = circle.get_center()

            distance_from_circle_center_to_point = math.sqrt(((dot_x-circle_center[0])**2)+((dot_y-circle_center[1])**2))

            # if inside of the circle
            if distance_from_circle_center_to_point < (3.5 * 0.75):
                in_circle_num += 1
                inside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=GREEN, radius=0.05))
                self.play(Create(Dot(point=[dot_x, dot_y, 0], color=GREEN, radius=0.05), run_time=0.08))
            # otherwise, if outside of the circle
            else:
                outside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=RED, radius=0.05))
                self.play(Create(Dot(point=[dot_x, dot_y, 0], color=RED, radius=0.05), run_time=0.08))
            num_dots_inside = len(inside_circle_dot_vgroup.submobjects)

            num_dots_outside = len(outside_circle_dot_vgroup.submobjects)

            pi = (num_dots_inside / (num_dots_inside + num_dots_outside)) * 4

        self.wait(10)
    
class BriefIntegrationConnection(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_min=0,
            y_max=5,
            x_min=0,
            x_max=5,
            y_axis_config={"tick_frequency": 1},
            x_axis_config={"tick_frequency": 1},
            y_labeled_nums=np.arange(0, 5, 1),
            x_labeled_nums=np.arange(0, 5, 1),
            **kwargs
        )
        self.function_color = RED

    def construct(self):
        self.setup_axes(animate=True)
        self.wait(1)
        func_graph = self.get_graph(lambda x: math.cos(x) + 2, x_max=5)

        point1 = self.coords_to_point(1, 2.54)
        point2 = self.coords_to_point(3, 2.54)
        point3 = self.coords_to_point(1, 0)
        point4 = self.coords_to_point(3, 0)


        line1 = Line(point1, point2, color=YELLOW)
        line2 = Line(point2, point4, color=YELLOW)
        line3 = Line(point1, point3, color=YELLOW)
        line4 = Line(point3, point4, color=YELLOW)
        # line1 = Line(self.coords_to_point(1, 2), self.coords_to_point(0, 0), color=YELLOW)
        # line1 = Line(self.coords_to_point(1, 2), self.coords_to_point(0, 0), color=YELLOW)
        # line1 = Line(self.coords_to_point(1, 2), self.coords_to_point(0, 0), color=YELLOW)


        graph_label = self.get_graph_label(func_graph, label="\\cos(x) + 2").shift(UP)
        self.play(
            Create(func_graph),
            Create(graph_label)
        )
        self.wait(1)
        self.play(
            Create(line1),
            Create(line2),
            Create(line3),
            Create(line4)
        )

        self.wait(1)

        inside_circle_dot_vgroup = VGroup()
        outside_circle_dot_vgroup = VGroup()

        total_dots_num = 0
        in_circle_num = 0

        integral = 0

        integral_text, integral_value = integral_label = VGroup(
            Text("Integral: "),
            DecimalNumber(
                0,
                num_decimal_places=4
            )
        )

        integral_label.arrange(RIGHT)

        integral_label.move_to((0, 3, 0))

        self.add(integral_label)

        integral_value.add_updater(lambda m: m.set_value(integral))
        

        for i in range(500):
            total_dots_num += 1

            dot_max_x = float(self.coords_to_point(3, 0)[0])
            dot_min_x = float(self.coords_to_point(1, 0)[0])
            dot_max_y = float(self.coords_to_point(0, 2.54)[1])
            dot_min_y = float(self.coords_to_point(1, 0)[1])

            # multiply random by real number line constraints to get real x and y

            dot_x_random = random.random()
            dot_y_random = random.random()

            dot_x = (dot_x_random * ((dot_max_x) - (dot_min_x))) + (dot_min_x)
            dot_y = (dot_y_random * ((dot_max_y) - (dot_min_y))) + (dot_min_y)

            real_dot_x = (dot_x_random * ((3) - (1))) + (1)
            real_dot_y = (dot_y_random * ((2.54) - (0))) + (0)

            # point_on_graph = math.cos()

            # if inside
            if real_dot_y < math.cos(real_dot_x) + 2:
                in_circle_num += 1
                inside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=GREEN, radius=0.05))
                self.play(Create(Dot(point=[dot_x, dot_y, 0], color=GREEN, radius=0.05), run_time=0.08))
            # otherwise, if outside
            else:
                outside_circle_dot_vgroup.add(Dot(point=[dot_x, dot_y, 0], color=RED, radius=0.05))
                self.play(Create(Dot(point=[dot_x, dot_y, 0], color=RED, radius=0.05), run_time=0.08))
            num_dots_inside = len(inside_circle_dot_vgroup.submobjects)

            num_dots_outside = len(outside_circle_dot_vgroup.submobjects)

            integral = (num_dots_inside / (num_dots_inside + num_dots_outside)) * 5.08
            


        self.wait(10)
