import cv2
import numpy as np
from config import config


class ShapeAnalysis:
    def __init__(self, debug=False):
        self.shapes = {'triangle': 0, 'rectangle': 0,
                       'polygons': 0, 'circles': 0}
        self.scale = config.shape_detection_scale
        self.debug = debug
        

    def analysis(self, frame):
        self.shapes = {'triangle': 0, 'rectangle': 0,
                       'polygons': 0, 'circles': 0}

        frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale)

        h, w, ch = frame.shape

        if self.debug:
            result = np.zeros((h, w, ch), dtype=np.uint8)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 99, 0)

        contours, hierarchy = cv2.findContours(
            binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if self.debug:
            cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
            cv2.imshow("gray", gray)
            cv2.imwrite("./img/1 gray.png", gray)
            cv2.imshow("binary", binary)
            cv2.imwrite("./img/2 binary.png", binary)
            cv2.imshow("frame", frame)
            cv2.imwrite("./img/3 frame.png", frame)

        circle_list = []

        for cnt in range(len(contours)):
            area = cv2.contourArea(contours[cnt])
            if area < 10000:
                continue

            # 輪廓逼近
            epsilon = 0.01 * cv2.arcLength(contours[cnt], True)
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)

            # 分析幾何形狀
            corners = len(approx)
            shape_type = ""
            if corners >= 10:
                count = self.shapes['circles']
                count = count + 1
                self.shapes['circles'] = count
                shape_type = "圓形"
            elif not self.debug:
                continue
            else:
                if corners == 3:
                    count = self.shapes['triangle']
                    count = count+1
                    self.shapes['triangle'] = count
                    shape_type = "三角形"
                elif corners == 4:
                    count = self.shapes['rectangle']
                    count = count + 1
                    self.shapes['rectangle'] = count
                    shape_type = "矩形"
                elif 4 < corners < 10:
                    count = self.shapes['polygons']
                    count = count + 1
                    self.shapes['polygons'] = count
                    shape_type = "多邊形"

            # 計算面積與周長
            p = cv2.arcLength(contours[cnt], True)
            area = cv2.contourArea(contours[cnt])

            # 求解中心位置
            mm = cv2.moments(contours[cnt])
            cx = int(mm['m10'] / mm['m00'])
            cy = int(mm['m01'] / mm['m00'])

            # 顏色分析
            color = frame[cy][cx]
            if self.debug:
                cv2.circle(result, (cx, cy), 3, (0, 0, 255), -1)
                print("color: {}".format(color),
                      "position: {}".format((cx, cy)))
                cv2.drawContours(result, contours, cnt, (0, 255, 0), 2)
            circle_list.append((np.array([cx, cy])/self.scale, color))
        if self.debug:
            # 提取與繪制輪廓
            result_img = self.draw_text_info(result)
            cv2.imshow("Analysis Result", result_img)
            cv2.imwrite("./img/4 result.png", result_img)
        return circle_list

    def draw_text_info(self, image):
        c1 = self.shapes['triangle']
        c2 = self.shapes['rectangle']
        c3 = self.shapes['polygons']
        c4 = self.shapes['circles']
        cv2.putText(image, "triangle: "+str(c1), (10, 20),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv2.putText(image, "rectangle: " + str(c2), (10, 40),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv2.putText(image, "polygons: " + str(c3), (10, 60),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        cv2.putText(image, "circles: " + str(c4), (10, 80),
                    cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 1)
        return image


if __name__ == "__main__":
    src = cv2.imread("./img/screenshot-1588224583.221296.png")

    crop_y = 400
    crop_x = 40

    src = src[crop_y:, crop_x:-crop_x]
    ld = ShapeAnalysis(debug=True)
    result = ld.analysis(src)
    print("result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
