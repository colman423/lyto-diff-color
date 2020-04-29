#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import cookie_helper
import base64
import cv2
import numpy as np
from shape_detection import ShapeAnalysis
import warnings
import time
from config import config
import os

warnings.filterwarnings('ignore')


def get_canvas_img(driver, canvas):
    canvas_base64 = driver.execute_script(
        "return arguments[0].toDataURL('image/png').substring(21);", canvas)
    encoded_data = canvas_base64.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def get_diff_circle(circles):
    positions = [circle[1] for circle in circles]
    diffs, indices, counts = np.unique(
        positions, axis=0, return_index=True, return_counts=True)
    diff_idx = 1 if counts[0] > counts[1] else 0
    positions_idx = indices[diff_idx]
    return circles[positions_idx]


def get_to_click_circle_pos(img, scale):
    crop_y = 450
    crop_x = 40

    crop_img = img[crop_y:, crop_x:-crop_x]
    if config.save_input_img:
        cv2.imwrite("./img/last_crop.png", crop_img)

    ld = ShapeAnalysis()
    circles = ld.analysis(crop_img, scale=scale)
    # circles[0] = position
    # circles[1] = color

    diff_circle_pos = get_diff_circle(circles)[0]
    diff_circle_pos = (diff_circle_pos[0]+crop_x, diff_circle_pos[1]+crop_y)

    return diff_circle_pos


def click_pos(driver, canvas, x, y, prevX, prevY):

    ideal_w = float(canvas.get_attribute('width'))
    ideal_h = float(canvas.get_attribute('height'))
    real_w = float(canvas.value_of_css_property('width')[:-2])
    real_h = float(canvas.value_of_css_property('height')[:-2])

    scale = real_w / ideal_w

    act = ActionChains(driver)

    if prevX == None:
        act.move_to_element(canvas)
        act.move_by_offset(-real_w/2, -real_h/2)
        act.move_by_offset(x*scale, y*scale)
    else:
        act.move_by_offset((x-prevX)*scale, (y-prevY)*scale)

    act.click()
    act.perform()


def play():
    canvas_img = get_canvas_img(driver, canvas)
    if config.save_input_img:
        cv2.imwrite("./img/{}.png".format(time.time()), canvas_img)

    scale = 1.5
    to_click_pos = get_to_click_circle_pos(canvas_img, scale)

    time1 = time.time()
    global prevX
    global prevY
    click_pos(driver, canvas, to_click_pos[0], to_click_pos[1], prevX, prevY)
    prevX = to_click_pos[0]
    prevY = to_click_pos[1]
    time2 = time.time()
    click_time = (time2-time1)*1000.0
    return click_time


if __name__ == "__main__":
    driver = webdriver.Chrome(config.webdriver_path)
    driver.get('https://www.facebook.com/')

    if config.first_use:
        os.makedirs('img')
        input("press any key after success login...")
        cookie_helper.save(driver)

    else:
        cookie_helper.load(driver)

    driver.get(config.post_path)

    input("press any key after clicking 'Start Game'...")
    # driver.switch_to.default_content()
    iframes = driver.find_element_by_css_selector('iframe')
    driver.switch_to.frame(iframes)

    canvas = driver.find_element_by_css_selector("canvas")

    prevX = None
    prevY = None

    while True:
        if input("press enter while a new stage is rendered. press '0' to exit: ") == "0":
            break
        click_time = play()
        print("click_time", click_time)

    input("press any key to close browser")
    driver.close()
