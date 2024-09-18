# BOYUTLAR
WIDTH = 612   # OYUN YÜZEY GENİŞLİĞİ
HEIGHT = 612  # OYUN YÜZEY BOYU
ROWS = 17
SQUARE_SIZE = WIDTH // ROWS #tahta boyu
GAP_SIZE = 2  # Bitişik kareler arası boşluk

# RENKLER
SURFACE_CLR = (15, 15, 15)
GRID_CLR = (20, 20, 20)
SNAKE_CLR = (50, 255, 50)
YEM_RENK = (255, 255, 0)
BAS_RENK = (0, 150, 0)
SANAL_YILAN_RENK = (255, 0, 0)

# OYUN AYARLARI
FPS = 30  
ILK_YILAN_UZUNLUK = 3
KAZANIP_BEKLEME = 15  
YEMEKSIZ_HAREKET = ROWS * ROWS * ROWS * 2  
SNAKE_MAX_LENGTH = ROWS * ROWS - ILK_YILAN_UZUNLUK  

# BFS ALGORİTMASINDA KULLANILAM DEĞİŞKENLER
GRID = [[i, j] for i in range(ROWS) for j in range(ROWS)] #IZGARAYI OLUŞTURUR


# Yardımcı fonksiyonlar
def get_neighbors(position):
    neighbors = [[position[0] + 1, position[1]],
                 [position[0] - 1, position[1]],
                 [position[0], position[1] + 1],
                 [position[0], position[1] - 1]]
    in_grid_neighbors = []
    for pos in neighbors:
        if pos in GRID:
            in_grid_neighbors.append(pos)
    return in_grid_neighbors


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]
    return abs(x2 - x1) + abs(y2 - y1)


# Konum demeti
ADJACENCY_DICT = {tuple(pos): get_neighbors(pos) for pos in GRID}
