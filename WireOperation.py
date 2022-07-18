import math
import cv2 as cv
import numpy as np

class Operation:
	def __init__(self) -> None:
		self._line_vector = []
		self._image_vector = []

	@property
	def line_vector(self) -> list:
		return self._line_vector

	@line_vector.setter
	def line_vector(self, line_vector : list) -> None:
		self._line_vector = line_vector

	@property
	def image_vector(self) -> list:
		return self._image_vector

	@image_vector.setter
	def image_vector(self, image_vector : list) -> None:
		self._image_vector = image_vector

	def paralelo(self, line_vector : list, image_vector : list) -> list:
		media_x0 : float = 0
		media_x1 : float = 0
		media_y0 : float = 0
		media_y1 : float = 0

		ponto_media_LX : float = 0
		ponto_media_LY : float = 0
		media_distancias : float = 0

		linhas_novas : list = []
		vetor_distancias : list = []

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

	def inside(self, ponto_0 : list, ponto_1 : list, lines : list, image_vector : list) -> list:
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

	def wireCheck(self, ponto_0 : list, ponto_1 : list, lines : list, image_vector : list) -> list:
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
	def angleCheck(self, line_vector : list) -> list:
		inclinacao : list = []
		media : float= 0
		linhas_novas : list = []	

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
