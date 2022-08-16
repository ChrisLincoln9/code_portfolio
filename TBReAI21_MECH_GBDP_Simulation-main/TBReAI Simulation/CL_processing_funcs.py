import math
import random
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import pygame
import scipy.stats as st


def extract_coords(cones):
    """
    :param cones:
    the array of cone objects
    :return:
    two arrays, with each of the x and y coordinates for all cones
    """
    # Need coordinates extracted from object
    x_coords = []
    y_coords = []
    for cone in cones:
        x_coords.append(cone.x)
        y_coords.append(cone.y)
    return x_coords, y_coords


def gps_pos_noise(base_station, abs_pos):
    """
    Simple random noise from a uniform distribution
    :param base_station: Change accuracy if theres a base station
    :param abs_pos: raw position data
    :return: the 'measured' data with noise
    """

    meas_pos = [0, 0]
    if base_station:
        noise_amplitude = 0.01  # 1cm for if base station exists
    else:
        noise_amplitude = 1.2  # 1.2m for if base station does not exist
    meas_pos[0] = abs_pos[0] + 2 * (random.uniform(0, 1) - 0.5) * noise_amplitude
    meas_pos[1] = abs_pos[1] + 2 * (random.uniform(0, 1) - 0.5) * noise_amplitude
    return meas_pos

def gps_vel_noise(abs_vel):
    """
    Simple random noise from a uniform distribution
    :param base_station: Change accuracy if theres a base station
    :param abs_vel: raw velocity data
    :return: the 'measured' data with noise
    """
    meas_vel = [0, 0]
    noise_amplitude = 0.03  # m/s
    meas_vel[0] = abs_vel[0] + 2 * (random.uniform(0, 1) - 0.5) * noise_amplitude
    meas_vel[1] = abs_vel[1] + 2 * (random.uniform(0, 1) - 0.5) * noise_amplitude
    return meas_vel

def depth_perception_noise(distance):
    """
    Using the documentation for the ZED camera, the accuracy is proportional to the square of the distance:
    Rz = a z^2
    1% at close values, quadratically to 9% at max range of 20m
    :param distance: the raw distance value to the cone
    :return: distance with noise
    """
    alpha = 0.0045 # Derived from zed camera website
    depth_resolution = distance**2 * alpha
    depth_with_noise = distance + 2 * (random.uniform(0, 1) - 0.5) * depth_resolution # add random uniform noise
    return depth_with_noise

class CalculateConeDistance:

    def __init__(self, left_cones, right_cones):
        self.left_xy = extract_coords(left_cones)
        self.right_xy = extract_coords(right_cones)

    def normalise_fov_angles(self,phi_yaw):
        """
        Accounts for the edge case where the output of np.arctan2 flips from 180 to -180 degrees
        sets the FOV angles accordingly using a + or - 360 correction to the affected side
        :param phi_yaw: current yaw angle of the vehicle
        """
        #Correct for flipping of sign when 180/-180 degrees is reached
        if phi_yaw < -135:
            self.start_fov_angle = phi_yaw - 45 + 360
            self.end_fov_angle = phi_yaw + 45
        if phi_yaw > 135:
            self.start_fov_angle = phi_yaw - 45
            self.end_fov_angle = phi_yaw + 45 - 360
        return


    def get_relative_cone_polar(self, xy, phi_yaw):
        """
        Function to find out which cones are within the FOV of the camera, and how far away they are from the camera, and what bearing
        relative to the direction of the vehicle
        :param xy: the xy of input cones, either left or right
        :param phi_yaw: the current yaw angle of the vehicle
        :return: returns all cones within the 90 degree FOV of the camera, that are within 20m
        """
        close_cones = []
        #print('Phi ' + str(phi_yaw) + ', Start Fov Angle: ' + str(self.start_fov_angle) + ', End Fov Angle: ' + str(
            #self.end_fov_angle))
        for i in range(len(xy[0]) - 1):
            rel_pos_x = xy[0][i] - self.abs_pos[0]
            rel_pos_y = xy[1][i] - self.abs_pos[1]
            distance = math.sqrt((rel_pos_x ** 2) + (rel_pos_y ** 2))
            if distance < 20:
                angle = np.arctan2(rel_pos_x, rel_pos_y) * 180 / math.pi
                if (angle > self.start_fov_angle) and (angle < self.end_fov_angle) and not self.edge_case: # Regular case
                    #print('Regular case: Angle: ' + str(angle))
                    close_cones.append([distance, (angle - phi_yaw), i])
                if not (self.end_fov_angle < angle < self.start_fov_angle) and self.edge_case: # Edge case
                    #print('Edge case: Angle: ' +str(angle))
                    if (phi_yaw < 0 and angle < 0) or (phi_yaw > 0 and angle > 0):
                        # if angle and phi are on same sides of 180/-180 edge
                        distance = depth_perception_noise(distance)  # add noise
                        close_cones.append([distance, (angle - phi_yaw), i])
                    else:
                        # if angle and phi are on opposite sides of 180/-180 edge
                        distance = depth_perception_noise(distance)  # add noise
                        close_cones.append([distance, - (angle - phi_yaw), i])
        return close_cones

    def check_cam_fov(self, abs_pos, yaw):
        """
        The top level function for the calculate cone distance class, has an output array of close cones that are
        within the field of view of the camera, for both the left cones and right cones

        :param abs_pos: the current coordinates of the car
        :param yaw: the current yaw angle of the car
        :return:
        """
        self.abs_pos = abs_pos
        phi_yaw = yaw
        print(yaw)
        if phi_yaw< -135 or phi_yaw>135:
            self.normalise_fov_angles(phi_yaw)
            self.edge_case = True
        else:
            self.start_fov_angle = phi_yaw - 45
            self.end_fov_angle = phi_yaw + 45
            self.edge_case = False

        self.normalise_fov_angles(phi_yaw)

        close_cones_left = self.get_relative_cone_polar(self.left_xy, phi_yaw)
        close_cones_right = self.get_relative_cone_polar(self.right_xy, phi_yaw)

        # print('close cones left: ' + str(close_cones_left))
        # print('close cones right: ' + str(close_cones_right))


class CameraNoise:
    """
    Class that is used to select camera noise, and sets up display using a pygame window so that the image can
    be refreshed quickly
    """
    def __init__(self, kernel_length, gsig):
        """
        Initialises kernals for motion and gaussian blur and opens the pygame window
        :param kernel_length:
        the size in pixels of the length of the square kernel
        :param gsig: int
        The sigma characteristic of the 2D gaussian distribution
        """
        self.horizontal_kernel = np.zeros((kernel_length, kernel_length))
        self.horizontal_kernel[int((kernel_length - 1) / 2), :] = np.ones(kernel_length)
        self.horizontal_kernel /= kernel_length
        pygame.init()
        self.screen = pygame.display.set_mode((512 + (2 * 50), 256 + (2 * 50)))
        self.clock = pygame.time.Clock()
        # Generate Gaussian kernal
        x = np.linspace(-gsig, gsig, (kernel_length + 1))
        kernal1D = np.diff(st.norm.cdf(x))
        kernal2D = np.outer(kernal1D, kernal1D)
        self.gkern = kernal2D / kernal2D.sum()

    def motion_blur(self, image):
        """
        Using the cv2 library, the horizontal motion blur is added,
        the new image then updates onto the pygame window

        :param image: the output from the coppeliasim vision sensor
        """
        horizontal_mb = cv2.filter2D(image, -1, self.horizontal_kernel)
        surface = pygame.surfarray.make_surface(horizontal_mb)
        surface = pygame.transform.rotate(surface, 90)
        self.screen.blit(surface, (50, 50))
        pygame.display.flip()
        self.clock.tick(60)
        pygame.display.set_caption("Horizontal Motion Blur")

    def gaussian_blur(self, image):
        """
        Using the cv2 library, the gaussian blur is added,
        the new image then updates onto the pygame window

        :param image: the output from the coppeliasim vision sensor
        """
        blurred = cv2.filter2D(image, -1, self.gkern)
        surface = pygame.surfarray.make_surface(blurred)
        surface = pygame.transform.rotate(surface, 90)
        self.screen.blit(surface, (50, 50))
        pygame.display.flip()
        self.clock.tick(60)
        pygame.display.set_caption("Gaussian Blur")

