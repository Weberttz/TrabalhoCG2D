import os

def transformar_txt_csv(arquivo):
    caracteres = {"<": "0", 
                  ">": "0",
                  "X": "1", 
                  "Q": "0", 
                  "?": "4", 
                  "S": "1", 
                  "E": "0", 
                  "-": "0", 
                  "[": "2", 
                  "]": "0",
                  "o": "7",
                  "P": "0",
                  "x": "0",
                  "B": "2",
                  "b": "3"
                }
    
    mapa = []
    with open(arquivo, "r") as f:
        for linha in f:                      
            mapa.append(linha.rstrip('\n'))  # guarda a linha sem o \n

    nome, extensao = os.path.splitext(arquivo)

    with open(f"{nome}.csv", "w") as f2:
        for linha in mapa:
            f2.write(",".join(str(caracteres[c]) for c in linha) + "\n")

if __name__ == "__main__":
    transformar_txt_csv("Mapas/txts/fase1.txt")