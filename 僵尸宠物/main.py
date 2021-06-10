# *_* coding : UTF-8 *_*

import os
import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyLabel(QLabel):
	transformation_signal = pyqtSignal(int)
	transpeed_signal = pyqtSignal(str)

	def __init__(self, *args):
		super().__init__(*args)
		# 声明
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		# 开放右键策略
		self.customContextMenuRequested.connect(self.rightMenuShow)

	# 添加右键菜单
	def rightMenuShow(self):
		menu = QMenu(self)
		transformation1 = QAction(QIcon(r'resources\graphics\Zombies\NormalZombie\Zombie\Zombie_0.png'), self.name[0],
								  self, triggered=lambda: self.transformation_signal.emit(0))
		transformation2 = QAction(
			QIcon(r'resources\graphics\Zombies\ConeheadZombie\ConeheadZombie\ConeheadZombie_0.png'), self.name[1], self,
			triggered=lambda: self.transformation_signal.emit(1))
		transformation3 = QAction(QIcon(r'resources\graphics\Zombies\FlagZombie\FlagZombie\FlagZombie_0.png'),
								  self.name[2], self, triggered=lambda: self.transformation_signal.emit(2))
		transformation4 = QAction(
			QIcon(r'resources\graphics\Zombies\BucketheadZombie\BucketheadZombie\BucketheadZombie_0.png'), self.name[3],
			self, triggered=lambda: self.transformation_signal.emit(3))
		transformation5 = QAction(
			QIcon(r'resources/graphics/Zombies/NewspaperZombie/NewspaperZombie/NewspaperZombie_0.png'), self.name[4],
			self, triggered=lambda: self.transformation_signal.emit(4))
		transformation = QMenu('换装', self)
		transformation.addAction(transformation1)
		transformation.addAction(transformation2)
		transformation.addAction(transformation3)
		transformation.addAction(transformation4)
		transformation.addAction(transformation5)

		transpeed1 = QAction(self.name_1[0], self, triggered=lambda: self.transpeed_signal.emit('+'))
		transpeed2 = QAction(self.name_1[1], self, triggered=lambda: self.transpeed_signal.emit('-'))
		transpeed3 = QAction(self.name_1[2], self, triggered=lambda: self.transpeed_signal.emit('stop'))
		transpeed4 = QAction(self.name_1[3], self, triggered=lambda: self.transpeed_signal.emit('start'))
		transpeed = QMenu('变速', self)
		transpeed.addAction(transpeed1)
		transpeed.addAction(transpeed2)
		transpeed.addAction(transpeed3)
		transpeed.addAction(transpeed4)

		menu.addMenu(transpeed)
		menu.addMenu(transformation)
		menu.addSeparator()
		menu.addAction(QAction('置顶', self, triggered=lambda: self.transpeed_signal.emit('top')))
		menu.addAction(QAction('隐藏', self, triggered=self.hide))
		menu.addAction(QAction('退出', self, triggered=self.quit))
		menu.exec_(QCursor.pos())

	def quit(self):
		self.close()
		sys.exit()

	def hide(self):
		self.setVisible(False)


def check_files(func):
	def main(*args, **kwargs):
		print('check')
		if os.path.exists('resources'):
			func(*args, **kwargs)
		else:
			QMessageBox(
		QMessageBox.Warning, '警告', '       未发现资源文件夹\n           无法运行\n请检查resources文件夹是否在同一目录').exec_()
			exit()

	return main


class TablePet(QWidget):
	@check_files
	def __init__(self):
		super(TablePet, self).__init__()

		self.is_follow_mouse = False
		self.mouse_drag_pos = self.pos()
		# 每隔一段时间做个动作
		self.timer = QTimer()
		self.timer.timeout.connect(self.randomAct)
		self.timer.start(100)

		self.name = ('普通僵尸', '路障僵尸', '旗帜僵尸', '铁桶僵尸', '报纸僵尸')
		self.name_1 = ('加速', '减速', '停止运动', '恢复运动')
		##僵尸形态
		self.sharp = 0
		##皇帝的新衣
		self.clothes = ''
		self.clothes_key = 0

		# 初始化步频
		self.step_frequency = 2

		# 初始化置顶方式
		self.top_way = True

		self.wardrobe(self.sharp)
		self.initUi()
		self.tray()

	##衣柜
	def wardrobe(self, key):
		default = r'resources\graphics\Zombies\NormalZombie\Zombie\Zombie_'
		battle = r'resources\graphics\Zombies\ConeheadZombie\ConeheadZombie\ConeheadZombie_'
		flag = r'resources\graphics\Zombies\FlagZombie\FlagZombie\FlagZombie_'
		Bucket = r'resources\graphics\Zombies\BucketheadZombie\BucketheadZombie\BucketheadZombie_'
		newspaper = r'resources\graphics\Zombies\NewspaperZombie\NewspaperZombie\NewspaperZombie_'

		if key == 0:
			self.clothes = default
			##TODO 根据文件数自动获取
			self.clothes_key = 21
		elif key == 1:
			self.clothes = battle
			self.clothes_key = 20
		elif key == 2:
			self.clothes = flag
			self.clothes_key = 11
		elif key == 3:
			self.clothes = Bucket
			self.clothes_key = 14
		elif key == 4:
			self.clothes = newspaper
			self.clothes_key = 18

	def transpeed(self, key):
		print(key)
		if key == '-' and self.step_frequency >= 1:
			self.step_frequency -= 1
		elif key == '+':
			self.step_frequency += 1
		elif key == 'stop':
			self.step_frequency = 0
		elif key == 'start':
			self.step_frequency = 2
		elif key == 'top':
			self.topshow()

	##变身
	def transformation(self):
		if self.sharp == 0:
			self.wardrobe(1)
			self.sharp = 1
		else:
			self.wardrobe(0)
			self.sharp = 0

	def randomAct(self):
		# 读取图片不同的地址，实现动画效果
		if self.key < self.clothes_key:
			self.key += 1
		else:
			self.key = 0

		self.pic_url = self.clothes + str(self.key) + '.png'
		self.pm = QPixmap(self.pic_url)
		if not self.is_follow_mouse:
			# 实现行进效果
			if self.w > 0:
				self.w -= self.step_frequency
			else:
				self.w = QDesktopWidget().screenGeometry().width() - 150
			self.move(self.w, self.h)
		self.lbl.setPixmap(self.pm)

	def initUi(self):
		# width() height()
		# print(QDesktopWidget().screenGeometry())
		screen = QDesktopWidget().screenGeometry()
		random_num = random.randint(0, screen.height() // 100)
		self.w = screen.width() - 150
		self.h = random_num * 100 + (screen.height() - (screen.height() // 100) * 100) - 150
		# print(self.h,screen.height()-150)
		if self.h < 150:
			self.h += 150
		elif self.h == screen.height() - 150:
			self.h -= 50
		# print(self.h)
		self.setGeometry(self.w, self.h, 300, 300)
		# self.setWindowTitle('mypet')
		self.lbl = MyLabel(self)
		self.lbl.name = self.name
		self.lbl.name_1 = self.name_1
		self.lbl.transformation_signal.connect(lambda a: self.wardrobe(a))
		self.lbl.transpeed_signal.connect(lambda a: self.transpeed(a))
		self.key = 0
		self.pic_url = self.clothes + str(self.key) + '.png'
		self.pm = QPixmap(self.pic_url)
		self.lbl.setPixmap(self.pm)

		# 背景透明等效果
		# Qt.SubWindow 会隐去icon图标+下面不会有窗口点击办法
		# Qt.FramelessWindowHint 去除最上面的框
		# Qt.WindowStaysOnTopHint 顶端显示
		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
		# 禁止填充背景色
		self.setAutoFillBackground(False)
		# 窗口透明显示
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.show()

	# self.repaint()

	# 系统托盘
	def tray(self):
		tp = QSystemTrayIcon(self)
		tp.setIcon(QIcon(r'resources\graphics\main.ico'))
		ation_quit = QAction('退出', self, triggered=self.quit)
		transformation1 = QAction(QIcon(r'resources\graphics\Zombies\NormalZombie\Zombie\Zombie_0.png'), self.name[0],
								  self, triggered=lambda: self.wardrobe(0))
		transformation2 = QAction(
			QIcon(r'resources\graphics\Zombies\ConeheadZombie\ConeheadZombie\ConeheadZombie_0.png'), self.name[1], self,
			triggered=lambda: self.wardrobe(1))
		transformation3 = QAction(QIcon(r'resources\graphics\Zombies\FlagZombie\FlagZombie\FlagZombie_0.png'),
								  self.name[2], self, triggered=lambda: self.wardrobe(2))
		transformation4 = QAction(
			QIcon(r'resources\graphics\Zombies\BucketheadZombie\BucketheadZombie\BucketheadZombie_0.png'), self.name[3],
			self, triggered=lambda: self.wardrobe(3))
		transformation5 = QAction(
			QIcon(r'resources/graphics/Zombies/NewspaperZombie/NewspaperZombie/NewspaperZombie_0.png'), self.name[4],
			self, triggered=lambda: self.wardrobe(4))
		display = QAction('显示', self, triggered=self.display)
		topshow = QAction('置顶', self, triggered=self.topshow)

		transformation = QMenu('换装', self)
		transformation.addAction(transformation1)
		transformation.addAction(transformation2)
		transformation.addAction(transformation3)
		transformation.addAction(transformation4)
		transformation.addAction(transformation5)

		transpeed1 = QAction(self.name_1[0], self, triggered=lambda: self.transpeed('+'))
		transpeed2 = QAction(self.name_1[1], self, triggered=lambda: self.transpeed('-'))
		transpeed3 = QAction(self.name_1[2], self, triggered=lambda: self.transpeed('stop'))
		transpeed4 = QAction(self.name_1[3], self, triggered=lambda: self.transpeed('start'))
		transpeed = QMenu('变速', self)
		transpeed.addAction(transpeed1)
		transpeed.addAction(transpeed2)
		transpeed.addAction(transpeed3)
		transpeed.addAction(transpeed4)

		tpMenu = QMenu(self)
		tpMenu.addMenu(transpeed)
		tpMenu.addMenu(transformation)
		tpMenu.addSeparator()

		tpMenu.addAction(topshow)
		tpMenu.addAction(display)
		tpMenu.addAction(ation_quit)
		tp.setContextMenu(tpMenu)
		tp.show()
		'''添加双击显示/隐藏桌面宠物'''
		tp.activated[QSystemTrayIcon.ActivationReason].connect(self.icon_activated)

	def icon_activated(self, reason):
		""" 双击显示/隐藏桌面宠物 """
		if reason == QSystemTrayIcon.DoubleClick:
			print(self.lbl.isVisible())
			if self.lbl.isVisible():
				self.hide()
			else:
				self.show()

	# 鼠标事件
	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.is_follow_mouse = True
			self.mouse_drag_pos = event.globalPos() - self.pos()
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))

	def mouseMoveEvent(self, event):
		if Qt.LeftButton and self.is_follow_mouse:
			self.move(event.globalPos() - self.mouse_drag_pos)
			xy = self.pos()
			self.w, self.h = xy.x(), xy.y()
			event.accept()

	def mouseReleaseEvent(self, event):
		self.is_follow_mouse = False
		self.setCursor(QCursor(Qt.ArrowCursor))

	def keyPressEvent(self, key):
		print(key.key())
		_key = key.key()
		if _key == 16777223:
			print('退出')
			self.quit()
		if _key == 16777216:
			if self.lbl.isVisible():
				self.lbl.setVisible(False)
			else:
				self.lbl.setVisible(True)
		if _key == 16777235:
			print('上')
			if self.h - 10 >= 0:
				self.h -= 20

		if _key == 16777237:
			print('下')
			if QDesktopWidget().screenGeometry().height() - 150 - self.h > 20:
				self.h += 20

		if _key == 16777234:
			print('左')
			self.w -= 20

		if _key == 16777236:
			print('右')
			if QDesktopWidget().screenGeometry().width() - 150 - self.w > 0:
				self.w += 20

		if _key == 16777217:
			self.lbl.rightMenuShow()

		if _key == 45:
			self.topshow()

	def display(self):
		self.lbl.setVisible(True)

	def topshow(self):
		if self.top_way:
			self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
			self.show()
			self.top_way = False
		else:
			print('aa')
			self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
			self.show()
			self.top_way = True

	def quit(self):
		self.close()
		sys.exit()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myPet = TablePet()
	sys.exit(app.exec_())
