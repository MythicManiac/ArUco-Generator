import os

from PIL import Image, ImageDraw, ImageFont

from cv2 import imwrite
from cv2 import aruco

CARD_WIDTH = 825
CARD_HEIGHT = 1125
CARD_TEXT_OFFSET = (108, 108)
CODE_SIZE = 600
FONT_PATH = "resources/Helvetica-Regular.ttf"


class CardGraphicGenerator(object):

    def __init__(self, output_path, start, stop):
        self.output_path = os.path.abspath(output_path)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(os.path.join(self.output_path, "marksers")):
            os.makedirs(os.path.join(self.output_path, "markers"))
        self.start = start
        self.stop = stop
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        self.font = ImageFont.truetype(FONT_PATH, 384)

    def get_output_path(self, filename):
        return os.path.join(self.output_path, filename)

    def generate(self):
        for i in range(self.start, self.stop):
            marker_path = self.create_marker(i)
            card_path = self.create_card(i, marker_path)
            print(card_path)

    def create_marker(self, code):
        marker = aruco.drawMarker(self.aruco_dict, code, 600)
        filename = self.get_output_path("markers/marker_%s.png" % code)
        imwrite(filename, marker)
        return filename

    def create_card(self, code, marker_path):
        card = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255))
        marker = Image.open(marker_path)
        card.paste(marker, (
            int(card.width / 2 - marker.width / 2),
            int(card.height / 2 - marker.height / 2)
        ))

        card_text = self.render_text(str(code))
        card.paste(card_text, CARD_TEXT_OFFSET)
        card = card.transpose(Image.ROTATE_180)
        card.paste(card_text, CARD_TEXT_OFFSET)
        card = card.transpose(Image.ROTATE_180)

        filename = self.get_output_path("card_%s.png" % code)
        card.save(filename)
        return filename

    def render_text(self, text):
        image = Image.new("RGBA", (800, 400), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, (0, 0, 0), font=self.font)
        image = image.resize((200, 100), Image.ANTIALIAS)
        return image


def main():
    generator = CardGraphicGenerator(
        output_path="markers",
        start=0,
        stop=212
    )
    generator.generate()


if __name__ == "__main__":
    main()
