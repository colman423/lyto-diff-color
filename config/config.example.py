webdriver_path = 'yourpath/to/chromedriver'   # your chromedriver path, the driver's version should equal to your chrome
first_use = True      # set to False after cookie saved first time
save_input_img = True   # set to False if dont want to save game's imgs
game_url = 'https://www.facebook.com/instantgames/play/1099543880229447/'    # or your friends' post

# tune to proper value to make sure the screenshot is cropped to only the balls
screenshot_crop_x = 40
screenshot_crop_y = 450

# tune to proper value to help shape detection always correct in any stage.
shape_detection_scale = 1.5
