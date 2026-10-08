# Nome do jogo

Jogo de plataforma em 2D com estilo visual pixel art, onde o jogador passa por cenário típicos da Uece - Campus Itapery (divididos em três fases) e enfrenta um grande vilão ao final.

## Funcionalidades
* Set Pixel -> todo o jogo foi renderizado pixel por pixel
* Primitivas de Rasterização 
    * Linha -> modelagem dos prédios, botões do menu
    * Círculo -> modelagem da Lua
    * Elipse -> modelagem das nuvens
* Preenchimento de Regiões 
    * Flood Fill/Boundary Fill -> foi usado principalmente no menu, mas também em partes do cenário, como Lua, nuvens e carrinho do Billy
    * Scanline -> usado no jogo em si (mapas, viewport, cenário)
* Transformações Geométricas 
    * Rotação -> Giro em coletável (moeda)
    * Translação -> Teleport 
    * Escala -> Viewport(minimapa)
* Animação 2D -> Movimentação dos personagens
* Janela e Viewport -> criação de minimapa 
* Recorte de Cohen-Sutherland (Clipping) -> usado no minimapa para plataformas que estavam nas bordas da viewport
* Mapeamento de Textura -> Sprites dos personagens e componentes do cenário
* Input (Teclado e/ou Mouse) -> Usado no menu e para movimentar o jogador 

## Lore
Um cientista conhecido como Dr. M trabalhava em uma universidade chamada Uece, e era muito bom em suas pesquisas. Em um de seus projetos, chamado TPBST (Teleportation breaks through space and time), conseguiu construir um portal que teletransporta pessoas de um lugar à outro instantaneamente. Mas ele não se contentava facilmente, por isso decidiu trabalhar em um mais ousado. O (Nome do projeto) visava evoluir todas as características de seres vivos, força, resistência, inteligência, habilidades motoras, etc. Ele sabia que o projeto seria arriscado, pois aquele estudo tinha muitos perigos, mutações inesperadas eram possíveis e, por esse motivo, já tinha se precavido e desenvolvido uma possível cura, caso as coisas saissem do controle. Mas o que ele não sabia, é que as coisas já haviam saído do controle. O seu gás tóxico, capaz de mudar um ser vivo, foi despejado à noite, ele tentou conter, mas já era tarde demais, o caos já havia sido instaurado, a mutação se espalhou, por humanos, por cachorros e até por pombos. O Dr. M tentou usar sua cura, mas não conseguiu, seu cerébro já havia sido consumido, não tinha mais capacidade de agir por si, e ele mesmo virou parte do caos, uma criatura gigante, ele parecia sofrer com a mutação de forma diferente....
    Com o caos que havia se alastrado pela universidade, militares do exército foram chamados, com uma missão, conter a mutação.
<Nome do personagem> e sua equipe foram salvar o que restou, mas se separam quando avistaram aquela situação, então <Nome do perosnagem> que era condecorado, possuia muitas habilidades com seu rifle e tinha experiência em combate, acreditava que estaria bem, mas ele não tinha noção do que realmente o esperava.
    Aquilo que deveria ser uma operação de contensão, acabou se tornando uma luta pela sobrevivência, e uma busca pela verdade do que 
aconteceu de fato naquela noite.

### Inimigos
* Zumbi - inimigo básico
* Cientista zumbi - inimigo final que lança livros
* Cachorro fantasma - inimigo imortal
* Pombo tóxico - inimigo aéreo que lança pedras

### Coletáveis
* Tapioca (aumenta vida)
* Munição (aumenta estoque para tiro)
* Fusível (missão principal)
* Remédio (missão principal - cura)
* Moedas (comprar alguma coisa)

### Cenário
#### Estruturas 
* NC2A 
* NUPEINSC
* Blocos G e R e outros genéricos
* Reitoria
* Carrinho do Billy 
* RU 
* Biblioteca central 
* Prédio da Medicina - existe uma cura??

#### Background
* Lua 
* Árvores 
* Nuvens 
* Paredes

# Mecânicas 
* Pulo 
* Corrida
* Tiro
* Ataque corpo a corpo

# Dificuldades
* Fácil - Dano de inimigo = 10
* Médio -  Dano de inimigo = 20
* Difícil - Dano de inimigo = 40

# Tutorial -> Como compilar e executar 

# Link para video de execução do programa
 [clique aqui](link)

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
│   ├── algoritmos.py  (algoritmos de renderização e rasterização)
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