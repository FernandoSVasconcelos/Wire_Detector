import math
import cv2 as cv
import numpy as np

from typing import List, Union

class Operation:
	def __init__(self, line_vector : List[float], image_vector : List[float]) -> None:
		self._line_vector = line_vector
		self._image_vector = image_vector

	@property
	def line_vector(self) -> List[float]:
		return self._line_vector

	@line_vector.setter
	def line_vector(self, line_vector : List[float]) -> None:
		self._line_vector = line_vector

	@property
	def image_vector(self) -> List[float]:
		return self._image_vector

	@image_vector.setter
	def image_vector(self, image_vector : List[float]) -> None:
		self._image_vector = image_vector

	def paralelo(self, line_vector : List[float], image_vector : List[float]) -> Union[List, List]:
		media_x0 : float = 0
		media_x1 : float = 0
		media_y0 : float = 0
		media_y1 : float = 0

		ponto_media_LX : float = 0
		ponto_media_LY : float = 0
		media_distancias : float = 0

		linhas_novas : List[float] = []
		vetor_distancias : List[float] = []

		height, width, channels = image_vector.shape
		raio = (height + width) // (channels * 2)

		for i in range(len(line_vector)):
			l = line_vector[i][0]
			media_x0 = media_x0 + l[0]
			media_y0 = media_y0 + l[1]
			media_x1 = media_x1 + l[2]
			media_y1 = media_y1 + l[3]

		media_x0 = media_x0 // len(line_vector)
		media_y0 = media_y0 // len(line_vector)
		media_x1 = media_x1 // len(line_vector)
		media_y1 = media_y1 // len(line_vector)

		cv.line(image_vector, (media_x0, media_y0), (media_x1, media_y1), (0,0,255), 3, cv.LINE_AA)
		ponto_media_Y = media_y0 + ((media_y1 - media_y0) / 2)
		ponto_media_X = media_x0 + ((media_x1 - media_x0) / 2)

		for i in range(len(line_vector)):
			l = line_vector[i][0]
			ponto_media_LX = l[0] + ((l[2] - l[0]) / 2)
			ponto_media_LY = l[1] + ((l[3] - l[1]) / 2)
			distancia = math.sqrt((ponto_media_LX - ponto_media_X) **2 + (ponto_media_LY - ponto_media_Y) **2)
			vetor_distancias.append(distancia)
			media_distancias = media_distancias + distancia

		media_distancias = media_distancias // len(vetor_distancias)
		#print(f'------------Distâncias----------- \n{vetor_distancias}')
		for i in range(len(vetor_distancias)):
			if vetor_distancias[i] > raio:
				linhas_novas.append(i)

		line_vector = np.delete(line_vector, linhas_novas, axis = 0)
		#print(f'------------Linhas excluídas-----------\n--> {len(linhas_novas)}')
		center_coordinates = (int(ponto_media_X), int(ponto_media_Y))
		cv.circle(image_vector, center_coordinates, raio, (255, 0, 0), 3)
		return line_vector, image_vector

	def intersect(self, Ax1 : float, Ay1 : float, Ax2 : float, Ay2 : float, Bx1 : float, By1 : float, Bx2 : float, By2 : float) -> bool:
		d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)    
		if d:
			uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
			uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
		else:
			return False
		if not(0 <= uA <= 1 and 0 <= uB <= 1):
			return False
		x = Ax1 + uA * (Ax2 - Ax1)
		y = Ay1 + uA * (Ay2 - Ay1)
		return True

	def inside(self, ponto_0 : List, ponto_1 : List, lines : List, image_vector : List) -> List:
		flag = 0
		vetor_conflitos = []
        
		if ponto_0[0] > ponto_1[0]:
			x_maximo = ponto_0[0]
			x_minimo = ponto_1[0]
		else:
			x_maximo = ponto_1[0]
			x_minimo = ponto_0[0]
		if ponto_0[1] > ponto_1[1]:
			y_maximo = ponto_0[1]
			y_minimo = ponto_1[1]
		else:
			y_maximo = ponto_1[1]
			y_minimo = ponto_0[1]
        
		for i in range(len(lines)):
			line = lines[i][0]
			if line[0] > line[2]:
				linha_x = line[0]
				linha_y = line[1]
			else:
				linha_x = line[2]
				linha_y = line[3]
            
			if (linha_x >= x_minimo) and (linha_x <= x_maximo):
				if (linha_y >= y_minimo) and (linha_y <= y_maximo):
					flag += 1
					vetor_conflitos.append(line)
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    
		for i in range(len(lines)):
			line = lines[i][0]
			if line[0] < line[2]:
				linha_x = line[0]
				linha_y = line[1]
			else:
				linha_x = line[2]
				linha_y = line[3]
            
			if (linha_x >= x_minimo) and (linha_x <= x_maximo):
				if (linha_y >= y_minimo) and (linha_y <= y_maximo):
					flag += 1
					vetor_conflitos.append(line)
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
        
		return vetor_conflitos

	def wireCheck(self, ponto_0 : List[float], ponto_1 : List[float], lines : List[float], image_vector : List[float]) -> List[float]:
		flag_intersect = 0
		vetor_conflitos = []
        
		if ponto_0[0] > ponto_1[0]:
			x_maximo = ponto_0[0]
			x_minimo = ponto_1[0]
		else:
			x_maximo = ponto_1[0]
			x_minimo = ponto_0[0]
		if ponto_0[1] > ponto_1[1]:
			y_maximo = ponto_0[1]
			y_minimo = ponto_1[1]
		else:
			y_maximo = ponto_1[1]
			y_minimo = ponto_0[1]
            
		if lines is None:
			return image_vector
		if len(lines) != 0:
			#print(f'-----------Quantidade de fios-----------\n--> {len(lines)}')
			for i in range(len(lines)):
				line = lines[i][0]
				bool_flag = self.intersect(line[0], line[1], line[2], line[3], x_maximo, y_maximo, x_maximo, y_minimo)
				if bool_flag:
					flag_intersect += 1
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
					vetor_conflitos.append(line)
					continue
                    
				bool_flag = self.intersect(line[0], line[1], line[2], line[3], x_minimo, y_minimo, x_minimo, y_maximo)
				if bool_flag:
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
					flag_intersect += 1
					vetor_conflitos.append(line)
					continue
                    
				bool_flag = self.intersect(line[0], line[1], line[2], line[3], x_minimo, y_maximo, x_maximo, y_maximo)
				if bool_flag:
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
					flag_intersect += 1
					vetor_conflitos.append(line)
					continue
				bool_flag = self.intersect(line[0], line[1], line[2], line[3], x_minimo, y_minimo, x_maximo, y_minimo)
				if bool_flag:
					cv.line(image_vector, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
					flag_intersect += 1
					vetor_conflitos.append(line)
                    
			vetor_inside = self.inside(ponto_0, ponto_1, lines, image_vector)
			vetor_conflitos = vetor_conflitos + vetor_inside
				
			#print(f'----------------------- {len(vetor_conflitos)} Interseções -----------------------')
			#for i in range(len(vetor_conflitos)):
			#	print(f'Fio {vetor_conflitos[i]} pode estar em contato com alguma árvore')

		return image_vector

	'''	    
	def angleCheck(self, line_vector : List) -> List:
		inclinacao : List[float]= []
		media : float= 0
		linhas_novas : List[float]= []	

		for i in range(len(line_vector)):
			l = line_vector[i][0]	
			m = (l[3] - l[1]) / (l[2] - l[0])
			m = math.degrees(math.atan(m))
			media = media + m
			inclinacao.append(m)
			print(f'angulo da reta[{str(i)}] = {m}')
		if media != 0:
			media = media / len(line_vector)
		else:
			media = 0
        
		x = len(inclinacao)
		for i in range(x):
			if i >= x:
				break
                
			if media > 0:
				if (inclinacao[i] > media * 2) or (inclinacao[i] < (media / 2)):
					inclinacao.pop(i)
					x = x - 1
			else:
				if (inclinacao[i] < media * 2) or abs(inclinacao[i]) < abs(media) - (abs(media) * 2):
					inclinacao.pop(i)
					x = x - 1
            
		media = 0
		for i in range(len(inclinacao)):
			media = media + inclinacao[i]
		if media != 0:
			media = media / len(inclinacao)
		else:
			media = 0
		print(f'-----------------Média------------------\n--> {media}')
		if inclinacao == []:
			return line_vector
        
		delta = max(inclinacao) - min(inclinacao)

		if (delta >= 50) and (delta < 70):
			media = media * 1.5
		elif (delta >= 70):
			media = media * 2
        
		if abs(media) > 20:
			operador_multiplicacao = 1.5
		else:
			operador_multiplicacao = 2
        
		print('------------Angulos excluídos-----------')
		for i in range(len(line_vector)):
			l = line_vector[i][0]
			m = (l[3] - l[1]) / (l[2] - l[0])
			m = math.degrees(math.atan(m))

			if abs(media) > abs(m):
				if abs(media) - abs(m) < 10: 
					continue
			else:
				if abs(m) - abs(media) < 10:
					continue
			if media > 0:
				if (m > media * operador_multiplicacao) or (m < media / 2):
					print(f'{m} > {media * operador_multiplicacao}')
					linhas_novas.append(i)
			else:
				if (m < media * operador_multiplicacao) or (m > media / 2):
					print(f'{m} < {media * operador_multiplicacao}')
					linhas_novas.append(i)
            
		line_vector = np.delete(line_vector, linhas_novas, axis = 0)
		return line_vector
	'''


class Wire:
	def __init__(self, caminho_imagem : str, imagem_fonte : str, box : List[float]) -> None:
		self.caminho_imagem : str = caminho_imagem
		self.imagem_fonte : str = imagem_fonte
		self.box : List[float ]= box

	def setThresh(self, imagem_fonte : str, varFilter : int, varThresh : int) -> List[float]:
		_, imagem_fonte = cv.threshold(imagem_fonte, varThresh, 255, varFilter)
		return imagem_fonte

	def setMorph(self, imagem_fonte : str, varKernel : int) -> List[float]:
		#Pode ser ELLIPSE ou CROSS ao invés de RECT
		kernel = cv.getStructuringElement(cv.MORPH_RECT,(varKernel, varKernel))
		imagem_fonte = cv.morphologyEx(imagem_fonte, cv.MORPH_OPEN, kernel)
		return imagem_fonte

	def setFilter(self, imagem_fonte : List) -> List:
		imagem_fonte = cv.bilateralFilter(imagem_fonte, 7, 130, 75)
		imagem_fonte = cv.Canny(imagem_fonte, 50, 200, None, 3)
		return imagem_fonte

	def probHough(self, imagem_fonte : List, varTeta : int, varMinlength : int, varMaxgap : int) -> Union[List, List]:
		image_vector = cv.cvtColor(imagem_fonte, cv.COLOR_GRAY2BGR)
		line_vector = []
		line_vector = cv.Houghline_vector(imagem_fonte, 1,  (np.pi / 180), varTeta, None, varMinlength, varMaxgap) 
		return line_vector, image_vector

	def save(self, imagem_fonte : List, caminho_imagem : str) -> None:
		caminho_imagem = caminho_imagem.split('.')
		caminho_imagem[3] = 'linhas'
		caminho_imagem = caminho_imagem[0] + '.' + caminho_imagem[1] + '.' + caminho_imagem[2] + '.' + caminho_imagem[3] + '.' + caminho_imagem[4]
		cv.imwrite("/mnt/SSD/Source/main/processData/src/img_to_merge/" + caminho_imagem, imagem_fonte)

def wireFunc(imagem_fonte : List[float], caminho_imagem : str, box : List[float]) -> bool:
	try:
		cv.imwrite("/mnt/SSD/Source/main/processData/src/img_to_merge/" + caminho_imagem, imagem_fonte)
	except Exception as e:
		print(f"Exceção: {str(e)}")
	line_vector : List[float] = []
	vetor_quantidade_fios : List[int] = []  
	newWire : Union[Wire] = Wire(caminho_imagem, imagem_fonte, box)
	#----------------------------------------------------------
	imagem_fonte1 = newWire.setThresh(imagem_fonte, 3, 240)
	imagem_fonte1 = newWire.setMorph(imagem_fonte1, 5)
	imagem_fonte1 = newWire.setFilter(imagem_fonte1)
	line_vector, image_vector = newWire.probHough(imagem_fonte1, 80, 20, 10)
	if line_vector is not None:
		vetor_quantidade_fios.append(len(line_vector))
	else:
		vetor_quantidade_fios.append(0)
    #----------------------------------------------------------
	imagem_fonte2 = newWire.setThresh(imagem_fonte, 3, 200)
	imagem_fonte2 = newWire.setMorph(imagem_fonte2, 7)
	imagem_fonte2 = newWire.setFilter(imagem_fonte2)
	line_vector2, image_vector2 = newWire.probHough(imagem_fonte2, 50, 20, 10)
	if line_vector2 is not None:
		vetor_quantidade_fios.append(len(line_vector2))
	else:
		vetor_quantidade_fios.append(0)
	#----------------------------------------------------------
	imagem_fonte3 = newWire.setThresh(imagem_fonte, 3, 250)
	imagem_fonte3 = newWire.setMorph(imagem_fonte3, 7)
	imagem_fonte3 = newWire.setFilter(imagem_fonte3)
	line_vector3, image_vector3 = newWire.probHough(imagem_fonte3, 50, 20, 10)
	if line_vector3 is not None:
		vetor_quantidade_fios.append(len(line_vector3))
	else:
		vetor_quantidade_fios.append(0)
    #----------------------------------------------------------
	imagem_fonte4 = newWire.setThresh(imagem_fonte, 3, 205)
	imagem_fonte4 = newWire.setMorph(imagem_fonte4, 7)
	imagem_fonte4 = newWire.setFilter(imagem_fonte4)
	line_vector4, image_vector4 = newWire.probHough(imagem_fonte4, 80, 20, 10)
	if line_vector4 is not None:
		vetor_quantidade_fios.append(len(line_vector4))
	else:
		vetor_quantidade_fios.append(0)
    #----------------------------------------------------------
	imagem_fonte5 = newWire.setThresh(imagem_fonte, 3, 205)
	imagem_fonte5 = newWire.setMorph(imagem_fonte5, 5)
	imagem_fonte5 = newWire.setFilter(imagem_fonte5)
	line_vector5, image_vector5 = newWire.probHough(imagem_fonte5, 80, 20, 10)
	if line_vector5 is not None:
		vetor_quantidade_fios.append(len(line_vector5))
	else:
		vetor_quantidade_fios.append(0)
	#----------------------------------------------------------
	'''imagem_fonte4 = newWire.setThresh(imagem_fonte, 0, 140)
	imagem_fonte4 = newWire.setMorph(imagem_fonte4, 7)
	imagem_fonte4 = newWire.setFilter(imagem_fonte4)
	line_vector4, image_vector4 = newWire.probHough(imagem_fonte4, 80, 20, 10)
	if line_vector4 is not None:
		vetor_quantidade_fios.append(len(line_vector4))
	else:
		vetor_quantidade_fios.append(0)'''
    #----------------------------------------------------------
	'''imagem_fonte5 = newWire.setThresh(imagem_fonte, 0, 120)
	imagem_fonte5 = newWire.setMorph(imagem_fonte5, 7)
	imagem_fonte5 = newWire.setFilter(imagem_fonte5)
	line_vector5, image_vector5 = newWire.probHough(imagem_fonte5, 50, 20, 10)
	if line_vector5 is not None:
		vetor_quantidade_fios.append(len(line_vector5))
	else:
		vetor_quantidade_fios.append(0)'''
    #----------------------------------------------------------
	flag = 0
	newOperation : Union[Operation] = Operation(line_vector, image_vector)
	for i in range(len(vetor_quantidade_fios)):
		if vetor_quantidade_fios[i] > 1:
			flag = i
	if flag == 1:
		newOperation.line_vector = line_vector2
		newOperation.image_vector = image_vector2
	elif flag == 2:
		newOperation.line_vector = line_vector3
		newOperation.image_vector = image_vector3
	elif flag == 3:
		newOperation.line_vector = line_vector4
		newOperation.image_vector = image_vector4
	elif flag == 4:
		newOperation.line_vector = line_vector5
		newOperation.image_vector = image_vector5

    #----------------------------------------------------------
	x_minimo : int = 0
	x_maximo : int = int(box[0][2])
	y_minimo : int = 0
	y_maximo : int = int(box[0][3])

	ponto_0 = (abs(x_minimo), abs(y_minimo))
	ponto_1 = (abs(x_maximo), abs(y_maximo))

	cv.rectangle(imagem_fonte, ponto_0, ponto_1, (0, 255, 0), 2)
	flag = False

	if newOperation.line_vector is not None:
		newOperation.line_vector, newOperation.image_vector = newOperation.paralelo(newOperation.line_vector, newOperation.image_vector)

	if newOperation.line_vector is not None:
		for i in range(0, len(newOperation.line_vector)):
			l = newOperation.line_vector[i][0]
			cv.line(imagem_fonte, (l[0], l[1]), (l[2], l[3]), (0,255,255), 3, cv.LINE_AA)
		flag = True

	#if newOperation.line_vector is not None:
	#	newOperation.line_vector = newOperation.angleCheck(newOperation.line_vector)	

	#if newOperation.line_vector is not None:
	#	imagem_fonte, flag = newOperation.wireCheck(ponto_0, ponto_1, newOperation.line_vector, imagem_fonte)
	newWire.save(imagem_fonte, caminho_imagem)
	return flag

def wireDetector(data, box : List) -> bool:
	images : List[float] = []
	images.append(cv.imread(data['camera'][0]))

	x_minimo = abs(int(box[0][0] - (box[0][2] / 2)))
	x_maximo = abs(int(box[0][0] + (box[0][2] / 2)))
	y_minimo = abs(int(box[0][1] - (box[0][3] / 2)))
	y_maximo = abs(int(box[0][1] + (box[0][3] / 2)))

	images[0] = images[0][y_minimo : y_maximo, x_minimo:x_maximo].copy()

	caminho_imagems = [data['camera'][0], data['camera'][0]]
	imagem_fonte = images[0]
	caminho_imagem = caminho_imagems[0].split('/')[-1]

	flag0 = wireFunc(imagem_fonte, caminho_imagem, box)
	return flag0

if __name__ == "__main__":
	caminho_imagem : str = '/home/ubuntu/Documentos/hdr_test/Capturas/camera/'
	filename : str = '2021-06-11.10:16:43.804897_0.webcam.jpg'
	imagem_fonte : List[float] = cv.imread(cv.samples.findFile(caminho_imagem + filename))
	wireDetector(caminho_imagem, imagem_fonte, filename)
