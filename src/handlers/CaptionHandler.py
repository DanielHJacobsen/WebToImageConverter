from PIL import Image, ImageDraw, ImageFont
from ..util.JsonExtraction import JsonExtraction as jsonExt


class CaptionHandler:
    
    @staticmethod
    def add_caption(site, image_path, is_with_log):
        captions = jsonExt.extract(site, "captions", [], "site", is_with_log)

        for caption in captions:
            CaptionHandler.add_captions(image_path, is_with_log, caption)

    @staticmethod
    def add_captions(image_path, is_with_log, caption):
        caption_text = jsonExt.extract(caption, "caption_text", "", "site", is_with_log)
        if caption_text == "":
            # Do nothing
            return

        else:
            # Open an Image
            img = Image.open(image_path)

            # Call draw Method to add 2D graphics in an image
            drawn_img = ImageDraw.Draw(img)

            # Add Text to an image
            caption_x = jsonExt.extract(caption, "caption_x", 28, "site", is_with_log)
            caption_y = jsonExt.extract(caption, "caption_y", 36, "site", is_with_log)
            caption_color = jsonExt.extract(caption, "caption_color", "#ff0000", "site", is_with_log)
            caption_size = jsonExt.extract(caption, "caption_size", 10, "site", is_with_log)
            caption_font = ImageFont.truetype("arial.ttf", caption_size)

            drawn_img.text(xy=(caption_x, caption_y), text=caption_text, fill=caption_color, font=caption_font)

            # Save the edited image
            img.save(image_path)
