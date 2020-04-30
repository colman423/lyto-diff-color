from selenium.webdriver.common.action_chains import ActionChains

# to click the driver faster
class MouseClicker:

    def __init__(self, driver=None, canvas=None):
        self.driver = driver
        self.canvas = canvas
        self.prev_x = None
        self.prev_y = None

    def click(self, x, y):
        ideal_w = float(self.canvas.get_attribute('width'))
        ideal_h = float(self.canvas.get_attribute('height'))
        real_w = float(self.canvas.value_of_css_property('width')[:-2])
        real_h = float(self.canvas.value_of_css_property('height')[:-2])

        scale = real_w / ideal_w

        act = ActionChains(self.driver)

        if self.prev_x == None:
            act.move_to_element(self.canvas)
            act.move_by_offset(-real_w/2, -real_h/2)
            act.move_by_offset(x*scale, y*scale)
        else:
            act.move_by_offset((x-self.prev_x)*scale, (y-self.prev_y)*scale)

        act.click()
        act.perform()

        self.prev_x = x
        self.prev_y = y
