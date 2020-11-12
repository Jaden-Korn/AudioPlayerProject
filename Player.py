import codecs
import os
import sys

from MainWindow import *
from pygame import mixer


class AudioPlayer(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        mixer.init()

        path_to_music = os.getcwd() + '\\root.txt'
        if os.path.exists(path_to_music):
            file = open(u'' + path_to_music)
            self.ui.lineEdit.setText(file.read().strip())
            file.close()
            self.path_to_the_file = None

        self.ui.pushButton_3.clicked.connect(self.scanning)
        self.ui.listWidget.currentTextChanged.connect(self.files)
        self.ui.listWidget_2.currentTextChanged.connect(self.stop)
        self.ui.pushButton_4.clicked.connect(self.pause)
        self.ui.pushButton.clicked.connect(self.play)
        self.ui.pushButton_2.clicked.connect(self.stop)
        self.songs = []
        self.is_pause = False
        self.have_files_to_play = False
        self.scanning()

    def scanning(self):
        path_to_the_file = list()
        folders_with_the_files = list()
        path_to_scanning = str(self.ui.lineEdit.text()).strip()
        file = codecs.open(u'' + os.getcwd() + '\\root.txt', 'w', 'utf8')
        file.write(path_to_scanning)
        file.close()

        for root, dirs, files in os.walk(path_to_scanning):
            for file in files:
                if file.split('.')[-1] == 'mp3':
                    path_to_the_file.append(os.path.join(root, file))
                    folders_with_the_files.append(os.path.join(root, file).split('\\')[-2])
        folders_with_the_files = dict(zip(folders_with_the_files, folders_with_the_files)).values()
        self.path_to_the_file = path_to_the_file
        self.ui.listWidget.clear()
        for folder in folders_with_the_files:
            self.ui.listWidget.addItem(folder.strip())

    def files(self):
        try:
            self.have_files_to_play = True
            self.songs = list()
            self.ui.listWidget_2.clear()
            name_of_folder = self.ui.listWidget.currentItem().text()
            for path in self.path_to_the_file:
                path_to_the_file = path.split('\\')[-2]
                if name_of_folder == path_to_the_file:
                    self.songs.append(path)
                    self.ui.listWidget_2.addItem(path.split('\\')[-1])
            self.ui.listWidget_2.setFocus()
            self.have_files_to_play = False
        except AttributeError:
            pass

    def play(self):
        try:
            if not self.have_files_to_play:
                number_of_song = self.ui.listWidget_2.currentRow()
                full_path_to_file = self.songs[number_of_song]
                mixer.music.stop()
                mixer.music.load(u'' + full_path_to_file)
                mixer.music.play()
        except IndexError:
            pass

    def stop(self):
        mixer.music.stop()

    def pause(self):
        if not self.is_pause:
            mixer.music.pause()
            self.is_pause = True
        elif self.is_pause:
            mixer.music.unpause()
            self.is_pause = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = AudioPlayer()
    ex.show()
    sys.exit(app.exec_())
