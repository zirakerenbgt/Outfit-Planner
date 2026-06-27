import sys
import json

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QListWidget,
    QLineEdit
)

from PyQt5.QtGui import (
    QPixmap,
    QPainter
)

from PyQt5.QtCore import Qt


class OutfitApp(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Dress Up Outfit"
        )

        self.resize(
            950,
            720
        )

        self.tops = [
            "hoodie",
            "tshirt",
            "bandshirt",
            "bluesweater",
            "formalshirt",
            "hoodie",
            "jeanjacket",
            "jersey",
            "lace",
            "layeredblouse",
            "leatherjacket",
            "redshirt",
            "snoopysweater",
            "vintagejacket"
        ]

        self.bottoms = [
            "fancyjeans",
            "redsweatpants",
            "starjeans",
            "straightjeans",
            "strippedjeans"
        ]

        self.shoes = [
            "sneakers",
            "blackflats",
            "blackheels",
            "bluesamba",
            "brownadidas",
            "converse",
            "newbalances",
            "yellowonit"
        ]

        main = QHBoxLayout()

        left = QVBoxLayout()

        self.outfit_name = QLineEdit()

        self.outfit_name.setPlaceholderText(
            "Outfit name..."
        )

        self.top_box = QComboBox()
        self.top_box.addItems(
            self.tops
        )

        self.bottom_box = QComboBox()
        self.bottom_box.addItems(
            self.bottoms
        )

        self.shoes_box = QComboBox()
        self.shoes_box.addItems(
            self.shoes
        )

        self.save_btn = QPushButton(
            "Save Outfit"
        )

        self.load_btn = QPushButton(
            "Load Outfit"
        )

        self.delete_btn = QPushButton(
            "Delete Outfit"
        )

        self.saved_list = QListWidget()

        left.addWidget(
            QLabel("Outfit Name")
        )

        left.addWidget(
            self.outfit_name
        )

        left.addWidget(
            QLabel("Choose Top")
        )

        left.addWidget(
            self.top_box
        )

        left.addWidget(
            QLabel("Choose Bottom")
        )

        left.addWidget(
            self.bottom_box
        )

        left.addWidget(
            QLabel("Choose Shoes")
        )

        left.addWidget(
            self.shoes_box
        )

        left.addWidget(
            self.save_btn
        )

        left.addWidget(
            self.load_btn
        )

        left.addWidget(
            self.delete_btn
        )

        left.addWidget(
            QLabel(
                "Saved Outfit"
            )
        )

        left.addWidget(
            self.saved_list
        )

        self.preview = QLabel()

        self.preview.setFixedSize(
            450,
            650
        )

        main.addLayout(
            left
        )

        main.addWidget(
            self.preview
        )

        self.setLayout(
            main
        )

        self.top_box.currentTextChanged.connect(
            self.update_preview
        )

        self.bottom_box.currentTextChanged.connect(
            self.update_preview
        )

        self.shoes_box.currentTextChanged.connect(
            self.update_preview
        )

        self.save_btn.clicked.connect(
            self.save_outfit
        )

        self.load_btn.clicked.connect(
            self.load_saved
        )

        self.delete_btn.clicked.connect(
            self.delete_outfit
        )

        self.refresh_saved()

        self.update_preview()

    def update_preview(self):

        canvas = QPixmap(
            450,
            650
        )

        canvas.fill(
            Qt.white
        )

        painter = QPainter(
            canvas
        )

        sections = [

            (
                "top_"
                + self.top_box.currentText()
                + ".png",

                0,

                220
            ),

            (
                "bottom_"
                + self.bottom_box.currentText()
                + ".png",

                220,

                220
            ),

            (
                "shoes_"
                + self.shoes_box.currentText()
                + ".png",

                440,

                180
            )

        ]

        for file, y, h in sections:

            pix = QPixmap(
                file
            )

            if not pix.isNull():

                pix = pix.scaled(

                    220,

                    h,

                    Qt.KeepAspectRatio,

                    Qt.SmoothTransformation

                )

                x = (
                    450
                    -
                    pix.width()
                ) // 2

                y2 = (
                    y
                    +
                    (
                        h
                        -
                        pix.height()
                    ) // 2
                )

                painter.drawPixmap(
                    x,
                    y2,
                    pix
                )

        painter.end()

        self.preview.setPixmap(
            canvas
        )

    def load_data(self):

        try:

            with open(
                "saved_outfits.json",
                "r"
            ) as file:

                return json.load(
                    file
                )

        except:

            return []

    def save_outfit(self):

        data = self.load_data()

        name = (
            self.outfit_name.text()
            .strip()
        )

        if name == "":

            name = (
                "Untitled Outfit"
            )

        data.append({

            "name":
            name,

            "top":
            self.top_box.currentText(),

            "bottom":
            self.bottom_box.currentText(),

            "shoes":
            self.shoes_box.currentText()

        })

        with open(
            "saved_outfits.json",
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        self.refresh_saved()

    def refresh_saved(self):

        self.saved_list.clear()

        for outfit in self.load_data():

            self.saved_list.addItem(

                outfit["name"]

            )

    def load_saved(self):

        idx = (
            self.saved_list.currentRow()
        )

        if idx == -1:

            return

        outfit = self.load_data()[

            idx

        ]

        self.outfit_name.setText(
            outfit["name"]
        )

        self.top_box.setCurrentText(
            outfit["top"]
        )

        self.bottom_box.setCurrentText(
            outfit["bottom"]
        )

        self.shoes_box.setCurrentText(
            outfit["shoes"]
        )

    def delete_outfit(self):

        idx = (
            self.saved_list.currentRow()
        )

        if idx == -1:

            return

        data = self.load_data()

        data.pop(
            idx
        )

        with open(
            "saved_outfits.json",
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        self.refresh_saved()


app = QApplication(
    sys.argv
)

window = OutfitApp()

window.show()

sys.exit(
    app.exec_()
)