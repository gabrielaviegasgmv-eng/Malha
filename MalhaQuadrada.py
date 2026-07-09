import numpy as np 
import matplotlib.pyplot as plt
class Malha:
    def __init__(self, base, altura, elemAltura, elemBase):
        self.base = base
        self.altura = altura 

# Eu to dividindo o tamanho da base pelo tamanho de cada elemento -> Descobrir quantos elementos 

        self.nx = int(round(self.base/elemBase))
        self.ny = int(round(self.altura/elemAltura))

# Tô encontrando o tamanho da base e da altura real de cada elemento 

        self.dx = self.base/self.nx
        self.dy = self.altura/self.ny

# Descobrir a quantidade de elementos e nós 

        self.nos = (self.nx + 1) * (self.ny + 1)
        self.elem = (self.nx) * (self.ny)

# Talvez:

        self.coordenadas_nos = None
        self.conectividade = None

    # Função para criar as coordenadas dos nós 

    def criar_coordenadas_nos(self):

# Criar uma tabela com a quantidade de linhas igual ao número de nós e com 2 colunas (coordenada x, coordenada y)

        self.coordenadas_nos = np.zeros((self.nos,2))

        cont_no = 0

        for j in range (self.ny + 1):

            y = j * self.dy

            for i in range (self.nx + 1):

                x = i * self.dx 

                self.coordenadas_nos[cont_no, 0] = x
                self.coordenadas_nos[cont_no, 1] = y

                cont_no += 1

        return self.coordenadas_nos

    def criar_conectividade(self):

        self.conectividade = np.zeros((self.elem,4),dtype=int)

        cont_elem = 0 

        nos_por_linha = self.nx + 1

        for j in range(self.ny):
            for i in range(self.nx):

                n1 = j * nos_por_linha + i 
                n2 = n1 + 1
                n3 = n2 + nos_por_linha
                n4 = n1 + nos_por_linha

                self.conectividade[cont_elem, 0] = n1
                self.conectividade[cont_elem, 1] = n2
                self.conectividade[cont_elem, 2] = n3
                self.conectividade[cont_elem, 3] = n4

                cont_elem += 1
            
        return self.conectividade

    def plotar_malha_completa(self):
        fig, ax = plt.subplots(figsize=(6,6))
        
        for i, elem in enumerate(self.conectividade):
            nos = self.coordenadas_nos[elem]
            x = np.append(nos[:, 0], nos[0, 0])
            y = np.append(nos[:, 1], nos[0, 1])
            ax.plot(x, y, 'k-', lw=1)
            
            cx, cy = np.mean(nos[:, 0]), np.mean(nos[:, 1])
            ax.text(cx, cy, str(i), color='blue', ha='center', va='center', fontweight='bold')
            
        for i, no in enumerate(self.coordenadas_nos):
            ax.plot(no[0], no[1], 'ro', markersize=4)
            ax.text(no[0] + self.dx*0.05, no[1] + self.dy*0.05, str(i), color='red', fontsize=9)
            
        ax.set_aspect('equal')
        ax.set_title("Malha: Nós (Vermelho) e Elementos (Azul)")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

    def plotar_elementos_regiao(self, condicao, titulo):
        """
        Função auxiliar para plotar elementos que satisfazem uma determinada
        condição (expressa por uma função que recebe x e y e retorna True/False).
        O elemento só será colorido se TODOS os seus nós satisfizerem a condição.
        """
        fig, ax = plt.subplots(figsize=(6,6))
        
        # Desenha a malha base (fundo)
        for elem in self.conectividade:
            nos = self.coordenadas_nos[elem]
            x = np.append(nos[:, 0], nos[0, 0])
            y = np.append(nos[:, 1], nos[0, 1])
            ax.plot(x, y, color='lightgray', lw=0.5)

        # Destacar os elementos contidos na região
        for i, elem in enumerate(self.conectividade):
            nos = self.coordenadas_nos[elem]
            
            # Verifica se TODOS os nós deste elemento retornam True para a condição
            if all(condicao(no[0], no[1]) for no in nos):
                x = np.append(nos[:, 0], nos[0, 0])
                y = np.append(nos[:, 1], nos[0, 1])
                # Pinta o interior do elemento
                ax.fill(x, y, color='skyblue', alpha=0.8)
                # Contorno do elemento
                ax.plot(x, y, color='blue', lw=1.5)
                
                # Enumera os elementos destacados
                cx, cy = np.mean(nos[:, 0]), np.mean(nos[:, 1])
                ax.text(cx, cy, str(i), color='black', ha='center', va='center', fontweight='bold')
                
        ax.set_aspect('equal')
        ax.set_title(titulo)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


        
        # Criar uma malha 3x3. Por exemplo, Base 3 e Altura 3, elementos de 1x1.
m = Malha(base=3.0, altura=3.0, elemAltura=1.0, elemBase=1.0)
m.criar_coordenadas_nos()
m.criar_conectividade()

# 1) Plotar malha enumerando nós e elementos
m.plotar_malha_completa()


# Aumentar a malha para melhor visualização das regiões
m_grande = Malha(base=10.0, altura=10.0, elemAltura=0.5, elemBase=0.5)
m_grande.criar_coordenadas_nos()
m_grande.criar_conectividade()

# 2) Plotar todos elementos contidos num círculo de raio r e centro (cx, cy)
cx, cy, r = 5.0, 5.0, 3.5
condicao_circulo = lambda x, y: (x - cx)**2 + (y - cy)**2 <= r**2
m_grande.plotar_elementos_regiao(
    condicao_circulo, 
    f"Elementos contidos no Círculo (centro={cx},{cy} e raio={r})"
)

# 3) Plotar todos elementos contidos num retângulo centrado em (cx, cy) com rb e rh
cx_ret, cy_ret = 5.0, 5.0
rb, rh = 6.0, 4.0
# Se é centrado em cx,cy e tem base rb, varia de cx - rb/2 até cx + rb/2. (Idem pra altura)
condicao_retangulo = lambda x, y: (abs(x - cx_ret) <= rb/2) and (abs(y - cy_ret) <= rh/2)
m_grande.plotar_elementos_regiao(
    condicao_retangulo, 
    f"Elementos contidos no Retângulo (base={rb}, alt={rh})"
)

# 4) Elementos contidos onde y >= eh/2 - (eb/eh)*x
eb, eh = 10.0, 10.0 # Considerando a base e altura totais como eb e eh
condicao_reta = lambda x, y: y >= (eh/2 - (eb/eh)*x)
m_grande.plotar_elementos_regiao(
    condicao_reta, 
    "Elementos contidos em: y >= eh/2 - (eb/eh)*x"
)

# 5) Elementos contidos em uma região regida por múltiplas inequações a_i*y + b_i*x <= 1
# Exemplo de lista de (a_i, b_i)
inequacoes = [
    (0.1, 0.05), # 0.1*y + 0.05*x <= 1
    (0.02, 0.1)  # 0.02*y + 0.1*x <= 1
]
def condicao_inequacoes(x, y):
    # Retorna True se TODAS as inequações da lista forem respeitadas para aquele (x,y)
    return all((a * y + b * x <= 1) for a, b in inequacoes)

m_grande.plotar_elementos_regiao(
    condicao_inequacoes, 
    "Elementos contidos no sistema de inequações"
)