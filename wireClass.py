import math
import cv2 as cv
import numpy as np

class Wire:
    def __init__(self, path, src, filename):
        self.path = path
        self.src = src
        self.filename = filename

    def setThresh(self, src, varFilter, varThresh):
        _, src = cv.threshold(src, varThresh, 255, varFilter)
        return src

    def setMorph(self, src, varKernel):
        #Pode ser ELLIPSE ou CROSS ao invés de RECT
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(varKernel, varKernel))
        src = cv.morphologyEx(src, cv.MORPH_OPEN, kernel)
        return src

    def setFilter(self, src):
        src = cv.bilateralFilter(src, 7, 130, 75)
        src = cv.Canny(src, 50, 200, None, 3)
        return src

    def probHough(self, src, varTeta, varMinlength, varMaxgap):
        cdstP = cv.cvtColor(src, cv.COLOR_GRAY2BGR)
        linesP = []
        linesP = cv.HoughLinesP(src, 1,  (np.pi / 180), varTeta, None, varMinlength, varMaxgap) 
        return linesP, cdstP

    def save(self, cdstP, path, filename):
        filename = filename.split('.')
        filename[3] = 'linhas'
        filename = filename[0] + '.' + filename[1] + '.' + filename[2] + '.' + filename[3] + '.' + filename[4]
        cv.imwrite(path + filename, cdstP)

    def paralelo(self, linesP, cdstP):
        mediaX0 = 0
        mediaX1 = 0
        mediaY0 = 0
        mediaY1 = 0
        pontoMediaLX = 0
        pontoMediaLY = 0
        mediaDist = 0
        newLines = []
        vetDist = []
        height, width, channels = cdstP.shape
        raio = (height + width) // (channels * 2)
        print(f'Raio = {raio}')
        for i in range(len(linesP)):
            l = linesP[i][0]
            mediaX0 = mediaX0 + l[0]
            mediaY0 = mediaY0 + l[1]
            mediaX1 = mediaX1 + l[2]
            mediaY1 = mediaY1 + l[3]

        mediaX0 = mediaX0 // len(linesP)
        mediaY0 = mediaY0 // len(linesP)
        mediaX1 = mediaX1 // len(linesP)
        mediaY1 = mediaY1 // len(linesP)

        cv.line(cdstP, (mediaX0, mediaY0), (mediaX1, mediaY1), (0,0,255), 3, cv.LINE_AA)
        pontoMediaY = mediaY0 + ((mediaY1 - mediaY0) / 2)
        pontoMediaX = mediaX0 + ((mediaX1 - mediaX0) / 2)

        for i in range(len(linesP)):
            l = linesP[i][0]
            pontoMediaLX = l[0] + ((l[2] - l[0]) / 2)
            pontoMediaLY = l[1] + ((l[3] - l[1]) / 2)
            dist = math.sqrt((pontoMediaLX - pontoMediaX) **2 + (pontoMediaLY - pontoMediaY) **2)
            vetDist.append(dist)
            mediaDist = mediaDist + dist

        mediaDist = mediaDist // len(vetDist)
        print(f'------------Distâncias----------- \n{vetDist}')
        for i in range(len(vetDist)):
            if vetDist[i] > raio:
                newLines.append(i)

        linesP = np.delete(linesP, newLines, axis = 0)
        print(f'------------Linhas excluídas-----------\n--> {len(newLines)}')
        center_coordinates = (int(pontoMediaX), int(pontoMediaY))
        cv.circle(cdstP, center_coordinates, raio, (255, 0, 0), 3)
        return linesP, cdstP

    def intersect(self, Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
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

    def inside(self, p0, p1, lines, cdstP):
        flag = 0
        vetConf = []
        
        if p0[0] > p1[0]:
            maxX = p0[0]
            minX = p1[0]
        else:
            maxX = p1[0]
            minX = p0[0]
        if p0[1] > p1[1]:
            maxY = p0[1]
            minY = p1[1]
        else:
            maxY = p1[1]
            minY = p0[1]
        
        for i in range(len(lines)):
            line = lines[i][0]
            if line[0] > line[2]:
                lineX = line[0]
                lineY = line[1]
            else:
                lineX = line[2]
                lineY = line[3]
            
            if (lineX >= minX) and (lineX <= maxX):
                if (lineY >= minY) and (lineY <= maxY):
                    flag += 1
                    vetConf.append(line)
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    
        for i in range(len(lines)):
            line = lines[i][0]
            if line[0] < line[2]:
                lineX = line[0]
                lineY = line[1]
            else:
                lineX = line[2]
                lineY = line[3]
            
            if (lineX >= minX) and (lineX <= maxX):
                if (lineY >= minY) and (lineY <= maxY):
                    flag += 1
                    vetConf.append(line)
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
        
        return vetConf

    def wireCheck(self, p0, p1, lines, cdstP):
        flagP = 0
        vetConf = []
        
        if p0[0] > p1[0]:
            maxX = p0[0]
            minX = p1[0]
        else:
            maxX = p1[0]
            minX = p0[0]
        if p0[1] > p1[1]:
            maxY = p0[1]
            minY = p1[1]
        else:
            maxY = p1[1]
            minY = p0[1]
            
        if lines is None:
            return cdstP
        if len(lines) != 0:
            print(f'-----------Quantidade de fios-----------\n--> {len(lines)}')
            for i in range(len(lines)):
                line = lines[i][0]
                boolflag = self.intersect(line[0], line[1], line[2], line[3], maxX, maxY, maxX, minY)
                if boolflag:
                    flagP += 1
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    vetConf.append(line)
                    continue
                    
                boolflag = self.intersect(line[0], line[1], line[2], line[3], minX, minY, minX, maxY)
                if boolflag:
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    flagP += 1
                    vetConf.append(line)
                    continue
                    
                boolflag = self.intersect(line[0], line[1], line[2], line[3], minX, maxY, maxX, maxY)
                if boolflag:
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    flagP += 1
                    vetConf.append(line)
                    continue
                boolflag = self.intersect(line[0], line[1], line[2], line[3], minX, minY, maxX, minY)
                if boolflag:
                    cv.line(cdstP, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
                    flagP += 1
                    vetConf.append(line)
                    
            vetInside = self.inside(p0, p1, lines, cdstP)
            vetConf = vetConf + vetInside
                
            print(f'----------------------- {len(vetConf)} Interseções -----------------------')
            for i in range(len(vetConf)):
                print(f'Fio {vetConf[i]} pode estar em contato com alguma árvore')

        return cdstP

    '''	    
    def angleCheck(self, linesP):
        slope = []
        media = 0
        newLines = []	
        
        for i in range(len(linesP)):
            l = linesP[i][0]	
            m = (l[3] - l[1]) / (l[2] - l[0])
            m = math.degrees(math.atan(m))
            media = media + m
            slope.append(m)
            print(f'angulo da reta[{str(i)}] = {m}')
        if media != 0:
            media = media / len(linesP)
        else:
            media = 0
        
        x = len(slope)
        for i in range(x):
            if i >= x:
                break
                
            if media > 0:
                if (slope[i] > media * 2) or (slope[i] < (media / 2)):
                    slope.pop(i)
                    x = x - 1
            else:
                if (slope[i] < media * 2) or abs(slope[i]) < abs(media) - (abs(media) * 2):
                    slope.pop(i)
                    x = x - 1
            
        media = 0
        for i in range(len(slope)):
            media = media + slope[i]
        if media != 0:
            media = media / len(slope)
        else:
            media = 0
        print(f'-----------------Média------------------\n--> {media}')
        if slope == []:
            return linesP
        
        delta = max(slope) - min(slope)
        
        if (delta >= 50) and (delta < 70):
            media = media * 1.5
        elif (delta >= 70):
            media = media * 2
        
        if abs(media) > 20:
            opx = 1.5
        else:
            opx = 2
        
        print('------------Angulos excluídos-----------')
        for i in range(len(linesP)):
            l = linesP[i][0]
            m = (l[3] - l[1]) / (l[2] - l[0])
            m = math.degrees(math.atan(m))
            
            if abs(media) > abs(m):
                if abs(media) - abs(m) < 10: 
                    continue
            else:
                if abs(m) - abs(media) < 10:
                    continue
            if media > 0:
                if (m > media * opx) or (m < media / 2):
                    print(f'{m} > {media * opx}')
                    newLines.append(i)
            else:
                if (m < media * opx) or (m > media / 2):
                    print(f'{m} < {media * opx}')
                    newLines.append(i)
            
        linesP = np.delete(linesP, newLines, axis = 0)
        return linesP
    '''

def wireDetector(path, src, filename):
    linesP = []
    varSize = []  
    wireClass = Wire(path, src, filename)
    #----------------------------------------------------------
    src1 = wireClass.setThresh(src, 3, 240)
    src1 = wireClass.setMorph(src1, 5)
    src1 = wireClass.setFilter(src1)
    linesP, cdstP = wireClass.probHough(src1, 80, 20, 10)
    if linesP is not None:
        varSize.append(len(linesP))
    else:
        varSize.append(0)
    #----------------------------------------------------------
    src2 = wireClass.setThresh(src, 3, 205)
    src2 = wireClass.setMorph(src2, 7)
    src2 = wireClass.setFilter(src2)
    linesP2, cdstP2 = wireClass.probHough(src2, 50, 20, 10)
    if linesP2 is not None:
        varSize.append(len(linesP2))
    else:
        varSize.append(0)
    #----------------------------------------------------------
    src3 = wireClass.setThresh(src, 3, 250)
    src3 = wireClass.setMorph(src3, 7)
    src3 = wireClass.setFilter(src3)
    linesP3, cdstP3 = wireClass.probHough(src3, 50, 20, 10)
    if linesP3 is not None:
        varSize.append(len(linesP3))
    else:
        varSize.append(0)
    #----------------------------------------------------------
    src4 = wireClass.setThresh(src, 0, 140)
    src4 = wireClass.setMorph(src4, 7)
    src4 = wireClass.setFilter(src4)
    linesP4, cdstP4 = wireClass.probHough(src4, 50, 20, 10)
    if linesP4 is not None:
        varSize.append(len(linesP4))
    else:
        varSize.append(0)
    #----------------------------------------------------------
    src5 = wireClass.setThresh(src, 0, 170)
    src5 = wireClass.setMorph(src5, 3)
    src5 = wireClass.setFilter(src5)
    linesP5, cdstP5 = wireClass.probHough(src5, 80, 20, 10)
    if linesP5 is not None:
        varSize.append(len(linesP5))
    else:
        varSize.append(0)
    #----------------------------------------------------------
    flag = 0
    for i in range(len(varSize)):
        if varSize[i] > 0:
            flag = i
            break
    if flag == 1:
        linesP = linesP2
        cdstP = cdstP2
    elif flag == 2:
        linesP = linesP3
        cdstP = cdstP3
    elif flag == 3:
        linesP = linesP4
        cdstP = cdstP4
    elif flag == 4:
        linesP = linesP5
        cdstP = cdstP5
    print(f"Filtro = {flag + 1}")
    #----------------------------------------------------------
    if linesP is not None:
        linesP, cdstP = wireClass.paralelo(linesP, cdstP)	

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,255,255), 3, cv.LINE_AA)

    #if linesP is not None:
	#	linesP = wireClass.angleCheck(linesP)	

	#p0 = (430, 124)
	#p1 = (295, 177)		
	#cv.rectangle(cdstP, p0, p1, (0, 255, 0), 2)	
	#cdstP = wireClass.wireCheck(p0, p1, linesP, cdstP)
    wireClass.save(cdstP, path, filename)

if __name__ == "__main__":
	path = '/home/ubuntu/Documentos/hdr_test/Capturas/camera/'
	filename = '2021-06-11.08_55_58.736237_0.webcam.jpg'
	src = cv.imread(cv.samples.findFile(path + filename))
	wireDetector(path, src, filename)