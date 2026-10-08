# Projeto PANDORA

Jogo de plataforma em 2D com estilo visual pixel art, onde o jogador passa por cenário típicos da Uece - Campus Itaperi (divididos em quatro estágios) e enfrenta um grande vilão ao final.

## Funcionalidades
* Set Pixel -> Todo o jogo foi renderizado pixel por pixel
* Primitivas de Rasterização 
    * Linha -> Modelagem dos prédios, botões do menu
    * Círculo -> Modelagem da Lua
    * Elipse -> Modelagem das nuvens
* Preenchimento de Regiões 
    * Flood Fill/Boundary Fill -> Foi usado principalmente no menu, mas também em partes do cenário, como Lua, nuvens e carrinho do Billy
    * Scanline -> Usado no jogo em si (mapas, viewport, cenário)
    * Scanline com gradiente -> Janelas dos prédios do cenário
* Transformações Geométricas 
    * Rotação -> Giro em coletável (moeda)
    * Translação -> Teleport 
    * Escala -> Viewport(minimapa)
* Animação 2D -> Movimentação dos personagens
* Janela e Viewport -> Criação de minimapa 
* Recorte de Cohen-Sutherland (Clipping) -> Usado no minimapa para plataformas que estavam nas bordas da viewport
* Mapeamento de Textura -> Sprites dos personagens e componentes do cenário
* Input (Teclado e/ou Mouse) -> Usado no menu e para movimentar o jogador 

## Lore  
<br>&emsp;&emsp;Um cientista conhecido como Dr. M trabalhava em uma universidade chamada Uece e era muito bom em suas pesquisas. Em um de seus projetos, chamado TPBST (Teleportation breaks through space and time), conseguiu construir um portal que teletransporta pessoas de um lugar para outro instantaneamente. Mas ele não se contentava facilmente, por isso decidiu trabalhar em um projeto mais ousado. O PANDORA (Project for Advanced Natural Development, Organism Reinforcement and Adaptation) visava evoluir todas as características de seres vivos, força, resistência, inteligência, habilidades motoras, etc. Ele sabia que o projeto seria arriscado, pois aquele estudo tinha muitos perigos, mutações inesperadas eram possíveis e, por esse motivo, já tinha se precavido e desenvolvido uma possível cura, caso as coisas saissem do controle. Mas o que ele não sabia, é que as coisas já haviam saído do controle. O seu gás tóxico, capaz de mudar um ser vivo, foi despejado à noite, ele tentou conter, mas já era tarde demais, o caos já havia sido instaurado, a mutação se espalhou, por humanos, por cachorros e até por pombos. O Dr. M tentou usar sua cura, mas não conseguiu, seu cerébro já havia sido consumido, não tinha mais capacidade de agir por si, e ele mesmo virou parte do caos, uma criatura gigante, ele parecia sofrer com a mutação de forma diferente....
<br>&emsp;Com o caos que havia se alastrado pela universidade, militares do exército foram chamados, com uma missão, conter a mutação.
Davi Maia e sua equipe foram salvar o que restou, mas se separam quando avistaram aquela situação, então Sargento Maia que era condecorado, possuia muitas habilidades com seu rifle e tinha experiência em combate, acreditava que estaria bem, mas ele não tinha noção do que realmente o esperava.
<br>&emsp;Aquilo que deveria ser uma operação de contensão, acabou se tornando uma luta pela sobrevivência, e uma busca pela verdade do que 
aconteceu de fato naquele lugar.

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
* Moeda (level design)

### Cenário
#### Estruturas 
* NC2A 
* NUPEINSC
* Blocos G e R e outros genéricos
* Reitoria
* Carrinho do Billy 
* RU 
* Biblioteca central 
* Prédio da Medicina

#### Background
* Lua 
* Árvores 
* Nuvens 
* Paredes

# Mecânicas 
* Pulo : tecla SPACE
* Corrida : teclas RIGHT , LEFT
* Tiro : tecla Z

# Dificuldades
* Fácil - Dano de inimigo = 10
* Médio -  Dano de inimigo = 20
* Difícil - Dano de inimigo = 40

# Tutorial 
## Como executar o jogo
* Clone o repositório
```
git clone 
``` 
* Entre na pasta do projeto
```
cd TrabalhoCG2D
```
* Crie um ambiente virtual
    * Linux/macOS
```
python3 -m venv .venv
source .venv/bin/activate
```
    * Windows (no Command Prompt)
```
python -m venv .venv
.venv\Scripts\activate.bat
```
* Intale as dependências 
```
pip install -r requirements.txt
```
* Executar jogo
```
python jogo.py 
```

## Link para video de execução do programa
 [clique aqui](link)

# Árvore do projeto
```
.
├── arvore.txt
├── Assets
│   ├── parede-pedra-1.png
│   ├── predio-quebrado.png
│   ├── PressStart2P-Regular.ttf
│   ├── tapioca.png
│   ├── tijolos-escuros.png
│   └── uece-noite.png
├── Biblioteca
│   ├── algoritmos.py
│   └── transformacoes.py
├── Classes
│   ├── arma.py
│   ├── cachorro.py
│   ├── camera.py
│   ├── cenario.py
│   ├── chefe.py
│   ├── coletavel.py
│   ├── equipamento.py
│   ├── humanoide.py
│   ├── jogador.py
│   ├── plataforma.py
│   ├── pombo.py
│   ├── projetil.py
│   ├── retangulo.py
│   ├── vetor.py
│   └── zumbi.py
├── converter.py
├── Docs
│   ├── jogo.gdd
│   ├── lore.txt
│   ├── nc2a.png
│   └── reitoria.png
├── Fontes
│   └── FreePixel.ttf
├── Gerenciador
│   ├── Atualizador.py
│   ├── GerenciadorFases.py
│   ├── Inicializador.py
│   └── Renderizador.py
├── jogo.py
├── Mapas
│   ├── estagio11.csv
│   ├── estagio12.csv
│   ├── estagio13.csv
│   ├── estagio14.csv
│   ├── fase1.csv
│   ├── fase2.csv
│   └── fase3.csv
├── menu.py
├── README.md
├── settings.py
├── Sons
│   └── suspense_sobrenatural_loop.wav
├── Sprites
│   ├── antigos
│   │   ├── soldado_hurt_idle_left.png
│   │   ├── soldado_hurt_idle_right.png
│   │   ├── soldado_hurt_jump_left.png
│   │   ├── soldado_hurt_jump_right.png
│   │   ├── soldado_hurt_walk_left.png
│   │   ├── soldado_hurt_walk_right.png
│   │   ├── zumbi_idle_0.png
│   │   ├── zumbi_idle_1.png
│   │   ├── zumbi_idle_2.png
│   │   ├── zumbi_idle_3.png
│   │   ├── zumbi_idle_4.png
│   │   ├── zumbi_idle_5.png
│   │   ├── zumbi_idle_6.png
│   │   ├── zumbi_idle_7.png
│   │   ├── zumbi_walk_left_0.png
│   │   ├── zumbi_walk_left_1.png
│   │   ├── zumbi_walk_left_2.png
│   │   ├── zumbi_walk_left_3.png
│   │   ├── zumbi_walk_left_4.png
│   │   ├── zumbi_walk_left_5.png
│   │   ├── zumbi_walk_left_6.png
│   │   ├── zumbi_walk_left_7.png
│   │   ├── zumbi_walk_right_0.png
│   │   ├── zumbi_walk_right_1.png
│   │   ├── zumbi_walk_right_2.png
│   │   ├── zumbi_walk_right_3.png
│   │   ├── zumbi_walk_right_4.png
│   │   ├── zumbi_walk_right_5.png
│   │   ├── zumbi_walk_right_6.png
│   │   └── zumbi_walk_right_7.png
│   ├── cientista_idle_0.png
│   ├── dog_idle_0.png
│   ├── dog_idle_1.png
│   ├── dog_idle_2.png
│   ├── dog_idle_3.png
│   ├── dog_idle_4.png
│   ├── dog_walk_left_0.png
│   ├── dog_walk_left_1.png
│   ├── dog_walk_left_2.png
│   ├── dog_walk_left_3.png
│   ├── dog_walk_left_4.png
│   ├── dog_walk_left_5.png
│   ├── dog_walk_left_6.png
│   ├── dog_walk_left_7.png
│   ├── dog_walk_right_0.png
│   ├── dog_walk_right_1.png
│   ├── dog_walk_right_2.png
│   ├── dog_walk_right_3.png
│   ├── dog_walk_right_4.png
│   ├── dog_walk_right_5.png
│   ├── dog_walk_right_6.png
│   ├── dog_walk_right_7.png
│   ├── fusivel.png
│   ├── moeda.png
│   ├── municao.png
│   ├── novos
│   │   ├── drm_50x50_sprites
│   │   │   ├── drm_attack_left_0.png
│   │   │   ├── drm_attack_left_1.png
│   │   │   ├── drm_attack_left_2.png
│   │   │   ├── drm_attack_left_3.png
│   │   │   ├── drm_attack_left_4.png
│   │   │   ├── drm_attack_left_5.png
│   │   │   ├── drm_attack_right_0.png
│   │   │   ├── drm_attack_right_1.png
│   │   │   ├── drm_attack_right_2.png
│   │   │   ├── drm_attack_right_3.png
│   │   │   ├── drm_attack_right_4.png
│   │   │   ├── drm_attack_right_5.png
│   │   │   ├── drm_idle_0.png
│   │   │   ├── drm_idle_1.png
│   │   │   ├── drm_idle_2.png
│   │   │   ├── drm_idle_3.png
│   │   │   ├── drm_walk_left_0.png
│   │   │   ├── drm_walk_left_1.png
│   │   │   ├── drm_walk_left_2.png
│   │   │   ├── drm_walk_left_3.png
│   │   │   ├── drm_walk_left_4.png
│   │   │   ├── drm_walk_left_5.png
│   │   │   ├── drm_walk_right_0.png
│   │   │   ├── drm_walk_right_1.png
│   │   │   ├── drm_walk_right_2.png
│   │   │   ├── drm_walk_right_3.png
│   │   │   ├── drm_walk_right_4.png
│   │   │   └── drm_walk_right_5.png
│   │   └── zumbi_50x50_sprites
│   ├── pombo_fly_left_0.png
│   ├── pombo_fly_left_1.png
│   ├── pombo_fly_left_2.png
│   ├── pombo_fly_left_3.png
│   ├── pombo_fly_right_0.png
│   ├── pombo_fly_right_1.png
│   ├── pombo_fly_right_2.png
│   ├── pombo_fly_right_3.png
│   ├── seringa.png
│   ├── soldado_idle_left_0.png
│   ├── soldado_idle_left_1.png
│   ├── soldado_idle_left_2.png
│   ├── soldado_idle_left_3.png
│   ├── soldado_idle_right_0.png
│   ├── soldado_idle_right_1.png
│   ├── soldado_idle_right_2.png
│   ├── soldado_idle_right_3.png
│   ├── soldado_jump_left_0.png
│   ├── soldado_jump_left_1.png
│   ├── soldado_jump_left_2.png
│   ├── soldado_jump_right_0.png
│   ├── soldado_jump_right_1.png
│   ├── soldado_jump_right_2.png
│   ├── soldado_to_look_up_0.png
│   ├── soldado_to_look_up_1.png
│   ├── soldado_to_look_up_2.png
│   ├── soldado_to_look_up_3.png
│   ├── soldado_walk_left_0.png
│   ├── soldado_walk_left_1.png
│   ├── soldado_walk_left_2.png
│   ├── soldado_walk_left_3.png
│   ├── soldado_walk_left_4.png
│   ├── soldado_walk_right_0.png
│   ├── soldado_walk_right_1.png
│   ├── soldado_walk_right_2.png
│   ├── soldado_walk_right_3.png
│   ├── soldado_walk_right_4.png
│   ├── tapioca.png
│   ├── zumbi_idle_left_0.png
│   ├── zumbi_idle_left_1.png
│   ├── zumbi_idle_left_2.png
│   ├── zumbi_idle_left_3.png
│   ├── zumbi_idle_right_0.png
│   ├── zumbi_idle_right_1.png
│   ├── zumbi_idle_right_2.png
│   ├── zumbi_idle_right_3.png
│   ├── zumbi_walk_left_0.png
│   ├── zumbi_walk_left_1.png
│   ├── zumbi_walk_left_2.png
│   ├── zumbi_walk_left_3.png
│   ├── zumbi_walk_left_4.png
│   ├── zumbi_walk_left_5.png
│   ├── zumbi_walk_right_0.png
│   ├── zumbi_walk_right_1.png
│   ├── zumbi_walk_right_2.png
│   ├── zumbi_walk_right_3.png
│   ├── zumbi_walk_right_4.png
│   └── zumbi_walk_right_5.png
└── teste_som.py
```
