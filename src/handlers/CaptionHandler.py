from PIL import Image, ImageDraw, ImageFont
from ..util.JsonExtraction import JsonExtraction as jsonExt


class CaptionHandler:
    
    @staticmethod
    def add_caption_to_image(site, image_path, is_with_log):
        caption = jsonExt.extract(site, "caption", "", "site", is_with_log)
        if caption == "":
            # Do nothing
            return

        else:
            # Open an Image
            img = Image.open(image_path)

            # Call draw Method to add 2D graphics in an image
            drawn_img = ImageDraw.Draw(img)

            # Add Text to an image
            caption_x = jsonExt.extract(site, "caption_x", 28, "site", is_with_log)
            caption_y = jsonExt.extract(site, "caption_y", 36, "site", is_with_log)
            caption_color = jsonExt.extract(site, "caption_color", "#ff0000", "site", is_with_log)
            caption_size = jsonExt.extract(site, "caption_size", 10, "site", is_with_log)
            caption_font = ImageFont.truetype("arial.ttf", caption_size)

            drawn_img.text(xy=(caption_x, caption_y), text=caption, fill=caption_color, font=caption_font)

            # Save the edited image
            img.save(image_path)
