# Nome do jogo

Jogo de plataforma em 2D com estilo visual pixel art, onde o jogador passa por cenário típicos da Uece - Campus Itapery (divididos em três fases) e enfrenta um grande vilão ao final.


# Árvore do projeto

```
.
├── Assets
│   ├── parede-pedra-1.png 
|   ├── predio-quebrado.png
│   ├── PressStart2P-Regular.ttf 
│   ├── tapioca.png 
│   ├── textura-tijolos.png
│   ├── tijolos-escuros.png
│   └── uece-noite.png
├── Biblioteca
│   ├── algoritmos.py  (algoritmos das aulas)
│   └── transformacoes.py (matrizes de transformações lineares)
├── Classes
│   ├── arma.py  (arma do jogador)
|   ├── cachorro (classe de inimigo)
│   ├── camera.py 
│   ├── cenario.py
│   ├── coletavel.py (classe mãe de todos os coletáveis)
│   ├── equipamento.py (equipamento do jogador ou zumbi)
│   ├── humanoide.py (classe mãe de jogador e zumbi)
│   ├── jogador.py 
│   ├── plataforma.py
│   ├── projetil.py (classe para todo ataque a distância com arma)
│   ├── retangulo.py (classe para colisão)
│   ├── tapioca.py (classe de alimento coletável que aumenta vida)
│   ├── vetor.py (classe para física)
│   └── zumbi.py (classe de inimigo)
├── converter.py (script de conversão de txt para csv)
├── Docs
│   └── jogo.gdd (ideias do jogo)
├── Gerenciador
│   ├── Atualizador.py (classe para atualização das entidades)
│   ├── Inicializador.py (classe para inicialização de um jogo)
│   └── Renderizador.py (classe para desenhar as entidades)
├── jogo.py (classe principal)
├── Mapas
│   ├── fase1.csv 
│   ├── fase2.csv
│   ├── fase3.csv
│   ├── fase4.csv
│   ├── fase5.csv
│   └── txts
│       ├── fase1.txt
│       ├── fase2.txt
│       ├── fase3.txt
│       ├── fase4.txt
│       └── fase5.txt
├── README.md
├── settings.py
└── Sprites 
    ├── zumbi_idle_0.png
    ├── zumbi_idle_1.png
    ├── zumbi_idle_2.png
    ├── zumbi_idle_3.png
    ├── zumbi_idle_4.png
    ├── zumbi_idle_5.png
    ├── zumbi_idle_6.png
    ├── zumbi_idle_7.png
    ├── zumbi_walk_left_0.png
    ├── zumbi_walk_left_1.png
    ├── zumbi_walk_left_2.png
    ├── zumbi_walk_left_3.png
    ├── zumbi_walk_left_4.png
    ├── zumbi_walk_left_5.png
    ├── zumbi_walk_left_6.png
    ├── zumbi_walk_left_7.png
    ├── zumbi_walk_right_0.png
    ├── zumbi_walk_right_1.png
    ├── zumbi_walk_right_2.png
    ├── zumbi_walk_right_3.png
    ├── zumbi_walk_right_4.png
    ├── zumbi_walk_right_5.png
    ├── zumbi_walk_right_6.png
    └── zumbi_walk_right_7.png
```

# Ideias para aplicar
## Transformações lineares
```
Teleport - Translação
Giro nos coletáveis - Rotação
Chefe gigante - Escala
```

## Inimigos
```
Zumbi - inimigo básico
Doutor zumbi - inimigo básico que lança livros
Cachorro fantasma - inimigo imortal
Pombo tóxico - inimigo aéreo
```

# Cenário
## Estruturas 
```
NC2A - prédio top - fusível vai está lá
Reitoria
Carrinho do Billy - melhor lugar para lanchar
RU - muita comida - tapioca tem que existir
Biblioteca central - documentos importantes
Prédio da Medicina - existe uma cura??
```
## Background
```
Lua - simbolizar noite
Árvores - uece é muito arborizada
Nuvens - céu bem cheio - parallax?
Estrelas - céu estrelado
```

# Lore
```
Em um mundo pós apocalíptico, é preciso visitar universidades para encontrar pesquisas úteis para mitgar pragas e curar pessoas, qualquer recurso é bem vindo. Você foi contratado para uma missão impossível, ir à uma universidade chamada Uece, coletar itens importantes e voltar com vida (a parte mais difícil, pois você não espera o que existe naquele local sombrio...). 
```

# Mecânicas 
```
Pulo (duplo?)
Corrida
Tiro
Ataque corpo a corpo
Lançar granadas ( temos que fazer isso kkk)
```

# Coletáveis
```
Tapioca ( cura vida )
Munição ( aumenta estoque para tiro)
Fusível ( missão principal )
Remédio ( missão principal)
Pacotes de comida ( missão principal )
Protótipo tecnológico ( melhoria de arma )
Moedas ( comprar alguma coisa )
Refrigerante ( aumentar velocidade - pulo duplo? dash? )
```

# Dificuldades
```
Fácil - Dano de inimigo = 10
Médio -  Dano de inimigo = 20
Difícil - Dano de inimigo = 40
```