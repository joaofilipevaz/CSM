# This Python file uses the following encoding: utf-8

# Trabalho 1 CSM

from time import time
from os import path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Queue
import pprint

# biblioteca eficiente para a representação de bits
from bitarray import bitarray

# 1

"""
Elabore uma função ("gera_huﬀman") que gere uma tabela com o código binário para cada símbolo de um dado
conjunto, usando o método de Huﬀman. Esta função deve ter como parâmetros de entrada um conjunto de
símbolos e as suas probabilidades (ou em alternativa pode usar o número de ocorrências de cada símbolo, dado
pelo seu histograma). Também pode em alternativa gerar não uma tabela mas outra estrutura de dados com os
códigos pretendidos.
"""


def gera_huffman(freq):

    # simbolos do algoritmo - neste caso uma gama de valores numa lista de listas
    simbolos = [[i] for i in xrange(len(freq))]
    # String vazia para guardar os bits resultantes da codificacao
    bits = ["" for y in xrange(len(freq))]

    # Cria um array de arrays (numero de ocorrencias,valor, codificação) organizado por ordem crescente
    dic = sorted(list(t) for t in zip(freq, simbolos, bits))

    # remove ocorrencias nulas do array
    while dic[0][0] == 0:
        dic.remove(dic[0])

    # implementa uma fila para simular o funcionamento do algoritmo
    p = Queue.PriorityQueue()
    # popula a fila com os valores do array
    for value in dic:
        p.put(value)
    # enquanto o fila tiver mais que um nó
    while p.qsize() > 1:
        # extrai os dois nós esquerda e direita com o valor mais pequeno
        l, r = p.get(), p.get()
        # itera no array de valores e nos simbolos dos nós
        for i in xrange(len(dic)):
            for z in xrange(len(l[1])):
                # se o simbolo no dicionario for igual ao simbolo do nó extraido
                if dic[i][1][0] == l[1][z]:
                    # para o no da esquerda guarda o bit 0 na codificação
                    dic[i][2] += '0'
            for t in xrange(len(r[1])):
                if dic[i][1][0] == r[1][t]:
                    dic[i][2] += '1'

        p.put([l[0] + r[0], l[1] + r[1]])

    # inverte a string com a codificação para representar o percurso da raiz até as folhas
    for i in xrange(len(dic)):
        dic[i][2] = dic[i][2][::-1]

    # imprime a array resultante em formato tabela
    pprint.pprint(dic)

    return dic

# 2

"""
Elabore uma função ("codiﬁca") que dada uma mensagem (sequência de símbolos) e a tabela da ponto anterior,
retorne uma sequência de bits com a mensagem codiﬁcada.
"""


def codifica(seqsimbo, tabela_cod):
    seqbits = bitarray()
    for i in xrange(len(seqsimbo)):
        for z in xrange(len(tabela_cod)):
            if seqsimbo[i] == tabela_cod[z][1][0]:
                seqbits += bitarray(tabela_cod[z][2])

    return seqbits

# 3

"""
Elabore uma função ("descodiﬁca") que dada uma sequência de bits (mensagem codiﬁcada) e a tabela do ponto
1, retorne uma sequência de símbolos (mensagem descodiﬁcada).
"""


def descodifica(seqbits, tabela_cod):
    seqsimbo = np.zeros(len(tabela_cod))
    for i in xrange(len(tabela_cod)):
        if seqsimbo[i] == tabela_cod[i][2]:
            seqbits += bitarray(tabela_cod[z][2])

    return seqbits

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

"""
-----------------------MAIN----------------------------
"""


# Lê a imagem em níveis de cinzento
x = cv2.imread("lena.tiff", cv2.IMREAD_GRAYSCALE)
# Converte a imagem (matriz) numa sequência de números (array)
xi = x.ravel()
# Calcula o histogram
h, bins, patches = plt.hist(xi, 256, [0, 256])

# Gera o código de Huffman
t0 = time()
tabela_codigo = gera_huffman(h)
t1 = time()
print "time:", t1-t0


# Codifica e grava ficheiro
seq_bit0 = codifica(xi, tabela_codigo)

escrever(seq_bit0, filename)
t2 = time()
print "time:", t2-t1

# Lê ficheiro e descodifica
seq_bit1 = ler(filename)
yi = descodifica(seq_bit1 ,tabela_codigo)
t3 = time()
print "time:", t3-t2
size_ini = path.getsize("filename original image")
size_end = path.getsize("filename compressed")
print "taxa: ", 1. * size_ini / size_end
plt.show()
cv2.waitKey(0)
plt.close("all")
cv2.destroyAllWindows()
