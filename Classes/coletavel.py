from settings import Retangulo, math
import Biblioteca.transformacoes as t

class Coletavel():
    def __init__(self, pos, largura, altura, cor, tipo, forma = "retangular", imagem = None):
        self.tipo = tipo
        self.pos = pos 
        self.largura = largura
        self.altura = altura
        self.imagem = imagem
        self.cor = cor
        self.forma = forma
        self.ativo = True
        
        # Variáveis para a rotação por matriz de rotação y
        self.angulo = 0.0
        self.velocidade_giro = 0.05

        meia_l = largura / 2
        meia_a = altura / 2
        self.vertices_locais_3d = [
            [[-meia_l], [-meia_a], [0]],  # Superior Esquerdo
            [ [meia_l], [-meia_a], [0]],  # Superior Direito
            [ [meia_l], [meia_a], [0]],  # Inferior Direito
            [[-meia_l],  [meia_a], [0]]   # Inferior Esquerdo
        ]
        
        self._vertices_rotacionados = []

        self.retangulo = Retangulo(self.pos.x, self.pos.y, largura, altura)
        self.centro = None
        self.raio = None
        self.atualizar()

    @property
    def vertices(self):
        if self.tipo == "moeda":
            return self._vertices_rotacionados
        return self.retangulo.vertices

    def atualizar(self):
        if not self.ativo:
            return

        self.angulo += self.velocidade_giro

        centro_x_mundo = self.pos.x + (self.largura / 2)
        centro_y_mundo = self.pos.y + (self.altura / 2)

        # 3. Executa a rotação 3D vértice por vértice
        matriz_atual = t.rotacao_y(self.angulo)
        novos_pontos = []
        
        for v in self.vertices_locais_3d:
            v_rotacionado = t.produto_matriz(matriz_atual, v)
            
            x_final = v_rotacionado[0] + centro_x_mundo
            y_final = v_rotacionado[1] + centro_y_mundo
            novos_pontos.append((x_final, y_final))
            
        self._vertices_rotacionados = novos_pontos