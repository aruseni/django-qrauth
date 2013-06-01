try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw

import qrcode.image.base
import qrcode.image.pil

class PilImage(qrcode.image.pil.PilImage):
    def __init__(self, border, width, box_size):
        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        qrcode.image.base.BaseImage.__init__(self, border, width, box_size)
        self.kind = "PNG"

        pixelsize = (self.width + self.border * 2) * self.box_size
        self._img = Image.new("RGBA", (pixelsize, pixelsize))
        self._idr = ImageDraw.Draw(self._img)

def make_qr_code(string):
    return qrcode.make(string, box_size=10, border=1, image_factory=PilImage)
