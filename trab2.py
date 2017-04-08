# This Python file uses the following encoding: utf-8

# Trabalho 2 CSM

from time import time
from os import path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Queue
import pprint


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
    tabela = sorted(list(t) for t in zip(freq, simbolos, bits))

    # remove ocorrencias nulas do array
    while tabela[0][0] == 0:
        tabela.remove(tabela[0])

    # implementa uma fila para simular o funcionamento do algoritmo
    p = Queue.PriorityQueue()
    # popula a fila com os valores do array
    for value in tabela:
        p.put(value)
    # enquanto o fila tiver mais que um nó
    while p.qsize() > 1:
        # extrai os dois nós esquerda e direita com o valor mais pequeno
        l, r = p.get(), p.get()
        # itera no array de valores e nos simbolos dos nós
        for i in xrange(len(tabela)):
            for z in xrange(len(l[1])):
                # se o simbolo no dicionario for igual ao simbolo do nó extraido
                if tabela[i][1][0] == l[1][z]:
                    # para o no da esquerda guarda o bit 0 na codificação
                    tabela[i][2] += '0'
            for t in xrange(len(r[1])):
                if tabela[i][1][0] == r[1][t]:
                    tabela[i][2] += '1'

        p.put([l[0] + r[0], l[1] + r[1]])

    # inverte a string com a codificação para representar o percurso da raiz até as folhas
    for i in xrange(len(tabela)):
        tabela[i][2] = tabela[i][2][::-1]

    # imprime a array resultante em formato tabela
    pprint.pprint(tabela)

    return tabela


# 2

"""
Elabore uma função ("codiﬁca") que dada uma mensagem (sequência de símbolos) e a tabela da ponto anterior,
retorne uma sequência de bits com a mensagem codiﬁcada.
"""


def codifica(mensagem, tabela_cod):

    # Sequencia de bits com a codificação da mensagem
    seqbits = ""

    # bits do Header
    bits_header = 0

    # bits mensagem
    bits_msg = 0

    # segmento de 8 bits com o numero de simbolos com ocorrencias não nulas
    num_simb_activos = '{0:08b}'.format(len(tabela_cod))

    # adiciona o n simbolos ao header e incrementa o contador
    seqbits += num_simb_activos
    bits_header += 8

    # dicionario para guardar pares chave(simbolo) valor(codificacao)
    dic = {}

    # itera na tabela de codigo para criar o header
    for r in xrange(len(tabela_cod)):
        # adiciona o simbolo ao header
        seqbits += '{0:08b}'.format(tabela_cod[r][1][0])
        # adiciona ao header a dim em nº bits resultante da codificação do simbolo
        seqbits += '{0:06b}'.format(len(tabela_cod[r][2]))
        # adiciona ao header a codificação do simbolo
        seqbits += tabela_cod[r][2]
        # adiciona valores ao dicionario
        dic[tabela_cod[r][1][0]] = tabela_cod[r][2]
        # incrementa contador bits
        bits_header += 8 + 6 + len(tabela_cod[r][2])

    # itera para criar a mensagem
    for i in xrange(len(mensagem)):
        seqbits += dic[mensagem[i]]
        bits_msg += len(dic[mensagem[i]])

    print "O numero de bits da mensagem original é {}".format(len(mensagem)*8)
    print "O numero de bits do header da mensagem codificada é {}".format(bits_header)
    print "O numero de bits de dados da mensagem codificada (sem header) é {}".format(bits_msg)
    print "O numero de bits total da mensagem codificada é {}".format(bits_header+bits_msg)
    print "A dimensão do Ficheiro comprimido é {}% relativamente à dimensão original".format(
        round((float(bits_header+bits_msg)/float(len(mensagem)*8))*100., 2))
    saldo_bits = (len(mensagem)*8) - (bits_header + bits_msg)
    if saldo_bits > 0:
        print "Através da codificação de Huffman conseguimos 'poupar' {} bits".format(saldo_bits)
    else:
        print "Neste caso a codificação de Huffman não foi eficiente e 'gastamos' {} bits".format(abs(saldo_bits))
    print "Não levando o header em consideração os valores passam para {} e {} respectivamente".format(
        round((float(bits_msg)/(len(mensagem)*8))*100., 2), (len(mensagem)*8) - bits_msg)

    return seqbits


# 3

"""
Elabore uma função ("descodiﬁca") que dada uma sequência de bits (mensagem codiﬁcada) e a tabela do ponto
1, retorne uma sequência de símbolos (mensagem descodiﬁcada).
"""


def descodifica(msg_cod):

    # dicionario para reconstruir os pares chave valor
    dic = {}

    # segmento de 8 bits com o numero de simbolos activos e o numero de ocorrencias dos simbolos
    num_simb_activos = int(msg_cod[0:8], 2)

    # slice da mensagem para excluir o oito bits lidos
    msg_cod = msg_cod[8:]

    # sequencia de simbolos para output
    seq_simbolos = []

    # variavel temporaria
    count = 0

    # leitura do header
    for i in xrange(num_simb_activos):
        # lê o simbolo, neste caso um numero
        simbolo = int(msg_cod[0:8], 2)
        # lê o comprimento do codigo
        l_cod = int(msg_cod[8:14], 2)
        # retira a codificação do simbolo
        cod = msg_cod[14:(14 + l_cod)]
        # adiciona os valores ao dicionario
        dic[cod] = simbolo
        # conta os bits utilizados
        count += 8 + 6 + l_cod

    # faz o slice da mensagem para excluir a parte do header
    msg_cod = msg_cod[count:]

    # lê os bits codificados enquanto houver dados para leitura
    while msg_cod:
        for k in dic:
            # avalia o prefixo inicial de acordo com a chave do dicionario
            if msg_cod.startswith(k):
                # quando encontramos a chave correta adicionamos o valor ao array de simbolos
                seq_simbolos.append(dic[k])
                # e slice da mensagem de bits para lermos sempre a partir do inicio
                msg_cod = msg_cod[len(k):]

    return seq_simbolos


# 4

"""
Elabore uma função ("escrever") que dada uma sequência de bits (mensagem codiﬁcada) e o nome do ﬁcheiro,
escreva a sequência de bits para o ﬁcheiro.
"""


def escrever(seqbits, nomeficheiro):
    f = open("{}".format(nomeficheiro), "w+")
    file_array = np.fromstring(seqbits, dtype=np.uint8)
    file_array.tofile(f)
    f.close()


# 5

"""
Elabore uma função ("ler") que dado o nome do ﬁcheiro, leia uma sequência de bits (mensagem codiﬁcada)
contida no ﬁcheiro.
"""


def ler(nomeficheiro):
    f = open("{}".format(nomeficheiro))
    file_array = np.fromfile(f, dtype=np.uint8)
    seqbits = np.array2string(file_array)
    f.close()
    return seqbits


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
files = np.array(['Lena.tiff', 'ubuntu_server_guide.pdf', 'ubuntu_server_guide.txt', 'HenryMancini-PinkPanther.mp3',
                 'HenryMancini-PinkPanther.mid', 'ecg.txt'])
# x = np.fromfile("lena.tiff", 'uint8')
# Lê a imagem em níveis de cinzento
x = cv2.imread("lena.tiff", cv2.IMREAD_GRAYSCALE)
cv2.imwrite('lena_gray_scale.bmp', x)
# Converte a imagem (matriz) numa sequência de números (array)
xi = x.ravel()
# Calcula o histogram
h, bins, patches = plt.hist(xi, 256, [0, 256])

# Gera o código de Huffman
t0 = time()
tabela_codigo = gera_huffman(h)
t1 = time()
print "time:", t1 - t0

# Codifica e grava ficheiro
seq_bit0 = codifica(xi, tabela_codigo)

escrever(seq_bit0, "teste.txt")
t2 = time()
print "time:", t2 - t1

# Lê ficheiro e descodifica
seq_bit1 = ler(filename)
yi = descodifica(seq_bit1, tabela_codigo)
t3 = time()
print "time:", t3 - t2
size_ini = path.getsize("filename original image")
size_end = path.getsize("filename compressed")
print "taxa: ", 1. * size_ini / size_end
plt.show()
cv2.waitKey(0)
plt.close("all")
cv2.destroyAllWindows()
