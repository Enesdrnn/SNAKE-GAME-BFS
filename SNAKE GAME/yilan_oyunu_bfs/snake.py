import pygame
from settings import *
from copy import deepcopy
from random import randrange


class Square:
    def __init__(self, pozisyon, yuzey, yem=False):
        self.pozisyon = pozisyon # karenin pozisyonunu(kordinatını belirlemek için atanan bir değişken)
        self.yuzey = yuzey  # karenin ekleneceği yüzeyi belirlemek için kullanılır(oyun ekranının yüzeyi)
        self.yem = yem #karenin yem olup olmadığını belirten bir değişkendir
        self.kuyruk = False #Bu, karenin yılanın kuyruğunun bir parçası olup olmadığını belirten bir değişkendir .
        self.yon = [-1, 0]  # [x, y] yon baslangicta [-1, 0] degerini alır -1 değeri, karenin yatay eksende sola hareket ettiğini, 0 değeri ise dikey eksende hareket etmediğini gösterir.

        if self.yem:
            self.yon = [0, 0] #  eğer kare bir yem ise  yemdeki karenin hareket etmeyeceğini belirtir.

    def draw(self, renk=SNAKE_CLR): #SNAKE_CLR Kareyi çizerken kullanılacak renk değerini belirten bir parametre.
        x, y = self.pozisyon[0], self.pozisyon[1] #karenin yerleştirileceği kordinatları temsil eder
        ss, gs = SQUARE_SIZE, GAP_SIZE #Kare'nin boyutlarını ve boşluk miktarını temsil eden SQUARE_SIZE ve GAP_SIZE değerlerini ss ve gs değişkenlerine atar. Bu değerler, kareyi çizmek için kullanılır.

        if self.yon == [-1, 0]: #eğer karenin hareket yönü sola ise çalışır
            if self.kuyruk: #true ise aşağıdaki işlem gerçekleşir
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs)) #koordinatlarında bir dikdörtgen çizilir. Bu, karenin sol tarafına bir dikdörtgen çizilmesini sağlar.
            else: #false ise aşağıdaki işlem gerçekleşir 
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss, ss - 2*gs)) #koordinatlarında bir dikdörtgen çizilir. Bu, karenin sol tarafına ve karenin tam boyutuna sahip bir dikdörtgen çizilmesini sağlar.

        if self.yon == [1, 0]: #Eğer karenin hareket yönü sağa eşitse
            if self.kuyruk: #true ise aşağıdaki işlem gerçekleşir
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs)) #koordinatlarında bir dikdörtgen çizilir. Bu, karenin sağ tarafına bir dikdörtgen çizilmesini sağlar.
            else: #değil ise aşağıdaki işlem gerçekleşir
                pygame.draw.rect(self.yuzey, renk, (x * ss - gs, y * ss + gs, ss, ss - 2*gs)) #koordinatlarında bir dikdörtgen çizilir. Bu, karenin sağ tarafına ve karenin tam boyutuna sahip bir dikdörtgen çizilmesini sağlar.

        if self.yon == [0, 1]: # Eğer karenin hareket yönü yukarıya eşitse, aşağıdaki işlemler gerçekleştirilir:
            if self.kuyruk:
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss - gs, ss - 2*gs, ss))

        if self.yon == [0, -1]: #Eğer karenin hareket yönü aşağıysa aşağıdaki işlemleri gerçekleştirir
            if self.kuyruk:
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss))

        if self.yem:
            pygame.draw.rect(self.yuzey, renk, (x * ss + gs, y * ss + gs, ss - 2*gs, ss - 2*gs))

    def hamle(self, yon): #yılanın hareket etmesini sağlayan fonksiyon
        self.yon = yon #yılanın bir sonraki adımda hangi yöne hareket edeceğini belirler.
        self.pozisyon[0] += self.yon[0] #pozisyon listesinin x ve y koordinatları, hareket yönüne göre güncellenir.
        self.pozisyon[1] += self.yon[1]

    def hitting_wall(self): #yılanın duvara çarpıp çarpmadığını kontrol eden fonksiyon
        if (self.pozisyon[0] <= -1) or (self.pozisyon[0] >= ROWS) or (self.pozisyon[1] <= -1) or (self.pozisyon[1] >= ROWS):
            return True # yılan duvara çarptıysa, true değeri döndürülür.
        else:
            return False # yılan duvara çarpmadıysa, false değeri döndürülür.


class Snake:
    def __init__(self, yuzey): 
        self.yuzey = yuzey
        self.olum = False
        self.baslangicpozisyonu = [[ROWS // 2 + i, ROWS // 2] for i in range(ILK_YILAN_UZUNLUK)]
        self.donusler = {}
        self.yon = [-1, 0]
        self.skor = 0
        self.yemsizhareket = 0
        self.yemm = Square([randrange(ROWS), randrange(ROWS)], self.yuzey, yem=True)

        self.tahtalar = []
        for pozisyon in self.baslangicpozisyonu:
            self.tahtalar.append(Square(pozisyon, self.yuzey))

        self.bas = self.tahtalar[0]
        self.kuyruk = self.tahtalar[-1]
        self.kuyruk.kuyruk = True

        self.yol = []
        self.sanalyilan = False
        self.top_hamle = 0
        self.kazanilan_oyun = False

    def draw(self):
        self.yemm.draw(YEM_RENK) #yemin görsel olarak ekrana çizilmesini sağlar.
        self.bas.draw(BAS_RENK) #Yılanın baş karesini BAS_RENK renk değeriyle çizmeye yarar.
        for sqr in self.tahtalar[1:]:
            if self.sanalyilan: 
                sqr.draw(SANAL_YILAN_RENK)
            else:
                sqr.draw()

    def set_yon(self, yon):
        if yon == 'sol':
            if not self.yon == [1, 0]:
                self.yon = [-1, 0]
                self.donusler[self.bas.pozisyon[0], self.bas.pozisyon[1]] = self.yon
        if yon == "sag":
            if not self.yon == [-1, 0]:
                self.yon = [1, 0]
                self.donusler[self.bas.pozisyon[0], self.bas.pozisyon[1]] = self.yon
        if yon == "yukari":
            if not self.yon == [0, 1]:
                self.yon = [0, -1]
                self.donusler[self.bas.pozisyon[0], self.bas.pozisyon[1]] = self.yon
        if yon == "asagi":
            if not self.yon == [0, -1]:
                self.yon = [0, 1]
                self.donusler[self.bas.pozisyon[0], self.bas.pozisyon[1]] = self.yon

    def olaylar(self):
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()

            # klavye yönleriyle yılan yönü ayarı
            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.set_yon('sol')

                elif keys[pygame.K_RIGHT]:
                    self.set_yon('sag')

                elif keys[pygame.K_UP]:
                    self.set_yon('yukari')

                elif keys[pygame.K_DOWN]:
                    self.set_yon('asagi')

    def hamle(self):
        for j, sqr in enumerate(self.tahtalar):
            p = (sqr.pozisyon[0], sqr.pozisyon[1])
            if p in self.donusler:
                turn = self.donusler[p]
                sqr.hamle([turn[0], turn[1]])
                if j == len(self.tahtalar) - 1:
                    self.donusler.pop(p)
            else:
                sqr.hamle(sqr.yon)
        self.yemsizhareket += 1

    def kare_ekle(self):
        self.tahtalar[-1].kuyruk = False
        kuyruk = self.tahtalar[-1]  # Yeni kare eklemeden önce kuyruk

        yon = kuyruk.yon
        if yon == [1, 0]:
            self.tahtalar.append(Square([kuyruk.pozisyon[0] - 1, kuyruk.pozisyon[1]], self.yuzey))
        if yon == [-1, 0]:
            self.tahtalar.append(Square([kuyruk.pozisyon[0] + 1, kuyruk.pozisyon[1]], self.yuzey))
        if yon == [0, 1]:
            self.tahtalar.append(Square([kuyruk.pozisyon[0], kuyruk.pozisyon[1] - 1], self.yuzey))
        if yon == [0, -1]:
            self.tahtalar.append(Square([kuyruk.pozisyon[0], kuyruk.pozisyon[1] + 1], self.yuzey))

        self.tahtalar[-1].yon = yon
        self.tahtalar[-1].kuyruk = True  # Yeni kare ekledikten sonra kuyruk

    def reset(self):
        self.__init__(self.yuzey)

    def kendine_carp(self):  # yilanin kendine çarpması durumunda ki çalışacak fonsksiyon
        for sqr in self.tahtalar[1:]:
            if sqr.pozisyon == self.bas.pozisyon:
                return True

    def yem_uret(self): #yeni bir yem  oluşturmak için kullanılır.
        self.yemm = Square([randrange(ROWS), randrange(ROWS)], self.yuzey, yem=True)#yeni yem nesnesi oluşturur.
        if not self.pozisyon_serbest(self.yemm.pozisyon):# oluşturulan yem tahtanın veya yılanın üstüne geliyor ise rastgele yeni yem pozisyonu oluşturur 
            self.yem_uret() #Yem pozisyonunu tekrar rastgele seçer çakışmayana kadar yapar bunu

    def yem_yemek(self): #yılanın yemi yemesini kontrol eder
        if self.bas.pozisyon == self.yemm.pozisyon and not self.sanalyilan and not self.kazanilan_oyun:
            self.yem_uret()
            self.yemsizhareket = 0
            self.skor += 1
            return True

    def gotur(self, position):  # yılanın baş kısmının hedef yöne yönelmesini sağlamak için kullanılacak bir fonksiyondur.
        if self.bas.pozisyon[0] - 1 == position[0]:
            self.set_yon('sol')
        if self.bas.pozisyon[0] + 1 == position[0]:
            self.set_yon('sag')
        if self.bas.pozisyon[1] - 1 == position[1]:
            self.set_yon('yukari')
        if self.bas.pozisyon[1] + 1 == position[1]:
            self.set_yon('asagi')

    def pozisyon_serbest(self, position): #yılanın ve duvarların içinde olup olmadığını kontrol eder.
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.tahtalar:
            if sqr.pozisyon == position:
                return False
        return True

    # Breadth First Search (BFS) ALGORİTMASI
    def bfs(self, s, e):  #başlangıc pozisyonuyla bitiş pozisyonu arasındaki en kısa yolu bul
        q = [s]  # Kuyruk
        ziyaret = {tuple(pos): False for pos in GRID} #her konumun ziyaret edilip edilmediğini tutar. 

        ziyaret[s] = True #Başlangıçta tüm konumlar ziyaret edilmemiş olarak işaretlenir.

        # "prev" terimi, yol bulma algoritmalarında her düğümün ebeveyn düğümünü temsil eder
        prev = {tuple(pos): None for pos in GRID} #her konumun bir önceki konumunu tutar.

        while q:  # Kuyruk boş değilken
            node = q.pop(0) #Kuyruğun başından bir düğüm alır ve node değişkenine atar.
            neighbors = ADJACENCY_DICT[node] #node düğümünün komşularını alır
            for next_node in neighbors: #Komşu düğümler üzerinde döngü oluşturulur.
                if self.pozisyon_serbest(next_node) and not ziyaret[tuple(next_node)]: #Eğer komşu düğüm boştaysa ve daha önce ziyaret edilmemişse
                    q.append(tuple(next_node))#Komşu düğümü kuyruğa ekleriz.
                    ziyaret[tuple(next_node)] = True #Komşu düğümü ziyaret edildi olarak işaretleriz.
                    prev[tuple(next_node)] = node #Komşu düğümün önceki düğümünü kayıt ederiz.

        yol = list() #en kısa yolun düğümlerini tutacak.
        p_node = e  # her düğümün ebeveyn düğümünü bulmak için kullanırız.

        node_ara = False #Başlangıç düğümü bulunana kadar false olarak kalır
        while not node_ara: #Bu döngü, hedef noktasından başlayarak her düğümün ebeveyn düğümünü bulmak için kullanılır baslangıc düğümünü bulana kadar devam eder
            if prev[p_node] is None: #düğümünün önceki düğümü yoksa yol bulunamadı
                return [] #Boş bir liste döndürür
            p_node = prev[p_node] #düğümünün önceki düğümünü alarak geriye doğru ilerler.
            if p_node == s: #başlangıç noktasına eşitse  yolu tamamlanmıştır
                yol.append(e) #Hedef noktasını yol listesine ekleriz.
                return yol  #Bulunan yolun listesini döndürerek en kısa yolun tamamlandığını ifade eder.
            yol.insert(0, p_node) #ardışık düğümleri takip ederek en kısa yolun oluşturulmasını sağlar. çünkü p_node düğümünü yol listesinin başına ekleriz.

        return []  # yol bulunamadı boş liste döndü

    def kopyala_yilan(self):  # yılanın bir kopyasını oluşturur
        v_yilan = Snake(self.yuzey)
        for i in range(len(self.tahtalar) - len(v_yilan.tahtalar)):
            v_yilan.kare_ekle()

        for i, sqr in enumerate(v_yilan.tahtalar):
            sqr.pozisyon = deepcopy(self.tahtalar[i].pozisyon)
            sqr.yon = deepcopy(self.tahtalar[i].yon)

        v_yilan.yon = deepcopy(self.yon)
        v_yilan.donusler = deepcopy(self.donusler)
        v_yilan.yemm.pozisyon = deepcopy(self.yemm.pozisyon)
        v_yilan.yemm.yem = True
        v_yilan.sanalyilan = True

        return v_yilan

    def baskuyruk_yol(self): #  yılanın başından kuyruğa olan yolunun bir listesini bulmak için kullanılır.
        kuyruk_poz = deepcopy(self.tahtalar[-1].pozisyon)#kuyruk pozisyonunu kopyalar yılanın son karesini kuyruktan çıkartır
        self.tahtalar.pop(-1)
        yol = self.bfs(tuple(self.bas.pozisyon), tuple(kuyruk_poz))#başlangıç ve hedef pozisyonları arasındaki en kısa yolun bir listesini bulur.
        self.kare_ekle()
        return yol

    def neighbors_poz(self, pozisyon):
        gecerli_neighbors = []
        neighbors = get_neighbors(tuple(pozisyon))
        for n in neighbors:
            if self.pozisyon_serbest(n) and self.yemm.pozisyon != n: #komşu pozisyonun boş olup olmadığını kontrol eder ve yemle aynı pozisyonda olmadığını doğrular bu yılanın yem ve kendi kuyruğuyla aynı pozisyonda olmasından kaçınmasını sağlar.
                gecerli_neighbors.append(tuple(n))#Geçerli ve uygun olan komşu pozisyonları ekler
        return gecerli_neighbors

    def uzun_yol_kuyruk(self):#yılanın başından kuyruğuna olan en uzun yolun bulunmasını sağlar.
        neighbors = self.neighbors_poz(self.bas.pozisyon)
        yol = []
        if neighbors:
            dis = -9999
            for n in neighbors:
                if distance(n, self.tahtalar[-1].pozisyon) > dis:
                    v_yilan = self.kopyala_yilan()
                    v_yilan.gotur(n)
                    v_yilan.hamle()
                    if v_yilan.yem_yemek():
                        v_yilan.kare_ekle()
                    if v_yilan.baskuyruk_yol():
                        yol.append(n)
                        dis = distance(n, self.tahtalar[-1].pozisyon)
            if yol:
                return [yol[-1]]

    def guvenli_hamle(self): #yılanın güvenli bir hamle yapmasını sağlar.
        neighbors = self.neighbors_poz(self.bas.pozisyon)
        yol = []
        if neighbors:
            yol.append(neighbors[randrange(len(neighbors))])#rastgele komşu pozisyon seçilir ve yol değişkenine eklenir.
            v_yilan = self.kopyala_yilan()# mevcut yılanın kopyasını oluşturur
            for hamle in yol:
                v_yilan.gotur(hamle)#yilan hareket ettirilir
                v_yilan.hamle()
            if v_yilan.baskuyruk_yol():
                return yol #kuyruğa giden yol bulunduysa yol döndürülür
            else:
                return self.baskuyruk_yol() #bulunmadıysa yılanın kuyruğa olan yolun bulunmasını sağlar ve döndürülür.

    def set_yol(self):
        #yılanın kazanmak için son bir elma kaldığında ve bu elmanın yılanın başına bitişik olduğunda özel bir durum kontrol edilir.
        if self.skor == SNAKE_MAX_LENGTH - 1 and self.yemm.pozisyon in get_neighbors(self.bas.pozisyon):#yılanın maksimum uzunluğu eksi 1 ve yem pozsiyonu içinde yer alıyorsa yılanın kazanmak üzere olduğu anlaşılır. Bu durumda, sadece elmanın pozisyonunu içeren bir yol oluşturulur
            winning_yol = [tuple(self.yemm.pozisyon)]
            print('Yilan kazanmak üzere...')
            return winning_yol

        v_yilan = self.kopyala_yilan()

        
        yol_1 = v_yilan.bfs(tuple(v_yilan.bas.pozisyon), tuple(v_yilan.yemm.pozisyon))

        #Sanal yılan  yem pozisyonuna giden yolun (yol_1) bulunup bulunmadığını kontrol eder
        yol_2 = []

        if yol_1:
            for pozisyon in yol_1:
                v_yilan.gotur(pozisyon)
                v_yilan.hamle()

            v_yilan.kare_ekle()  
            yol_2 = v_yilan.baskuyruk_yol()

       

        if yol_2:  # sanalyılanla kuyruk arasında bir yol var ise
            return yol_1  # yeme ulaşmak için BFS algoritmasını seçeriz en hızlı ve en kısa yol olarak

        # yol 1 ve yol 2 de musait bir durum yok ise 3 koşul test edilir.
            # 1- Kuyruğa giden en uzun yolun müsait olduğundan emin olmak
            # 2- skor çift ise kuyruğu takip eder tek ise güvenli hamleyi kullanır 
            # 3- yılan bir döngüde sıkışırsa kuyruk takibindeki yöntemi değiştirir.
        if self.uzun_yol_kuyruk() and\
                self.skor % 2 == 0 and\
                self.yemsizhareket < YEMEKSIZ_HAREKET / 2:

            # Kuyruğa en uzak yolu seçer
            return self.uzun_yol_kuyruk()

        # Mümkün olan herhangi bir güvenli hamle oynanır kuyruğa giden yolun musaitliğine bakılarak.
        if self.guvenli_hamle():
            return self.guvenli_hamle()

       #kuyrukta geçerli bir yol var ise
        if self.baskuyruk_yol():
            # Kuyruğa giden en kısa yol
            return self.baskuyruk_yol()

        
        print('Yol yok, yilan tehlikede')

    def update(self):
        self.olaylar()

        self.yol = self.set_yol()
        if self.yol:
            self.gotur(self.yol[0])

        self.draw()
        self.hamle()

        if self.skor == ROWS * ROWS - ILK_YILAN_UZUNLUK:  # Yılan oyunu kazanır ise
            self.kazanilan_oyun = True

            print("Yilan  {} hamleden sonra kazandı"
                  .format(self.top_hamle))

            pygame.time.wait(1000 * KAZANIP_BEKLEME)
            return 1

        self.top_hamle += 1

        if self.kendine_carp() or self.bas.hitting_wall():
            print("Yilan kaybetti tekrar dene...")
            self.olum = True
            self.reset()

        if self.yemsizhareket == YEMEKSIZ_HAREKET:
            self.olum = True
            print("Yilan engele takildi tekrar deniyor..")
            self.reset()

        if self.yem_yemek():
            self.kare_ekle()
