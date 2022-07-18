import cv2 as cv
import sys

packages = 'media/nvidia/SSD/vegetacao-codes/source/main/process/utils/Wire_Detector/'
sys.path.insert(0, packages)

from Wire_Detector.SetWire import Wire
from Wire_Detector.WireOperation import Operation
from Wire_Detector.WireFlag import WireFlag
from Wire_Detector.testParams import testParams

def save_test(imagem_fonte, caminho_imagem, box) -> None:
	image_copy : str = imagem_fonte
	try:
		for i in range(4):
			if i == 1 or i == 2:
				continue
			for j in range(256):
				for k in range(8):
					if k % 2 == 0:
						continue
					for z in range(2):
						if z == 0:
							var_teta = 80
						elif z == 1:
							var_teta = 50
						caminho_imagem = str(i) + '_' + str(j) + '_' + str(k) + '_' + str(var_teta) + '.jpg'
						test_list = testParams(Wire(caminho_imagem, image_copy, box), image_copy, i, j, k, var_teta, 20, 10)
					
						if test_list.line_vector is not None:
							for x in range(0, len(test_list.line_vector)):
								l = test_list.line_vector[x][0]
								cv.line(test_list.image_vector, (l[0], l[1]), (l[2], l[3]), (0,255,255), 3, cv.LINE_AA)

							cv.imwrite("/media/nvidia/SSD/vegetacao-codes/source/main/process/utils/test_img/" + caminho_imagem, test_list.image_vector)
	except Exception as e:
		print(f"Erro com a imagem: /media/nvidia/SSD/vegetacao-codes/source/main/process/utils/test_img/{caminho_imagem}.\n{e}")
				
def wireFunc(imagem_fonte : list, caminho_imagem : str, box : list) -> bool:
	try:
		cv.imwrite("/media/nvidia/SSD/vegetacao-codes/source/main/process/utils/img_to_merge/" + caminho_imagem, imagem_fonte)
	except Exception as e:
		print(f"Exceção: {str(e)}")
	 
	newOperation : Operation = Operation()
	
	imagem_teste : str = imagem_fonte
	#save_test(imagem_teste, caminho_imagem, box)

	line_vector : list = []
	vetor_quantidade_fios : list = [] 
	test_list : list = []
	flag : int = 0

	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 240, 7, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 240, 5, 80, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 199, 7, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 250, 7, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 205, 7, 80, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 205, 5, 80, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 240, 5, 50, 20, 10))
	
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 150, 7, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 3, 150, 7, 80, 20, 10))

	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 3, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 5, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 7, 50, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 3, 80, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 5, 80, 20, 10))
	test_list.append(testParams(Wire(caminho_imagem, imagem_fonte, box), imagem_fonte, 0, 150, 7, 80, 20, 10))


	for i in range(len(test_list)):
		if test_list[i].line_vector is not None:
			if len(test_list[i].line_vector) > 1:
				flag = i
				break

	newOperation.line_vector = test_list[flag].line_vector
	newOperation.image_vector = test_list[flag].image_vector

    #----------------------------------------------------------
	#x_minimo : int = 0
	#x_maximo : int = int(box[0][2])
	#y_minimo : int = 0
	#y_maximo : int = int(box[0][3])

	#ponto_0 = (abs(x_minimo), abs(y_minimo))
	#ponto_1 = (abs(x_maximo), abs(y_maximo))

	#cv.rectangle(imagem_fonte, ponto_0, ponto_1, (0, 255, 0), 2)
	#-----------------------------------------------------------
	newFlag = WireFlag()
	newFlag.flag = False

	if newOperation.line_vector is not None:
		newOperation.line_vector, newOperation.image_vector = newOperation.paralelo(newOperation.line_vector, newOperation.image_vector)

	if newOperation.line_vector is not None:
		for i in range(0, len(newOperation.line_vector)):
			l = newOperation.line_vector[i][0]
			cv.line(imagem_fonte, (l[0], l[1]), (l[2], l[3]), (0,255,255), 3, cv.LINE_AA)

			newFlag.__add__(newFlag.x_inicial, l[0])
			newFlag.__add__(newFlag.x_final, l[2])
			newFlag.__add__(newFlag.y_inicial, l[1])
			newFlag.__add__(newFlag.y_final, l[3])
			
		newFlag.flag = True

	#if newOperation.line_vector is not None:
	#	newOperation.line_vector = newOperation.angleCheck(newOperation.line_vector)	

	#if newOperation.line_vector is not None:
	#	imagem_fonte, flag = newOperation.wireCheck(ponto_0, ponto_1, newOperation.line_vector, imagem_fonte)
	Wire(caminho_imagem, imagem_fonte, box).save(imagem_fonte, caminho_imagem)
	return newFlag

def wireDetector(img, box : list) -> bool:
	path_img = "/media/nvidia/SSD/vegetacao-codes/source/main/process/utils/temp_img/tmp_img.jpg"
	cv.imwrite(path_img, img)
	
	images : list = []
	images.append(cv.imread(path_img))

	x_minimo = abs(int(box[0][0] - (box[0][2] / 2)))
	if (x_minimo - 15) >= 0:
		x_minimo = x_minimo - 15
	x_maximo = abs(int(box[0][0] + (box[0][2] / 2))) + 15
	y_minimo = abs(int(box[0][1] - (box[0][3] / 2)))
	if (y_minimo - 15) >= 0:
		y_minimo = y_minimo - 15
	y_maximo = abs(int(box[0][1] + (box[0][3] / 2))) + 15

	print(len(box))
	images[0] = images[0][y_minimo : y_maximo, x_minimo:x_maximo].copy()

	caminho_imagens = [path_img, path_img]
	imagem_fonte = images[0]
	caminho_imagem = caminho_imagens[0].split('/')[-1]

	flag0 = wireFunc(imagem_fonte, caminho_imagem, box)
	return flag0