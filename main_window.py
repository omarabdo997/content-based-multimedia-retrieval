import string 
import random
from PySide2.QtWidgets import QMainWindow, QFileDialog, QFrame
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile


class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super(MainWindow, self).__init__()
        self._setup_ui(ui_file_path)
    
    def _load_ui_file(self, ui_file_path):
        loader = QUiLoader()
        self._ui = loader.load(ui_file_path)
    
    def _setup_ui(self, ui_file_path):
        self._load_ui_file(ui_file_path)
        self._loaded_image = ""
        self._ui.mean_color_radio_button.setChecked(True)
        self._ui.load_image_button.clicked.connect(self._on_load_image_button_clicked)
        self._ui.save_image_button.clicked.connect(self._on_save_image_button_clicked)
        self._ui.search_image_button.clicked.connect(self._on_search_image_button_clicked)
    
    def _set_loading_state(self, button, isDisabled, text):
        button.setDisabled(isDisabled)
        button.setText(text)
  
    def _on_search_image_button_clicked(self):
        if not self._loaded_image:
            return
        self._set_loading_state(self._ui.search_image_button, True, "Searching...")
        if self._ui.mean_color_radio_button.isChecked():
            print("mean checked")
        elif self._ui.color_histogram_button.isChecked():
            print("histo is checked")
        elif self._ui.object_detection_radio_button.isChecked():
            print("object is checked")
        images = ["/home/omar/Documents/content-based-multimedia-retrieval/images/h7zi9s76lv.jpg", "/home/omar/Documents/content-based-multimedia-retrieval/images/h7zi9s76lv.jpg", "/home/omar/Documents/content-based-multimedia-retrieval/images/h7zi9s76lv.jpg", "/home/omar/Documents/content-based-multimedia-retrieval/images/j49yaunz7o.png"]
        self._load_images(images)
        self._set_loading_state(self._ui.search_image_button, False, "Search Image")
    
    def _color_label(self, label, color):
        label.setStyleSheet("color: {}".format(color))
    
    def _set_image(self, frame, image):
        frame.setStyleSheet("image: url({})".format(image))
    
    def _on_save_image_button_clicked(self, is_image = 1):
        self._set_loading_state(self._ui.save_image_button, True, "Saving...")
        ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
        result = QFile.copy(self._loaded_image,"images/{}.{}".format(ran, self._loaded_image.split(".")[-1]))
        if not result:
            self._ui.image_saved_label.setText("Image not saved!")
            self._color_label(self._ui.image_saved_label, "red")
            self._set_loading_state(self._ui.save_image_button, False, "Save Image")
            return
        self._ui.image_saved_label.setText("Image saved successfully!")
        self._color_label(self._ui.image_saved_label, "blue")
        self._set_loading_state(self._ui.save_image_button, True, "Save Image")

    
    def _on_load_image_button_clicked(self):
        image_path, _ = QFileDialog.getOpenFileUrl(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        image_path = image_path.path()
        if not image_path:
            self._ui.image_loaded_label.setText("Image not loaded!")
            self._color_label(self._ui.image_loaded_label, "red")
            return
        self._ui.image_frame.setStyleSheet("image: url({})".format(image_path))
        self._ui.image_loaded_label.setText("Image loaded successfully!")
        self._color_label(self._ui.image_loaded_label, "blue")
        self._ui.save_image_button.setDisabled(False)
        self._ui.image_saved_label.setText("")
        self._loaded_image = image_path
    
    def _load_images(self, images):
        print (5!=2)
        while True:
            child = self._ui.image_results_layout.takeAt(0)
            if child == None:
                break
            del child
        for image in images:
            image_frame = QFrame(self)
            self._set_image(image_frame, image)
            image_frame.setMinimumSize(500,300)
            self._ui.image_results_layout.addWidget(image_frame)
        
    def show(self):
        self._ui.show()




