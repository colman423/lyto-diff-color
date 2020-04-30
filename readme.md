# Lyto Diff Color Hacker

<!-- ## DEMO
todo \>\< -->

## Notice
***DON'T share .cookie file to others.***

<!-- ### FBinstant -->

## Environment
python 3.7.1

win10 1600*900

chrome window size: 1280*720


## Usage
1. Clone it `git clone https://github.com/colman423/lyto-diff-color.git`
2. Install packages with `pip install -r requirements.txt`
3. Rename `config.example.py` to `config.py` and [set options](#Options) inside.
4. Run with `python main.py`
5. Follow the guide shown in cli.
6. Would you give me a star QAQ.

## Options
| Name  | Description |
| ------------- | ------------- |
| `webdriver_path` | Path to your `chromedriver.exe`. [Download chromedriver here](https://chromedriver.chromium.org/downloads). <br />Make sure your chromedriver version is equal to your chrome's version. |
| `first_use` | If it's your first time to use this tool, set to `True`, else set to `False`. <br /> While setting `first_use` to `True`, it will automatically save a `.cookie` file in `config/` after success logged in to FB, <br /> and make a new dir named `img/` which storing screenshot images. <br /> While setting it to False, it will read the `.cookie` file and automatically login to FB. <br /> ***DON'T share `.cookie` file to others.***|
| `save_input_img` | If `True`, the screenshot of the game will be saved into `img/`. |
| `game_url` | The url of the game, can be either the url of FB game lobby, or your friends' game challenge post. |
| `screenshot_crop_x` | We only want to detect shape of the balls, so we need to crop animations on both sides. <br /> For me, my chrome's size is 1280*720, the best crop_x size is 40.  |
| `screenshot_crop_y` | We only want to detect shape of the balls, so we need to crop UI at the top. <br /> For me, my chrome's size is 1280*720, the best crop_y size is 450. |
| `shape_detection_scale` | After stage 48, the balls is too many so that they'll be too close to each others, which will make shape detection harder. <br /> We need to resize the screenshot to bigger size, so that shape detection won't crashed. <br /> For me, `1.5` is enough.|

