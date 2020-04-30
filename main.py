#!/usr/bin/env python
# coding: utf-8

import cookie_helper
import warnings
from config import config
import os
from Gamer import Gamer

warnings.filterwarnings('ignore')

if __name__ == "__main__":
    print("loading...")
    gamer = Gamer()

    if config.first_use:
        os.makedirs('img')
        input("press any key after success login...")
        cookie_helper.save(gamer.driver)

    else:
        cookie_helper.load(gamer.driver)

    gamer.start()
    gamer.stop()
