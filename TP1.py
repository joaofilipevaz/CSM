# This Python file uses the following encoding: utf-8

# Trabalho 1 CSM

# João Filipe Vaz - 40266 | João Ventura - 38950

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# 1

x_img = cv2.imread("lenac.tif")
cv2.imshow('Original Image', x_img)
# metodo que retorna o data type da imagem
print x_img.dtype
# metodo que retorna o numero de linhas, colunas e canais de cor. o numero de canais só aparece se a imagem for a cores
print x_img.shape
cv2.waitKey(0)
cv2.destroyAllWindows()

# 2

"""
Grave a mesma imagem, mas agora em formato "JPEG"com diferentes qualidades. Veriﬁque visualmente a
qualidade das imagens assim como o tamanho do ﬁcheiro. Calcule a taxa de compressão, a SNR e a PSNR.
"""


# calcula o mean square error
def meanse(x_img_original, x_img_transformada):
    # mean square error
    mse = 0
    for i in range(len(x_img_original)):
        for z in range(len(x_img_original[i])):
            for t in range(len(x_img_original[i][z])):
                # O erro é dado pelo quadrado da diferença entre os dados originais e os transformados
                mse += ((float(x_img_original[i][z][t]) - float(x_img_transformada[i][z][t])) ** 2)
    return mse / x_img.size


# calcula o peak signal to noise ratio
def peaksnr(mse, bits):
    # como a imagem possui 8 bits por amostra - uint8 - o valor maximo possivel é 255
    return round(10. * np.log10((2 ** bits) ** 2 / mse), 3)


# calcula o signal to noise ratio
def snr(x_img_transformada, mse):
    # potencia do sinal
    p_sinal = np.sum(x_img_transformada.astype(np.float64)**2) / x_img_transformada.size
    return round(10. * np.log10(p_sinal / mse), 3)


cv2.imwrite('file1.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
cv2.imwrite('file2.jpg', x_img, (cv2.IMWRITE_JPEG_QUALITY, 10))

x_img_hi = cv2.imread("file1.jpg")
x_img_lo = cv2.imread("file2.jpg")

dim_img_original = os.path.getsize("lenac.tif")
dim_img_jpg_hi = os.path.getsize("file1.jpg")
dim_img_jpg_lo = os.path.getsize("file2.jpg")

txcomp_img_jpg_lo = int(dim_img_original / dim_img_jpg_lo)
txcomp_img_jpg_hi = int(dim_img_original / dim_img_jpg_hi)

print "a taxa de compressão da imagem de alta qualidade é de {} para 1".format(txcomp_img_jpg_hi)
print "e a de baixa qualidade é de {} para 1".format(txcomp_img_jpg_lo)

print "a SNR da imagem de alta qualidade é de {}".format(snr(x_img_hi, meanse(x_img, x_img_hi)))
print "a SNR da imagem de baixa qualidade é de {}".format(snr(x_img_lo, meanse(x_img, x_img_lo)))

print "a Peak SNR da imagem de alta qualidade é de {}".format(peaksnr(meanse(x_img, x_img_hi), 8))
print "a Peak SNR da imagem de baixa qualidade é de {}".format(peaksnr(meanse(x_img, x_img_lo), 8))

# 3

"""
Converta a imagem para níveis de cinzento, usando o método "cvtColor"e grave a imagem. Este método aplica
a transformação Y = R∗299/1000+G∗587/1000+B ∗114/1000, justiﬁque a utilização desta equação. Veriﬁque
também o tamanho do ﬁcheiro e compare-o com o ﬁcheiro original.

R - A equação Y = R∗299/1000+G∗587/1000+B ∗114/1000 é conhecida como a "ITU-R 601-2 luma transform" e é um standard
para a representação da luma, também conhecida pela letra Y. A luma representa o brilho de uma imagem, tipicamente
representado a preto e branco e acromatico. O olho humano tem uma sensibilidade superior a luminancia do que
relativamente às diferenças cromáticas. O calculo directo da luminancia obriga a analises espectrais particulares,
outra forma de a intrepretar é atraves de uma soma ponderada dos componentes RGB. Analisando as 3 cores vermelho,
verde e azul, e tendo elas a mesma radiancia no espectro visivel, entao o verde irá aparecer como a mais brilhante
das tres já que a função de eficiencia de luminosidade (que nos fornece uma representação fiedigna da sensibilidade
do olho humano à luminosidade) atinge o pico nesta gama do espectro de cores. O vermelho será menos brilhante e o
azul o mais escuro dos tres. Os coeficientes são então uma função de cada componente espectral devidamente ponderado
pela sensibilidade do olho humano. A origem destes coeficientes foi a de servir como referencia para a computação da
luminancia nos monitores CRT introduzidos pela TV em 1953. Embora estes coeficientes sejam ainda adequados para o
calculo da luma já nao reflectem a luminancia nos monitores comtemporaneos. Na realidade o tamanho do ficheiro é um
terço do ficheiro original, este facto é explicado pelo facto da luma, ou Y, ser apenas um dos canais dos três que
compoem o ficheiro, praticamente o que estamos a fazer é a suprimir a componente chromatica e a ficar apenas com a
compoente da intensidade da luz.

"""

x_img_g = cv2.cvtColor(x_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray Image', x_img_g)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('file3.bmp', x_img_g)

# 4

"""
Apresente o histograma da imagem em tons de cizento, veriﬁque quantos níveis de cizento tem a imagem.
"""

plt.hist(x_img_g.ravel(), 256, [0, 256])

"""
Os pixeis da imagem estão distribuidos entre os niveis de cinzento 30 e 230, sendo que os picos de distribuição estão a
volta dos niveis 50, 100 e 150. A imagem tem 256 niveis diferentes de cinzento.
"""

# 5

"""
Nos próximos trabalhos será necessário realizar operações com os valores de cada pixel. Para este efeito pode-
se transformar a imagem para um array. O código seguinte representa o pixel mais signiﬁcante da imagem.
Apresente oito imagens, cada uma com o valor de cada bit para todos os pixeis.
"""


def bitvalue(img_g):
    # array com o valor de cada bit
    bits = [1, 2, 4, 8, 16, 32, 64, 128]
    # numero de colunas e linhas do array bidimensional
    cols = len(img_g)
    rows = len(img_g[0])
    # itera cada bit
    for i in range(len(bits)):
        # em cada bit cria uma imagem para representar o plano de bits
        y = np.zeros((cols, rows), dtype=np.uint8)
        # itera nas linhas e colunas
        for z in range(len(img_g)):
            for t in range(len(img_g[z])):
                # avalia a expressão binaria em 8 bits para saber se o bit esta activo
                if '{0:08b}'.format(img_g[z][t])[7 - i] == '1':
                    # se o bit esta activo o pixel é guardado com o valor respectivo
                    y[z][t] = bits[i]
        cv2.imshow('Bit Plane - bit %i' % i, y * 1.0)
        cv2.imwrite('Bit Plane - bit %i.bmp' % i, y * 1.0)


bitvalue(x_img_g)

# 6

"""
Grave uma imagem que contém apenas a informação dos 4 bits mais signiﬁcantes da imagem.
"""


def mostsigbits(img_g):
    # array com o valor de cada bit
    bits = [1, 2, 4, 8, 16, 32, 64, 128]
    # numero de colunas e linhas do array bidimensional
    cols = len(img_g)
    rows = len(img_g[0])
    # array de destino iniciado a zeros
    y = np.zeros((cols, rows), dtype=np.uint8)
    # itera os 4 bits mais significantes
    for i in range(len(bits) / 2, len(bits)):
        # itera a imagem nas linhas e colunas
        for z in range(len(img_g)):
            for t in range(len(img_g[z])):
                # avalia a expressão binaria em 8 bits para saber se o bit esta activo
                if '{0:08b}'.format(img_g[z][t])[7 - i] == '1':
                    # se o bit esta activo o valor do bit é adicionado ao pixel
                    y[z][t] += bits[i]
    cv2.imshow('Imagem com os 4 bits mais significativos', y)
    cv2.imwrite('4bitsig.bmp', img_g)


mostsigbits(x_img_g)

# 7

"""
Crie uma função que apresente uma imagem (100 × 100) como se apresenta na ﬁgura. O ângulo de cada sector
é dado por parâmetro passado à função (o ângulo é um valor inteiro entre 0 e 360 graus).
"""


def cria_imagem(angulo, dim):
    # inizializamos array vazio para a imagem
    img = np.zeros((dim, dim), np.uint8)
    cor = 0
    # cria uma grelha ortogonal entre 0 e dim
    x, y = np.meshgrid(np.arange(0, dim, dtype=np.float64), np.arange(0, dim, dtype=np.float64))
    # calcula o centro da grelha
    origem_x = (len(x) - 1) / 2.
    origem_y = (len(y) - 1) / 2.
    # recalcula x e y como um referencial face a origem
    x -= origem_x
    y -= origem_y
    # multiplica y pela componente imaginaria
    y = y * 1j
    # junta a parte real e imaginaria para obter coordenadas complexas
    z = x + y
    # Calcula todos os algulos relativos às coordenanas complexas z
    a = np.angle(z)*180./np.pi
    for n in range(-360/angulo, 360/angulo):
        # verifica quais os elementos do array dentro da area definida pelo angulo a
        indice = ((a >= n*angulo) & (a < (n+1)*angulo))
        # atribui a cor aos pixeis correspondentes
        img[indice] = cor
        # pinta os sectores alternadamente
        if cor == 0:
            cor = 255
        else:
            cor = 0
    return img

image = cria_imagem(1, 600)
cv2.imshow('Invencao', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('imagem_abstracta.bmp', image)
