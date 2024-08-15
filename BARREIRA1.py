import random
import threading
import time

class Forca:
    def __init__(self, palavra):
        self.palavra = palavra.upper()
        self.tamanho = len(self.palavra)
        self.ocultada = ['_'] * self.tamanho
        self.letras_escolhidas = []
        self.vencedor = None
        #self.lock = threading.Lock()  # Lock para proteger seções críticas

    def chutar(self, letra, posicao, jogador_nome):
       #with self.lock:  # Protege a operação crítica
            letra = letra.upper()
            if posicao < 0 or posicao >= self.tamanho or self.ocultada[posicao] != '_':
                return False
            if self.palavra[posicao] == letra:
                self.ocultada[posicao] = letra
                self.letras_escolhidas.append(letra)
                if self.esta_completa():
                    self.vencedor = jogador_nome  # Armazena o nome do jogador vencedor
                return True
            self.letras_escolhidas.append(letra)
            return False

    def esta_completa(self):
        return '_' not in self.ocultada

    def faltam_menos_que_quarenta_porcento_das_letras(self):
        letras_ocultas = self.ocultada.count('_')
        return letras_ocultas < (self.tamanho * 0.4)

class Barreira:
    def __init__(self, quantidade_threads):
        self.num_threads = quantidade_threads  # Número de threads que precisam esperar na barreira
        self.contador = 0               # Contador de threads que chegaram à barreira
        self.condicao = threading.Condition()  # Condição para sincronizar as threads
        self.jogo_finalizado = threading.Event()
    
    def esperar(self):
        with self.condicao:
            if self.jogo_finalizado.is_set():
                return  # Sai se o jogo foi finalizado
            self.contador += 1  # Incrementa o contador quando uma thread chega à barreira
            if self.contador == self.num_threads:
                print("Todos os jogadores chegaram à barreira.")
                self.contador = 0  # Reinicia o contador para a próxima rodada de sincronização
                self.condicao.notify_all()  # Desbloqueia todas as threads que estavam esperando
            else:
                self.condicao.wait()  # Espera até que todas as threads cheguem à barreira

barreira = Barreira(5)

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

def escolher_palavra(palavras):
    return random.choice(palavras)

def calcular_numeros_primos(n):
    primos = []
    for num in range(2, n):
        is_primo = all(num % i != 0 for i in range(2, int(num**0.5) + 1))
        if is_primo:
            primos.append(num)
    return len(primos)

class Jogador(threading.Thread):
    def __init__(self, nome, forca, palavras, barreira):
        threading.Thread.__init__(self)
        self.nome = nome
        self.forca = forca
        self.palavras = palavras
        self.barreira = barreira

    def run(self):
        while not self.forca.esta_completa():
            if self.forca.faltam_menos_que_quarenta_porcento_das_letras():
                possivel_palavra = self.buscar_possivel_palavra()
                if possivel_palavra:
                    print(f'{self.nome} tenta adivinhar a palavra: {possivel_palavra}')
                    #with self.forca.lock:
                    if possivel_palavra.upper() == self.forca.palavra:
                        self.forca.ocultada = list(possivel_palavra.upper())
                        self.forca.vencedor = self.nome  # Jogador vence ao descobrir a palavra completa

                        break

            posicoes_disponiveis = [i for i, letra in enumerate(self.forca.ocultada) if letra == '_']
            if not posicoes_disponiveis:
                break

            posicao = random.choice(posicoes_disponiveis)
            letra = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            if self.forca.chutar(letra, posicao, self.nome):
                print(f'{self.nome} acertou a letra {letra} na posição {posicao + 1}!')
            else:
                print(f'{self.nome} errou com a letra {letra} na posição {posicao + 1}.')

            print('Palavra atual:', ' '.join(self.forca.ocultada))

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

            # Espera na barreira
            self.barreira.esperar()

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

livros = ['livro1.txt', 'livro2.txt', 'livro3.txt', 'livro4.txt', 'livro5.txt']
todas_palavras = []
palavras1 = []
palavras2 = []
palavras3 = []
palavras4 = []
palavras5 = []

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

palavra_jogo = escolher_palavra(todas_palavras)
forca = Forca(palavra_jogo)

jogador1 = Jogador('Jogador 1', forca, palavras1, barreira)
jogador2 = Jogador('Jogador 2', forca, palavras2, barreira)
jogador3 = Jogador('Jogador 3', forca, palavras3, barreira)
jogador4 = Jogador('Jogador 4', forca, palavras4, barreira)
jogador5 = Jogador('Jogador 5', forca, palavras5, barreira)

jogador1.start()
jogador2.start()
jogador3.start()
jogador4.start()
jogador5.start()

jogador1.join()
jogador2.join()
jogador3.join()
jogador4.join()
jogador5.join()

# Print final do jogo
if forca.esta_completa():
    print('Parabéns! A palavra foi completada:', ''.join(forca.ocultada))
    print(f'O vencedor é: {forca.vencedor}!')
else:
    print('O jogo terminou. A palavra era:', forca.palavra)
