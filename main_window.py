import string
import time 
import random
import os
from PySide2.QtWidgets import QMainWindow, QFileDialog, QFrame, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget


class MainWindow(QMainWindow):
    def __init__(self, ui_file_path):
        super(MainWindow, self).__init__()
        self._setup_ui(ui_file_path)
        self._ui.setWindowTitle("CBMR")
    
    def _load_ui_file(self, ui_file_path):
        loader = QUiLoader()
        self._ui = loader.load(ui_file_path)
    
    def _create_main_video_player(self):
        self._player = QMediaPlayer()
        vw = QVideoWidget()
        vw.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._ui.video_player_layout.addWidget(vw)
        self._player.setVideoOutput(vw)
    
    def _connect_signals(self):
        self._ui.play_button.clicked.connect(self._player.play)
        self._ui.pause_button.clicked.connect(self._player.pause)
        self._ui.stop_button.clicked.connect(self._player.stop)
        self._ui.vlc_button.clicked.connect(lambda: self._run_with_vlc(self._loaded_video))
        self._ui.load_image_button.clicked.connect(self._on_load_image_button_clicked)
        self._ui.load_video_button.clicked.connect(self._on_load_video_button_clicked)
        self._ui.save_image_button.clicked.connect(self._on_save_image_button_clicked)
        self._ui.save_video_button.clicked.connect(self._on_save_video_button_clicked)
        self._ui.search_image_button.clicked.connect(self._on_search_image_button_clicked)
        self._ui.search_video_button.clicked.connect(self._on_search_video_button_clicked)
    
    def _setup_ui(self, ui_file_path):
        self._load_ui_file(ui_file_path)
        self._loaded_image = ""
        self._loaded_video = ""
        self._create_main_video_player()
        self._ui.mean_color_radio_button.setChecked(True)
        self._ui.mean_color_radio_button_2.setChecked(True)
        self._connect_signals()
        
    
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
    
    def _on_search_video_button_clicked(self):
        if not self._loaded_video:
            return
        self._set_loading_state(self._ui.search_video_button, True, "Searching...")
        if self._ui.mean_color_radio_button_2.isChecked():
            print("mean checked")
        elif self._ui.color_histogram_button_2.isChecked():
            print("histo is checked")
        elif self._ui.object_detection_radio_button_2.isChecked():
            print("object is checked")
        videos = ["/home/omar/Videos/rviz_2.mp4", "/home/omar/Videos/rviz_2.mp4", "/home/omar/Videos/rviz_2.mp4"]
        self._load_videos(videos)
        self._set_loading_state(self._ui.search_video_button, False, "Search Video")
    
    def _color_label(self, label, color):
        label.setStyleSheet("color: {}".format(color))
    
    def _set_image(self, frame, image):
        frame.setStyleSheet("image: url({})".format(image))
    
    def _on_save_image_button_clicked(self):
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
    
    def _on_save_video_button_clicked(self):
        self._set_loading_state(self._ui.save_video_button, True, "Saving...")
        ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
        result = QFile.copy(self._loaded_video,"videos/{}.{}".format(ran, self._loaded_video.split(".")[-1]))
        if not result:
            self._ui.video_saved_label.setText("Video not saved!")
            self._color_label(self._ui.video_saved_label, "red")
            self._set_loading_state(self._ui.save_video_button, False, "Save Video")
            return
        self._ui.video_saved_label.setText("Video saved successfully!")
        self._color_label(self._ui.video_saved_label, "blue")
        print("here")
        self._set_loading_state(self._ui.save_video_button, True, "Save Video")

    def _run_with_vlc(self, video):
        if video:
            vlc_command = 'vlc "{}"'.format(video)
            os.system(vlc_command)

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
    
    def _on_load_video_button_clicked(self):
        video_path, _ = QFileDialog.getOpenFileUrl(self, "Open Video", "", "Video Files (*.mp4 *.mov *.wmv *.avi)")
        video_path = video_path.path()
        if not video_path:
            self._ui.video_loaded_label.setText("Video not loaded!")
            self._color_label(self._ui.video_loaded_label, "red")
            return
        self._player.setMedia(QUrl.fromLocalFile(video_path))
        self._ui.video_loaded_label.setText("Video loaded successfully!")
        self._color_label(self._ui.video_loaded_label, "blue")
        self._ui.save_video_button.setDisabled(False)
        self._ui.video_saved_label.setText("")
        self._loaded_video = video_path
        self._player.pause()

    def _clear_layout(self, layout):
        while True:
            child = layout.takeAt(0)
            if child == None:
                break
            del child
    
    def _load_images(self, images):
        self._clear_layout(self._ui.image_results_layout)
        for image in images:
            image_frame = QFrame(self)
            self._set_image(image_frame, image)
            image_frame.setMinimumSize(500,300)
            self._ui.image_results_layout.addWidget(image_frame)
    
    def _create_video_player(self, video):
        vw_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        player = QMediaPlayer(self)
        vw = QVideoWidget()
        play_button = QPushButton("play")
        pause_button = QPushButton("pause")
        stop_button = QPushButton("stop")
        vlc_button = QPushButton("open in vlc")
        play_button.clicked.connect(player.play)
        pause_button.clicked.connect(player.pause)
        stop_button.clicked.connect(player.stop)
        vlc_button.clicked.connect(lambda: self._run_with_vlc(video))
        buttons_layout.addWidget(play_button)
        buttons_layout.addWidget(pause_button)
        buttons_layout.addWidget(stop_button)
        buttons_layout.addWidget(vlc_button)
        vw_layout.addWidget(vw)
        vw_layout.addLayout(buttons_layout)
        vw.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        vw.setMinimumSize(500,270)
        self._ui.video_results_layout.addLayout(vw_layout)
        player.setVideoOutput(vw)
        player.setMedia(QUrl.fromLocalFile(video))
        player.pause()
    
    def _load_videos(self, videos):
        self._clear_layout(self._ui.video_results_layout)
        for video in videos:
            self._create_video_player(video)
        
    def show(self):
        self._ui.show()




