from resources import HEX_COLOUR_BLUE
from base_context import ContextCheckBox, IMAGE_ROOT


class NodesCheckBox(ContextCheckBox):
    COLOUR = HEX_COLOUR_BLUE

    def __init__(self, *args, **kwargs):
        super(NodesCheckBox, self).__init__(*args, **kwargs)
        self.setText("Nodes")
        self.setStyleSheet("""
            QCheckBox::indicator:unchecked {
                image: url(%s/images/blue_checkbox_unchecked.png);
            }

            QCheckBox::indicator:unchecked:hover {
                image: url(%s/images/blue_checkbox_unchecked_hover.png);
            }

            QCheckBox::indicator:unchecked:pressed {
                image: url(%s/images/blue_checkbox_unchecked_pressed.png);
            }

            QCheckBox::indicator:checked {
                image: url(%s/images/blue_checkbox_checked.png);
            }

            QCheckBox::indicator:checked:hover {
                image: url(%s/images/blue_checkbox_checked_hover.png);
            }

            QCheckBox::indicator:checked:pressed {
                image: url(%s/images/blue_checkbox_checked_pressed.png);
            }
            """ % (IMAGE_ROOT, IMAGE_ROOT, IMAGE_ROOT, IMAGE_ROOT, IMAGE_ROOT, IMAGE_ROOT))
