class WireFlag:
	def __init__(self) -> None:
		self._flag : bool = False
		self._x_inicial : list = []
		self._x_final : list = []
		self._y_inicial : list = []
		self._y_final : list = []

	@property
	def flag(self) -> bool:
		return self._flag

	@flag.setter
	def flag(self, flag : bool) -> None:
		self._flag = flag

	@property
	def x_inicial(self) -> list:
		return self._x_inicial

	@x_inicial.setter
	def x_inicial(self, x_inicial : list) -> None:
		self._x_inicial = x_inicial

	@property
	def x_final(self) -> list:
		return self._x_final

	@x_final.setter
	def x_final(self, x_final : list) -> None:
		self._x_final = x_final

	@property
	def y_inicial(self) -> list:
		return self._y_inicial

	@y_inicial.setter
	def y_inicial(self, y_inicial : list) -> None:
		self._y_inicial = y_inicial

	@property
	def y_final(self) -> list:
		return self._y_final

	@y_final.setter
	def y_final(self, y_final : list) -> None:
		self._y_final = y_final

	def __add__(self, x : list, y : int) -> str:
		return x.append(y)

	def __str__(self) -> str:
		return(f"X0: {self._x_inicial}\nX1: {self._x_final}\nY0: {self._y_inicial}\nY1: {self._y_final}\nFlag: {self._flag}")
