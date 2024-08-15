import random
import threading
import time


# O jogo escolhe uma palavra aleatóriamente dentre as palavras dos 5 livros disponíveis.
# Todos os 5 livros são de dominio público e sobre computação.
# Para garantir um melhor funcionamento do jogo limitei as plavras entre 5 e 10 letras. 
# o jogo desmonstra a quantidade de letras na pavras em um "_" para cada letra. Cada letra correta descoberta o "_"  é substituido pela letra correta. Ou seja na medida que se acerta a letra ela é revelada.
# o problema de condição de corrida ocorre quando duas ou mais threads tentam acessar a mesma posição da palavra de forma simultânea. 

    
class Forca:
    def __init__(self, palavra):
        #as letras são convertidas para maiusculas
        self.palavra = palavra.upper()
        #retorna o comprimento da palavra
        self.tamanho = len(self.palavra)
        #cria uma lista com "_" para cada letra da palavra
        self.ocultada = ['_'] * self.tamanho
        #lista para armazenar as letras que foram escolhidas pelo jogador
        self.letras_escolhidas = []
        self.vencedor = None
    def chutar(self, letra, posicao):
        #a letra é convertida para maiuscula
        letra = letra.upper()
        #verifica se a posição é válida e disponível. 
        if posicao < 0 or posicao >= self.tamanho or self.ocultada[posicao] != '_':
            return False
        #verifica se a letra escolhida é igual a letra da palavra na posição especifica
        if self.palavra[posicao] == letra:
            self.ocultada[posicao] = letra
            self.letras_escolhidas.append(letra)
            if self.esta_completa():
                self.vencedor = jogador_nome  # Armazena o nome do jogador vencedor
            return True
           
        self.letras_escolhidas.append(letra)
        return False

    #verifica se a palavra foi completada
    def esta_completa(self):
        return '_' not in self.ocultada
    #verifica se a quantidade de letras ocultas é menor que 40% da quantidade total de letras da palavra
    def faltam_menos_que_quarenta_porcento_das_letras(self):
        letras_ocultas = self.ocultada.count('_')
        return letras_ocultas < (self.tamanho * 0.4)



#carrega os livros
def carregar_livro(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            texto = f.read()
        palavras = texto.split()
        palavras = [palavra for palavra in palavras if 5 <= len(palavra) <= 10]
        return palavras
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")
        return []

#escolha da palavra de forma aleatória 
def escolher_palavra(palavras):
    return random.choice(palavras)


# Para "distrair/manter ocupada as treads" elas realizam operações matematicas, para que enquanto umas estão fazendo o calculo outra consiga acessar a região crítrica e fazer a operação. 
# o jogo desmonstra o tempo de cálculo de números primos para cada thread.
def calcular_numeros_primos(n):
    #números primos são aquele que possuem apensas dois divisores, o 1 e o próprio número.
    primos = []
    for num in range(2, n):
        is_primo = all(num % i != 0 for i in range(2, int(num**0.5) + 1))
        if is_primo:
            primos.append(num)
    return len(primos)


# Criar jogadores
class Jogador(threading.Thread):
    def __init__(self, nome, forca, palavras):
        threading.Thread.__init__(self)
        self.nome = nome
        self.forca = forca
        self.palavras = palavras


    def run(self):
        while not self.forca.esta_completa():
            if self.forca.faltam_menos_que_quarenta_porcento_das_letras():
                possivel_palavra = self.buscar_possivel_palavra()
                if possivel_palavra:
                    print(f'{self.nome} tenta adivinhar a palavra: {possivel_palavra}')
                    if possivel_palavra.upper() == self.forca.palavra:
                        self.forca.ocultada = list(possivel_palavra.upper())
                        self.forca.vencedor = self.nome  # Jogador vence ao descobrir a palavra completa
                        break

            posicoes_disponiveis = [i for i, letra in enumerate(self.forca.ocultada) if letra == '_']
            if not posicoes_disponiveis:
                break
        
            posicao = random.choice(posicoes_disponiveis)
            letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            if self.forca.chutar(letra, posicao):
                print(f'{self.nome} acertou a letra {letra} na posição {posicao + 1}!')
            else:
                print(f'{self.nome} errou com a letra {letra} na posição {posicao + 1}.')

            print('Palavra atual:', ' '.join(self.forca.ocultada))

            # Medir o tempo para calcular números primos
            inicio = time.time()
            try:

                aleatorio = random.choice([10000, 20000, 50000, 600, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000])
                num_primos = calcular_numeros_primos(aleatorio)
            except Exception as e:
                print(f'Erro ao calcular números primos: {e}')
                num_primos = 0
            fim = time.time()
            duracao = fim - inicio

            print(f'{self.nome} calculou {num_primos} números primos (Tempo de cálculo: {duracao:.2f} segundos)')

    def buscar_possivel_palavra(self):
        for palavra in self.palavras:
            if len(palavra) == self.forca.tamanho:
                match = True
                for i, letra in enumerate(self.forca.ocultada):
                    if letra != '_' and letra != palavra[i].upper():
                        match = False
                        break
                if match:
                    return palavra
        return None

# Carregar os livros
livros = ['livro1.txt', 'livro2.txt', 'livro3.txt', 'livro4.txt', 'livro5.txt']
todas_palavras = []
palavras1 = []
palavras2 = []
palavras3 = []
palavras4 = []
palavras5 = []

# Carregar as palavras dos livros
for livro in livros:
    palavras = carregar_livro(livro)
    todas_palavras.extend(palavras)

    if livro == 'livro1.txt':
        palavras1.extend(palavras)

    elif livro == 'livro2.txt':
        palavras2.extend(palavras)

    elif livro == 'livro3.txt':
        palavras3.extend(palavras)

    elif livro == 'livro4.txt':
        palavras4.extend(palavras)

    elif livro == 'livro5.txt':
        palavras5.extend(palavras)

# Escolher uma palavra aleatória
palavra_jogo = escolher_palavra(todas_palavras)

# Inicializar o jogo
forca = Forca(palavra_jogo)

# Criar jogadores
jogador1 = Jogador('Jogador 1', forca, palavras1)
jogador2 = Jogador('Jogador 2', forca, palavras2)
jogador3 = Jogador('Jogador 3', forca, palavras3)
jogador4 = Jogador('Jogador 4', forca, palavras4)
jogador5 = Jogador('Jogador 5', forca, palavras5)

# Iniciando threads
jogador1.start()
jogador2.start()
jogador3.start()
jogador4.start()
jogador5.start()

# Esperar threads finalizarem
jogador1.join()
jogador2.join()
jogador3.join()
jogador4.join()
jogador5.join()

# Final
if forca.esta_completa():
    print('Parabéns! A palavra foi completada:', ''.join(forca.ocultada))
    print(f'O vencedor é: {forca.vencedor}!')
else:
    print('O jogo terminou. A palavra era:', forca.palavra)
