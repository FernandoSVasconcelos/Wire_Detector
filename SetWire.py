import cv2 as cv
import numpy as np

class Wire:
	def __init__(self, caminho_imagem : str, imagem_fonte : str, box : list) -> None:
		self.caminho_imagem : str = caminho_imagem
		self.imagem_fonte : str = imagem_fonte
		self.box : list = box

	@property
	def imagem_fonte(self) -> str:
		return self._imagem_fonte

	@imagem_fonte.setter
	def imagem_fonte(self, imagem_fonte) -> None:
		self._imagem_fonte = imagem_fonte

	def setThresh(self, varFilter : int, varThresh : int) -> list:
		_, self._imagem_fonte = cv.threshold(self._imagem_fonte, varThresh, 255, varFilter)
		return self._imagem_fonte

	def setMorph(self, varKernel : int) -> list:
		#Pode ser ELLIPSE ou CROSS ao invés de RECT
		kernel = cv.getStructuringElement(cv.MORPH_RECT,(varKernel, varKernel))
		self._imagem_fonte = cv.morphologyEx(self._imagem_fonte, cv.MORPH_OPEN, kernel)
		return self._imagem_fonte

	def setFilter(self) -> list:
		self._imagem_fonte = cv.bilateralFilter(self._imagem_fonte, 7, 130, 75)
		self._imagem_fonte = cv.Canny(self._imagem_fonte, 50, 200, None, 3)
		return self._imagem_fonte

	def probHough(self, varTeta : int, varMinlength : int, varMaxgap : int) -> list:
		image_vector = cv.cvtColor(self._imagem_fonte, cv.COLOR_GRAY2BGR)
		line_vector = []
		line_vector = cv.HoughLinesP(self._imagem_fonte, 1,  (np.pi / 180), varTeta, None, varMinlength, varMaxgap) 
		return line_vector, image_vector

	def save(self, imagem_fonte : list, caminho_imagem : str) -> None:
		pass
		"""caminho_imagem = caminho_imagem.split('.')
		caminho_imagem[3] = 'linhas'
		caminho_imagem = caminho_imagem[0] + '.' + caminho_imagem[1] + '.' + caminho_imagem[2] + '.' + caminho_imagem[3] + '.' + caminho_imagem[4]
		cv.imwrite("/media/nvidia/SSD/vegetacao-codes/source/main/process/utils/img_to_merge/" + caminho_imagem, imagem_fonte)"""
