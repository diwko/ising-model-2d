import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class View:
    def __init__(self, temperature, magnetic_field, spins):
        plt.subplots_adjust(0.1, 0.2, 0.9, 0.9)
        self.plot = plt.imshow(spins)

        self.temperature_slider = Slider(plt.axes([0.2, 0.14, 0.6, 0.02]), 'Temperature:', 0.01, 100.0,
                                         valinit=temperature)
        self.magnetic_slider = Slider(plt.axes([0.2, 0.1, 0.6, 0.02]), 'Magnetic Field:', 0.0, 100.0,
                                      valinit=magnetic_field)

        plt.ion()
        plt.show()

    def update(self, spins):
        self.plot.set_data(spins)
        plt.draw()
        plt.pause(1e-9)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.temperature_slider.on_changed(self.update_temperature)
        self.view.magnetic_slider.on_changed(self.update_magnetic_field)

    def run(self):
        i = 0
        while True:
            self.update_model()
            i += 1
            if i == 1000:
                self.update_view()
                i = 0

    def update_temperature(self, temperature):
        self.model.set_temperature(temperature)

    def update_magnetic_field(self, magnetic_field):
        self.model.set_magnetic_field(magnetic_field)

    def update_model(self):
        rand_pos = self.get_random_position()
        energy = self.model.get_component_energy(*rand_pos)
        if energy > 0:
            self.model.switch_spin(*rand_pos)
        else:
            random_number = random.uniform(0, 1)
            if random_number < np.exp(2 * energy / self.model.temperature):
                self.model.switch_spin(*rand_pos)

    def update_view(self):
        self.view.update(self.model.spins)

    def get_random_position(self):
        return random.randint(0, self.model.width - 1), random.randint(0, self.model.height - 1)


class Model:
    def __init__(self, width=64, height=64, temperature=50.0, magnetic_field=0.0):
        self.width = width
        self.height = height
        self.spins = np.random.choice([-1, 1], (width, height))
        self.temperature = temperature
        self.magnetic_field = magnetic_field

    def switch_spin(self, i, j):
        self.spins[i, j] *= -1

    def get_component_energy(self, i, j):
        return -self.spins[i, j] * self.get_adj_sum(i, j) - self.magnetic_field*self.spins[i, j]

    def get_adj_sum(self, i, j):
        elements = filter(
            lambda x: 0 <= x[0] < self.width and 0 <= x[1] < self.height,
            [(i, j), (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        )
        s = 0
        for x, y in elements:
            s += self.spins[x, y]
        return s

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_magnetic_field(self, magnetic_field):
        self.magnetic_field = magnetic_field


if __name__ == "__main__":
    model = Model()
    view = View(model.temperature, model.magnetic_field, model.spins)
    controller = Controller(model, view)

    controller.run()
