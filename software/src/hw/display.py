from waveshare_epd import epd4in0e   # ovladač z repozitáře reFrame (složka waveshare_epd)

class Display:
    """Waveshare 4" e-Paper HAT+ (E). Piny řeší ovladač: RST=17, DC=25, BUSY=24, PWR=18, SPI0 CE0."""
    def __init__(self):
        self.epd = epd4in0e.EPD()

    def show(self, img):                 # img: PIL RGB 600x400 (už dithered)
        self.epd.init()
        self.epd.display(self.epd.getbuffer(img))   # ~20 s fyzické překreslení
        self.epd.sleep()                 # hluboký spánek – obraz drží bez napájení
