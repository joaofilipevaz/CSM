# This Python file uses the following encoding: utf-8

# Trabalho 1 CSM

from time import time
from os import path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Queue

# 1

"""
Elabore uma função ("gera_huﬀman") que gere uma tabela com o código binário para cada símbolo de um dado
conjunto, usando o método de Huﬀman. Esta função deve ter como parâmetros de entrada um conjunto de
símbolos e as suas probabilidades (ou em alternativa pode usar o número de ocorrências de cada símbolo, dado
pelo seu histograma). Também pode em alternativa gerar não uma tabela mas outra estrutura de dados com os
códigos pretendidos.
"""

# Lê a imagem em níveis de cinzento
x = cv2.imread("lena.tiff", cv2.IMREAD_GRAYSCALE)
# Converte a imagem (matriz) numa sequência de números (array)
xi = x.ravel()
# Calcula o histogram
h, bins, patches = plt.hist(xi, 256,[0,256])

# Gera o código de Huffman
t0 = time()
tabela_codigo = gera_huffman(np.arange(0,256),h)
t1 = time()
print "time:", t1-t0

def gera_huffman(bins, h):
    prob = bins
    #Cria um diciionario (numero de ocorrencias,valor) organizado por ordem crescente
    bits = ["" for x in range(len(h))]
    dic = sorted(list(t) for t in zip(h, bins, bits))

    #remove ocorrencias nulas do array
    while dic[0][0] == 0:
        dic.remove(dic[0])

    def create_tree(dic):
        p = Queue.PriorityQueue()
        for value in dic:  # 1. Create a leaf node for each symbol
            p.put(value)
        while p.qsize() > 1:  # 2. While there is more than one node
            l, r = p.get(), p.get()  # 2a. remove two highest nodes
            for i in range(len(dic)):
                if type(l[1]) == np.float64:
                    if dic[i][1] == l[1]:
                        dic[i][2] += '0'
                else:
                    for z in range(len(l[1])):
                        if dic[i][1] == l[1][z]:
                            dic[i][2] += '0'
                if type(r[1]) == np.float64:
                    if dic[i][1] == r[1]:
                        dic[i][2] += '1'
                else:
                    for z in range(len(r[1])):
                        if dic[i][1] == r[1][z]:
                            dic[i][2] += '1'
            if (type(l[1]) == np.float64 and type(r[1]) == np.float64):
                p.put([l[0] + r[0], [l[1]] + [r[1]], ""])
            elif (type(l[1]) == np.float64 and type(r[1]) != np.float64):
                p.put([l[0] + r[0], [l[1]] + r[1], ""])
            elif (type(l[1]) != np.float64 and type(r[1]) == np.float64):
                p.put([l[0] + r[0], l[1] + [r[1]], ""])
            else:
                p.put([l[0] + r[0], l[1] + r[1], ""])
        return p.get()  # 3. tree is complete - return root node

# 2

"""
Elabore uma função ("codiﬁca") que dada uma mensagem (sequência de símbolos) e a tabela da ponto anterior,
retorne uma sequência de bits com a mensagem codiﬁcada.
"""

# 3

"""
Elabore uma função ("descodiﬁca") que dada uma sequência de bits (mensagem codiﬁcada) e a tabela do ponto
1, retorne uma sequência de símbolos (mensagem descodiﬁcada).
"""

# 4

"""
Elabore uma função ("escrever") que dada uma sequência de bits (mensagem codiﬁcada) e o nome do ﬁcheiro,
escreva a sequência de bits para o ﬁcheiro.
"""

# 5

"""
Elabore uma função ("ler") que dado o nome do ﬁcheiro, leia uma sequência de bits (mensagem codiﬁcada)
contida no ﬁcheiro.
"""

# 6

"""
Teste as funções elaboradas usando para o efeito vários ﬁcheiros com diferentes tipos de média:
Imagem: Use para o efeito a imagem “Lena.tiff” em tons de cinzento.
Texto: Use os ﬁcheiros “ubuntu_server_guide.pdf” e “ubuntu_server_guide.txt”.
Áudio: Use o ﬁcheiro “HenryMancini-PinkPanther.mp3”.
Midi: Use o ﬁcheiro “HenryMancini-PinkPanther.mid”.
ECG: Eletrocardiograma - use o ﬁcheiro “ecg.txt”.
a) Gere o código usando a função realizada no ponto 1. Meça o tempo que demora a função.
b) Meça a entropia e o número médio de bits por símbolo. Calcule a eﬁciência.
c) Faça a codiﬁcação da mensagem contida no ﬁcheiro (usando a função realizada no ponto 2). Meça o tempo
que a função demora a fazer a codiﬁcação.
d) Grave um ﬁcheiro com a mensagem codiﬁcada, usando a função realizada no ponto 4. Veja o tamanho do
ﬁcheiro.
e) Leia do ﬁcheiro o conjunto de bits, usando a função realizada no ponto 5.
f) Faça a descodiﬁcação da mensagem (usando a função realizada no ponto 3.) Meça o tempo que a função
demora a fazer a descodiﬁcação.
g) Compare a mensagem descodiﬁcada com a original e veriﬁque que são iguais (erro nulo).
"""



# Codifica e grava ficheiro
seq_bit0 = codifica(xi,tabela_codigo)
escrever(seq_bit0, filename)
t2 = time()
print "time:", t2-t1
# Lê ficheiro e descodifica
seq_bit1 = ler(filename)
yi = descodifica(seq_bit1,tabela_codigo)
t3 = time()
print "time:", t3-t2
size_ini = path.getsize("filename original image")
size_end = path.getsize("filename compressed")
print "taxa: ", 1.* size_ini / size_end
plt.show()
cv2.waitKey(0)
plt.close("all")
cv2.destroyAllWindows()

