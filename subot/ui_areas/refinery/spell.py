
from subot.ocr import OCR
from subot.settings import Config
from subot.ui_areas.base import SpeakAuto, OCRMode, SpeakCapability
from subot.ui_areas.base import FrameInfo
from subot.ocr import slice_img
from subot.ui_areas.enchanter.spell_craft_screen import center_crop

from subot.ui_areas.spell_components import ComponentSortUI, ComponentSpellDescription, ComponentSpellInfo, \
    ComponentSpellEnchanterDescription


class SalvageSpellUI(SpeakAuto):
    mode = OCRMode.SPELL_REFINERY

    def __init__(self, ocr_engine: OCR, config: Config, audio_system: SpeakCapability):
        super().__init__(ocr_engine, config, audio_system)
        self.description_component = ComponentSpellDescription(self.ocr_engine)
        self.sort_component = ComponentSortUI(self.ocr_engine)
        self.spell_info_component = ComponentSpellInfo(self.ocr_engine)
        self.help_text = f"Press {self.program_config.read_secondary_key} for description, press f to change sort order of spells"

    def ocr(self, parent: FrameInfo):
        bgr = parent.frame
        gray = parent.gray_frame
        ui_border = center_crop(gray, 21)
        bgr_cropped = bgr[ui_border.top:ui_border.bottom, ui_border.left:ui_border.right]

        spell_name_roi = slice_img(bgr_cropped, x_start=0.00, x_end=0.45, y_start=0.00, y_end=1.0)
        self.spell_info_component.ocr(spell_name_roi)

        spell_description_roi = slice_img(bgr_cropped, x_start=0.46, x_end=1.0, y_start=0.09, y_end=0.9)
        self.description_component.ocr(spell_description_roi)

        sort_text_roi = slice_img(bgr_cropped, x_start=0.75, x_end=1.0, y_start=0.0, y_end=0.09)
        self.sort_component.ocr(sort_text_roi)

    def speak_interaction(self):
        self.audio_system.speak_nonblocking(self.description_component.description)

    @property
    def is_same_state(self) -> bool:
        return self.spell_info_component.is_same_state and self.sort_component.is_same_state

    def speak_auto(self):
        if self.is_same_state:
            return

        sort_text = self.sort_component.new_text

        spell_gem_text = f"{self.spell_info_component.spell_name}, {self.spell_info_component.spell_class.name} class"

        text = f"{spell_gem_text}. {sort_text}"
        self.audio_system.speak_nonblocking(text)

