# 判断矩形是否碰撞
class Rectangular() :

    def __init__(self, x, y, w, h):

        self.x0 = x
        self.y0 = y
        self.x1 = x + w
        self.y1 = y + h
        self.w = w
        self.h = h


    def __gt__(self, other) :

        if self.w > other.w and self.h > other.h:
            return True
        return False


    def __lt__(self, other) :
        if self.w < other.w and self.h < other.h:
            return True
        return False


    def collision(self, r2) :

        if self.x0 < r2.x1 and self.y0 < r2.y1 and self.x1 > r2.x0 and self.y1 > r2.y0:
            return True
        return False


# 创建用于计算碰撞的矩形框对象
def createRectangular(val, word_width):
    return Rectangular(val["Coordinate"]["UpperLeft"][0],
                       val["Coordinate"]["UpperLeft"][1],
                       val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0] + word_width,
                       val["Coordinate"]["LowerLeft"][1] - val["Coordinate"]["UpperLeft"][1])


# 找出矩形框碰撞对象
def findRectangular(rr1, ocr_result, index1, tmp_words_list):
    for index2, val in enumerate(ocr_result):
        if index2 <= index1:
            continue
        word_width = (val["Coordinate"]["UpperRight"][0] - val["Coordinate"]["UpperLeft"][0]) // 2
        rr2 = createRectangular(val, word_width)
        if rr2.collision(rr1):
            tmp_words_list.append(val)
            findRectangular(rr2, ocr_result, index2, tmp_words_list)
            break


# 找出矩形框碰撞对象
def findRectangular2(rr1, ocr_result, index1, tmp_words_list, word_width):
    for index2, val in enumerate(ocr_result):
        if index2 <= index1:
            continue
        rr2 = createRectangular(val, word_width)
        if rr2.collision(rr1):
            tmp_words_list.append(val)
            findRectangular2(rr2, ocr_result, index2, tmp_words_list, word_width)
            break