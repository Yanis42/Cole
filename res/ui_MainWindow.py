# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(571, 321)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(571, 321))
        MainWindow.setMaximumSize(QSize(571, 321))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.searchGroup = QGroupBox(self.centralwidget)
        self.searchGroup.setObjectName(u"searchGroup")
        self.searchGroup.setGeometry(QRect(10, 10, 221, 301))
        self.searchBox = QLineEdit(self.searchGroup)
        self.searchBox.setObjectName(u"searchBox")
        self.searchBox.setGeometry(QRect(10, 20, 201, 21))
        self.actorFoundLabel = QLabel(self.searchGroup)
        self.actorFoundLabel.setObjectName(u"actorFoundLabel")
        self.actorFoundLabel.setGeometry(QRect(10, 280, 71, 16))
        self.actorCategoryList = QComboBox(self.searchGroup)
        self.actorCategoryList.setObjectName(u"actorCategoryList")
        self.actorCategoryList.setGeometry(QRect(10, 250, 201, 22))
        self.actorFoundBox = QListWidget(self.searchGroup)
        self.actorFoundBox.setObjectName(u"actorFoundBox")
        self.actorFoundBox.setGeometry(QRect(10, 50, 201, 192))
        self.paramGroup = QGroupBox(self.centralwidget)
        self.paramGroup.setObjectName(u"paramGroup")
        self.paramGroup.setGeometry(QRect(250, 10, 311, 301))
        self.actorTypeList = QComboBox(self.paramGroup)
        self.actorTypeList.setObjectName(u"actorTypeList")
        self.actorTypeList.setEnabled(False)
        self.actorTypeList.setGeometry(QRect(80, 20, 221, 22))
        self.actorTypeLabel = QLabel(self.paramGroup)
        self.actorTypeLabel.setObjectName(u"actorTypeLabel")
        self.actorTypeLabel.setGeometry(QRect(10, 20, 61, 21))
        self.verticalLayoutWidget = QWidget(self.paramGroup)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 50, 141, 241))
        self.paramLabelLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.paramLabelLayout.setObjectName(u"paramLabelLayout")
        self.paramLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_2 = QWidget(self.paramGroup)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(160, 50, 141, 241))
        self.paramLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.paramLayout.setSpacing(6)
        self.paramLayout.setObjectName(u"paramLayout")
        self.paramLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cole - OoT Actor Lookup", None))
        self.searchGroup.setTitle(QCoreApplication.translate("MainWindow", u"Search Actor", None))
#if QT_CONFIG(tooltip)
        self.searchBox.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.searchBox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.searchBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search...", None))
        self.actorFoundLabel.setText(QCoreApplication.translate("MainWindow", u"Found: 0", None))
        self.paramGroup.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.actorTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Actor Type", None))
    # retranslateUi

