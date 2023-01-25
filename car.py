from car_vision import *
from game_settings import *
from neural_net import *
import copy
import tensorflow as tf

class car(object):

    def __init__(self, display, start_x, start_y, course_lines, brain=None):
        self.x = start_x
        self.y = start_y
        self.start_pos_x = start_x
        self.start_pos_y = start_y
        self.speed = 0
        self.width = car_width
        self.height = car_height
        self.curr_angle = 0
        self.score = 0
        self.front_left = (self.x, self.y)
        self.front_right = (self.x + self.width, self.y)
        self.back_left = (self.x, self.y + self.height)
        self.back_right = (self.x + self.width, self.y + self.height)
        self.center_pos = (self.x + self.width/2, self.y + self.height/2)
        self.display = display
        self.color = (255, 0, 0)
        self.car_img = pygame.image.load(images_folder + "car.png").convert_alpha()
        self.car_img = pygame.transform.scale(self.car_img, (car_width, car_height))
        self.image = self.car_img
        self.rect = self.image.get_rect(center=self.center_pos)
        self.course_lines = course_lines
        self.vision = car_vision((self.front_left, self.front_right, self.back_left, self.back_right), course_lines)
        self.brain = Neural_Network(5, 8, 2, brain)
        self.has_crashed = False


    def copy(self):
        # cloning the model is very slow
        brain_model = tf.keras.models.clone_model(model=self.brain.model)
        brain_model.set_weights(self.brain.model.get_weights())
        new_car = car(self.display, self.start_pos_x, self.start_pos_y, self.course_lines, brain_model)
        return new_car

    def think(self):
        inputs = self.vision.vision_distances
        inputs[:] = [x / (vision_distance/6) for x in inputs]
        outputs = self.brain.predict(inputs)
        return outputs

    def mutate(self, mutation_rate):
        self.brain.mutate(mutation_rate)

    def draw(self, display_vision_lines = False):
        #draw car
        self.curr_angle = self.curr_angle % 1440
        working_angle = self.curr_angle / 4
        image, self.rect = self.rotate_img(self.image, self.rect, -working_angle)
        self.display.blit(image, self.rect)
        #draw car vision lines
        if display_vision_lines and not self.has_crashed:
            for vision_line in self.vision.vision_lines:
                pygame.draw.line(self.display, (0, 255, 0), vision_line[0], vision_line[1])
                pygame.draw.circle(self.display, (0, 0, 255), (int(vision_line[1][0]), int(vision_line[1][1])), 5)

    def check_crash(self):
        for course_line in self.course_lines:
            #check front
            if intersects(course_line[0], course_line[1], self.front_left, self.front_right):
                pygame.draw.aaline(self.display, (255,0,0), course_line[0], course_line[1])
                self.has_crashed = True
            #check right
            if intersects(course_line[0], course_line[1], self.front_right, self.back_right):
                pygame.draw.aaline(self.display, (255,0,0), course_line[0], course_line[1])
                self.has_crashed = True
            #check bottom
            if intersects(course_line[0], course_line[1], self.back_right, self.back_left):
                pygame.draw.aaline(self.display, (255,0,0), course_line[0], course_line[1])
                self.has_crashed = True
            #check left
            if intersects(course_line[0], course_line[1], self.front_left, self.back_left):
                pygame.draw.aaline(self.display, (255,0,0), course_line[0], course_line[1])
                self.has_crashed = True

    def rotate_img(self, image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=self.center_pos)
        return new_image, rect

    def delete_car(self):
        tf.keras.backend.clear_session()

    def accelerate(self):
        self.speed += acceleration_factor
        if self.speed >= max_speed:
            self.speed = max_speed
        self.move()

    def move(self):
        self.curr_angle = self.curr_angle % 1440
        working_angle = self.curr_angle / 4 + 90
        x_change = -self.speed * math.cos(math.radians(working_angle))
        y_change = -self.speed * math.sin(math.radians(working_angle))
        self.center_pos = (self.center_pos[0] + x_change, self.center_pos[1] + y_change)
        self.front_left = (self.front_left[0] + x_change, self.front_left[1] + y_change)
        self.front_right = (self.front_right[0] + x_change, self.front_right[1] + y_change)
        self.back_right = (self.back_right[0] + x_change, self.back_right[1] + y_change)
        self.back_left = (self.back_left[0] + x_change, self.back_left[1] + y_change)
        self.vision.update((self.front_left, self.front_right, self.back_left, self.back_right))

    def rotate_right(self):
        self.front_left = self.rotate(self.front_left, rotation_factor)
        self.front_right = self.rotate(self.front_right, rotation_factor)
        self.back_left = self.rotate(self.back_left, rotation_factor)
        self.back_right = self.rotate(self.back_right, rotation_factor)
        self.vision.update((self.front_left, self.front_right, self.back_left, self.back_right))

    def rotate_left(self):
        self.front_left = self.rotate(self.front_left, 360 - rotation_factor)
        self.front_right = self.rotate(self.front_right, 360 - rotation_factor)
        self.back_left = self.rotate(self.back_left, 360 - rotation_factor)
        self.back_right = self.rotate(self.back_right, 360 - rotation_factor)
        self.vision.update((self.front_left, self.front_right, self.back_left, self.back_right))

    def rotate(self, point, angle):
        self.curr_angle += angle
        curr_x = point[0]
        curr_y = point[1]
        s = math.sin(math.radians(angle))
        c = math.cos(math.radians(angle))
        curr_x -= self.center_pos[0]
        curr_y -= self.center_pos[1]
        newx = curr_x * c - curr_y * s
        newy = curr_x * s + curr_y * c
        curr_x = newx + self.center_pos[0]
        curr_y = newy + self.center_pos[1]
        return (curr_x, curr_y)
