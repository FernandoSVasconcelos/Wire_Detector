import sys
packages = 'media/nvidia/SSD/vegetacao-codes/source/main/process/utils/Wire_Detector'
sys.path.insert(0, packages)

from Wire_Detector.SetWire import Wire

class testParams:
	def __init__(self, newWire, imagem_fonte, var_filtro, var_thresh, var_kernel, var_teta, var_min_length, var_max_gap) -> None:
		self._imagem_fonte : str = imagem_fonte
		self._newWire : Wire = newWire
		self._line_vector : list = []
		self._image_vector : list = []
		self.get_vector(var_filtro, var_thresh, var_kernel, var_teta, var_min_length, var_max_gap)

	@property
	def imagem_fonte(self) -> str:
		return self._imagem_fonte

	@imagem_fonte.setter
	def imagem_fonte(self, imagem_fonte) -> None:
		self._imagem_fonte = imagem_fonte

	@property
	def newWire(self) -> Wire:
		return self._newWire

	@newWire.setter
	def newWire(self, newWire) -> None:
		self._newWire = newWire

	@property
	def line_vector(self) -> list:
		return self._line_vector
	
	@line_vector.setter
	def line_vector(self, line_vector) -> None:
		self._line_vector = line_vector

	@property
	def image_vector(self) -> list:
		return self._image_vector

	@image_vector.setter
	def image_vector(self, image_vector) -> None:
		self._image_vector = image_vector

	def testar_parametros_thresh(self, var_filtro, var_thresh) -> None:
		self._image_fonte = self._newWire.setThresh(var_filtro, var_thresh)

	def testar_parametros_morph(self, var_kernel) -> None:
		self._image_fonte = self._newWire.setMorph(var_kernel)

	def testar_parametros_filter(self) -> None:
		self._image_fonte = self._newWire.setFilter()

	def testar_probHough(self, var_teta, var_min_length, var_max_gap) -> None:
		self._line_vector, self._image_vector = self._newWire.probHough(var_teta, var_min_length, var_max_gap)
		
	def get_vector(self, var_filtro, var_thresh, var_kernel, var_teta, var_min_length, var_max_gap) -> None:
		self.testar_parametros_thresh(var_filtro, var_thresh)
		self.testar_parametros_morph(var_kernel)
		self.testar_parametros_filter()
		self.testar_probHough(var_teta, var_min_length, var_max_gap)

	def __add__(self, x : list, y : int) -> str:
		return x.append(y)

	def __str__(self) -> str:
		return(f"Line Vector: {self._line_vector}")
