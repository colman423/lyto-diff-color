#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import base64
import cv2
import numpy as np
from shape_detection import ShapeAnalysis
import time
from config import config
from MouseClicker import MouseClicker



class Gamer:
    def __init__(self):
        self.driver = webdriver.Chrome(
            config.webdriver_path)   # create a selenium driver
        # go to facebook
        self.driver.get('https://www.facebook.com/')
        self.mouse_clicker = MouseClicker(driver=self.driver)
        self.iframe = None      # the game's iframe
        self.canvas = None      # the game's canvas
        self.shape_detector = ShapeAnalysis()

    def get_game_canvas(self):
        try:
            # manually click 'Start Game' / '開始玩'
            input("press any key after clicking 'Start Game'...")

            self.iframe = self.driver.find_element_by_css_selector('iframe')
            self.driver.switch_to.frame(self.iframe)
            self.canvas = self.driver.find_element_by_css_selector("canvas")
            self.mouse_clicker.canvas = self.canvas
            return True
        except:
            return False

    def start(self):
        self.driver.get(config.game_url)      # go to game page

        while not self.get_game_canvas():
            pass

        while True:
            if input("press enter while a new stage is rendered. press '0' to exit: ") == "0":
                break
            click_time = self.play()    # click the right ball once
            print("previous click time =", click_time)

    def get_canvas_img(self):
        canvas_base64 = self.driver.execute_script(
            "return arguments[0].toDataURL('image/png').substring(21);",
            self.canvas
        )
        encoded_data = canvas_base64.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if config.save_input_img:
            cv2.imwrite("./img/screenshot-{}.png".format(time.time()), img)
        return img

    def get_diff_ball(self, balls):
        positions = [ball[1] for ball in balls]
        diffs, indices, counts = np.unique(
            positions, axis=0, return_index=True, return_counts=True)
        diff_idx = 1 if counts[0] > counts[1] else 0
        positions_idx = indices[diff_idx]
        return balls[positions_idx]

    def get_diff_ball_pos(self, screenshot):
        crop_x = config.screenshot_crop_x
        crop_y = config.screenshot_crop_y
        # crop the img, we only need the balls
        crop_img = screenshot[
            crop_y:,
            crop_x:-crop_x
        ]
        if config.save_input_img:
            cv2.imwrite("./img/last_crop.png", crop_img)

        balls = self.shape_detector.analysis(crop_img)
        # balls[0] = position
        # balls[1] = color

        diff_ball = self.get_diff_ball(balls)
        diff_ball_pos = self.get_diff_ball(balls)[0]
        diff_ball_pos_x = diff_ball_pos[0] + crop_x
        diff_ball_pos_y = diff_ball_pos[1] + crop_y

        return (diff_ball_pos_x, diff_ball_pos_y)

    def play(self):
        try:
            canvas_img = self.get_canvas_img()    # get the screenshot of the game

            # calculate which ball is diff color, and get it's position
            to_click_pos = self.get_diff_ball_pos(canvas_img)

            time1 = time.time()
            self.mouse_clicker.click(to_click_pos[0], to_click_pos[1])
            time2 = time.time()
            click_time = (time2-time1)*1000.0
            return click_time
        except:
            return 'ERROR!!!'

    def stop(self):
        while input("type 'close' to close browser: ") != "close":
            pass
        self.driver.close()

