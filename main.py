import math
import turtle
import os
import time

class Projetil:
    def __init__(self, velocidade, angulo, y0, gravidade):
        """
        Inicializa os parâmetros do projétil.
        
        velocidade: velocidade inicial (m/s)
        angulo: ângulo de lançamento (graus)
        y0: altura inicial (m)
        gravidade: aceleração da gravidade (m/s²)
        """
        self.velocidade = velocidade
        self.angulo = angulo
        self.y0 = y0
        self.gravidade = gravidade
        
        # Calcula valores usados no movimento
        
        # Converte o ângulo de graus para radianos (necessário para usar com funções trigonométricas)
        self.angulo_rad = math.radians(self.angulo)
        
        # vx = velocidade horizontal constante (não muda, pois não há resistência do ar)
        self.vx = self.velocidade * math.cos(self.angulo_rad)
        
        # vy = velocidade vertical inicial (vai diminuindo ao longo do tempo por causa da gravidade)
        self.vy = self.velocidade * math.sin(self.angulo_rad)
        
        # Criamos a lista de pontos que representam a posição do projétil em cada instante de tempo
        self.pontos = []
        
        # Tempo total de voo (segundos)
        self.tempo_voo = 0 

    def calcular_trajetoria(self):
        """
        Calcula a lista de pontos (x,y) da trajetória do projétil
        e o tempo total de voo.
        """
        self.pontos = [(0, self.y0)] # Começamos no ponto (x=0, y=y0), ou seja, na posição inicial
        tempo = 0 # Tempo inicial (segundos)
        intervalo = 0.05 # De quanto em quanto tempo vamos calcular a posição (0.05s = 50 milissegundos)
        
        # Loop para calcular a posição do projétil a cada intervalo de tempo
        while True:
            
            # x = posição horizontal no tempo atual
            x = self.vx * tempo  # Como vx é constante, só multiplicamos pelo tempo
            
            # Cálculo da posição vertical (y):
            # Primeiro, a parte positiva: o quanto o projétil sobe devido à velocidade inicial vertical
            subida = self.vy * tempo

            # Depois, a parte negativa: o quanto ele cai por causa da gravidade
            queda = 0.5 * self.gravidade * tempo ** 2  # Fórmula da física: (1/2) * g * t²

            # Posição final no eixo Y: soma da altura inicial + subida - queda
            y = self.y0 + subida - queda
            
            # Se o projétil caiu no chão (y < 0), encerramos o cálculo
            if y < 0:
                break
            
            # Adiciona o ponto (x, y) à lista de posições
            self.pontos.append((x, y))
            
            # Avança o tempo
            tempo += intervalo
        
        self.tempo_voo = tempo
    
    def exibir_resultados(self):
        """
        Mostra tempo de voo, altura máxima e distância total no console.
        """
        altura_maxima = self.pontos[0][1]
        distancia_total = self.pontos[0][0]

        for x, y in self.pontos:
            if y > altura_maxima:
                altura_maxima = y
            if x > distancia_total:
                distancia_total = x
                
        print("\033[1;36m\n=== Resultados ===\033[0m")
        time.sleep(1)
        print(f"\033[1;33mAltura máxima:\033[0m {altura_maxima:.2f} metros")
        time.sleep(1)
        print(f"\033[1;33mDistância percorrida:\033[0m {distancia_total:.2f} metros")
        time.sleep(1)
        print(f"\033[1;33mTempo de voo:\033[0m {self.tempo_voo:.2f} segundos\n")
        time.sleep(1)
    
    def desenhar_trajetoria(self):
        """
        Desenha a trajetória usando a biblioteca turtle.
        """
        import turtle

        turtle.title("Trajetória do Projétil")
        turtle.bgcolor("white")
        turtle.speed(0)

        escala = 1
        margem = 50

        max_x = self.pontos[0][0]
        max_y = self.pontos[0][1]

        for x, y in self.pontos:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        turtle.setworldcoordinates(
            -margem,
            -margem - self.y0 * escala,
            max_x * escala + margem,
            max_y * escala + margem
        )

        # Linha do chão
        turtle.penup()
        turtle.goto(-margem, 0)
        turtle.pendown()
        turtle.color("black")
        turtle.pensize(4)
        turtle.goto(max_x * escala + margem, 0)

        # Ponto de lançamento
        turtle.penup()
        turtle.goto(self.pontos[0][0] * escala, self.pontos[0][1] * escala)
        turtle.dot(20, "red")

        # Desenha a trajetória com pontos
        turtle.setheading(self.angulo)
        turtle.pendown()
        turtle.color("blue")
        turtle.pensize(2)
        for x, y in self.pontos:
            turtle.goto(x * escala, y * escala)
            turtle.dot(5, "red")  # Pequeno ponto vermelho em cada ponto

        # Ponto final (queda)
        x_final, y_final = self.pontos[-1]
        turtle.color("red")
        turtle.dot(10, "red")

        # Texto de informações
        turtle.penup()
        turtle.goto(x_final * escala + 10, y_final * escala + 10)
        turtle.color("black")
        turtle.write(
            f"Impacto!\n"
            f"Tempo = {self.tempo_voo:.2f} s\n"
            f"Altura Máxima = {max_y:.2f} m\n"
            f"Distância Total = {x_final:.2f} m",
            font=("Arial", 12, "normal")
        )

        turtle.hideturtle()
        turtle.done()

def simular():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\033[1;35m=== Simulador de Projétil ===\033[0m")
    print("Sugestão de valores:")
    print("- Velocidade: entre 10 e 50 m/s")
    print("- Ângulo: entre 0 e 45 graus")
    print("- Altura inicial: entre 0 e 10 metros")
    print("- Gravidade: normalmente 9.8 m/s²")

    velocidade = float(input("\nVelocidade inicial (m/s): "))
    if velocidade < 0:
        print("Velocidade não pode ser negativa.")
        return

    angulo = float(input("Ângulo de lançamento (graus): "))
    if angulo < 0 or angulo > 90:
        print("Ângulo deve estar entre 0 e 90 graus.")
        return

    y0 = float(input("Altura inicial (m): "))
    if y0 < 0:
        print("Altura inicial não pode ser negativa.")
        return

    gravidade = float(input("Gravidade (m/s²): "))
    if gravidade <= 0:
        print("Gravidade deve ser um valor positivo.")
        return

    proj = Projetil(velocidade, angulo, y0, gravidade)

    print("\033[1;34m\nCalculando trajetória...\033[0m")
    time.sleep(1)
    proj.calcular_trajetoria()

    print("\033[1;34mExibindo resultados...\033[0m")
    time.sleep(1)
    proj.exibir_resultados()

    resposta = input("Deseja exibir o gráfico da simulação? (s/n): ").strip().lower()
    if resposta == "s":
        print("\033[1;34mAbrindo janela de simulação gráfica...\033[0m")
        time.sleep(2)
        proj.desenhar_trajetoria()
    else:
        print("\033[1;32mSimulação encerrada sem exibição gráfica.\033[0m")

# Executa a simulação
simular()
