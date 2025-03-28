#!/usr/bin/python

""" Conjunt utilitats grafiques per msx , programat per Jordi Sala Clara
les opcions son: 
utils.py nom.tga x y mode tipus color_fondo

nom.tga --> arxiu per volcar
x y --> numero sprites per volcar, 
        exemple 5 2   ---> 5*2=10 total 10 sprites
mode            (8x8,16x16)  ---> byte  8*8   , word  16*16, sprite 16*16 multicolor(2 planols)
tipus             (car,spr) ---> minuscules
color_fondo   (0..15)

exemple: 
utils.py tiles.tga 16 4 16x16 car
utils.py jack.tga 16 2 16x16 spr 1
"""



#Import Modules
import os, pygame,sys
from pygame.locals import *
from sys import argv


if not pygame.font: print 'Warning, fonts disabled'



#extreure multiple color char
def extreure_mcc(px,py,salta):
   
    quadre=[128,64,32,16,8,4,2,1]
    pos=(int(px),int(py))
    fondo=screen.get_at(pos)
    # print "fondo",fondo 

    #fondo de color negre per defecte

    #fondo=color_msx[1]
    color=fondo
    data=0
    for i in range(8):
        b=screen.get_at(pos)
        if b<>fondo:
            data+=quadre[i]
            color=b
        px+=salta
        pos=(int(px),int(py))
    return data,color,fondo
    
def extreure_16char(anteriorx,anteriory,salta):
   
    vector_forma=[]
    vector_color=[]
    px=anteriorx
    py=anteriory
    for i in range(2):
        for j in range(16):
            db=extreure_mcc(px,py,salta)
            py+=salta
            forma=db[0]
            for m in range(16):
                
                if m==15: 
                    
                   #print "error-->",db[1] 
                   break
                if db[1]==color_msx[m]: break
            for n in range(16):
                if n==15: 
                   #print "error-->",db[2] 
                   break
                if db[2]==color_msx[n]: break
            color_char=(m*16)+n
                
          
            vector_forma.append(forma)
            vector_color.append(color_char)
            
        px+=8*salta
        py=anteriory
    return vector_forma,vector_color

def extreure_8char(anteriorx,anteriory,salta):
  
    vector_forma=[]
    vector_color=[]
    px=anteriorx
    py=anteriory
    for j in range(8):
            db=extreure_mcc(px,py,salta)
            py+=salta
            forma=db[0]
            for m in range(16):
                if m==15: 
                    
                   print "error-->",db[1] 
                   break
                if db[1]==color_msx[m]: break
            for n in range(16):
                if n==15: 
                   print "error-->",db[2] 
                   break
                if db[2]==color_msx[n]: break
            color_char=(m*16)+n

            vector_forma.append(forma)
            vector_color.append(color_char)
        
    return vector_forma,vector_color
    
#extreure multiple color sprite de una linia de 8 pixels
def extreure_mcs(px,py,salta,fondo,color1):
    quadre=[128,64,32,16,8,4,2,1]
    pos=(int(px),int(py))
    color2=16
    data1=0
    data2=0
    for i in range(8):
        pixel_llegit=screen.get_at(pos)
        if pixel_llegit<>fondo: """ descobreix pixel de dibuix """
        	
            if color1==16: color1=pixel_llegit
            if pixel_llegit<>color1: color2=pixel_llegit """esbrinem color 2 de l'sprite"""
            if pixel_llegit==color1: data1+=quadre[i]   """contem binari color1 """
            else: data2+=quadre[i] """contem binari color2"""
        px+=salta
        pos=(int(px),int(py))
    return data1,data2,color1,color2
    
    
def extreure_spr(anteriorx,anteriory,salta,color_fondo):
    px=anteriorx
    py=anteriory
    color1=16
    color2=color_fondo
    vector_forma1=[]
    vector_forma2=[]
    for i in range(2):
        for j in range(16):
            db=extreure_mcs(px,py,salta,color_fondo,color1)
            if db[2]<>16: color1=db[2]
            if db[3]<>16: color2=db[3]
            py+=salta
            forma1=db[0]
            forma2=db[1]
            
            vector_forma1.append(forma1)
            vector_forma2.append(forma2) 
        px+=8*salta
        py=anteriory
    return vector_forma1,vector_forma2,color1,color2
    
    

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert()

def extreu_tot_char(posx,posy,salta,x,y,longitud):
    colors=[]
    datas=[]
    anteriorx=posx
    for i in range(y):
        for j in range(x):
            if longitud==16:
                d=extreure_16char(posx,posy,salta)
                #print "char 16x16"
            else:
                #print "char 8x8"
                d=extreure_8char(posx,posy,salta) 
            
                 
            
            #screen.set_at((posx,posy),colorblanc)
            posx+=longitud*salta
            datas.append(d[0])
            colors.append(d[1])
        posy+=longitud*salta
        posx=anteriorx
    return datas,colors
    
def extreu_tot_spr(posx,posy,salta,x,y,longitud,color_fondo):
    colors1=[]
    colors2=[]
    datas1=[]
    datas2=[]
    anteriorx=posx
    for i in range(y):
        for j in range(x):
            if longitud==16:
                print i,j,"sprite 16x16"
                d=extreure_spr(posx,posy,salta,color_fondo)
            else:
                print "sprite 8x8 no definet functions"
                pass
            
            #screen.set_at((posx,posy),colorblanc)
            posx+=longitud*salta
            datas1.append(d[0])
            datas2.append(d[1])
            colors1.append(d[2])
            colors2.append(d[3])
        posy+=longitud*salta
        posx=anteriorx
    return datas1,datas2,colors1,colors2
    
def main():
#Initialize Everything
    global color_msx  
    color_msx=[(148,156,148,255),
    (0,0,0,255),      (40,220,20,255), (112,252,112,255),
    (40,40,248,255),  (80,116,248,255),(184,40,40,255),
    (80,220,248,255), (248,40,40,255), (248,116,112,255),(216,220,40,255),
    (216,220,152,255),(40,152,40,255), (216,80,184,255),
    (184,184,184,255),(248,252,248,255)] #rgb pygame
	

    args=int(len(argv))
    mida='16x16'
    tipus='car'
    longitud=16
    nombre='tiles.tga'
    columna=16
    fila=4
    color_fondo=color_msx[1]
    if args==2:
      nombre=argv[1]
    elif args==3:
      nombre=argv[1]
      columna=int(argv[2])
    elif args==4:
      nombre=argv[1]
      columna=int(argv[2])
      fila=int(argv[3])
    elif args==5:
      nombre=argv[1]
      columna=int(argv[2])
      fila=int(argv[3])
      mida=argv[4]
    elif args==6:
      nombre=argv[1]
      columna=int(argv[2])
      fila=int(argv[3])
      mida=argv[4]
      tipus=argv[5]
    elif args==7:
      nombre=argv[1]
      columna=int(argv[2])
      fila=int(argv[3])
      mida=argv[4]
      tipus=argv[5]
      color_fondo=color_msx[int(argv[6])]
      
      
    elif args>7:
      print "Error: Massa arguments"
    
    if mida=='8x8':
        longitud=8
    else:
        longitud=16 
    
    

    pygame.init()
    global screen,colorblanc
    colorblanc=(255,250,250,255)
    
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Entorn Msx')
    pygame.mouse.set_visible(1)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
#tga
    
    zona=load_image(nombre)
    
#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Conversor a Format Msx", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    screen.blit(zona,(5,50))
    pygame.display.flip()
    print "...Programa utils...."
    print "inici..."
           
    if tipus=='car': 
        a=extreu_tot_char(5,50,1,columna,fila,longitud)
        print "datas",
        f=open(nombre+'.dat.asm','w')
        f.write('; Utilitat Extraccio de Datas a Msx\n')
        f.write('; Programat per Jordi Sala Clara\n')
    
        if longitud==8:
            for i in range(fila*columna):
                f.write('\ndb ')
                for n in range(8):
                        valor=a[0][i][n]
                        f.write(str(valor))
                        if n<7:
                                f.write(',')
            f.close()
            print "... ok"
        
            print "colors",
            f=open(nombre+'.col.asm','w')
            f.write('; Utilitat Extraccio de colors a Msx\n')
            f.write('; Programat per Jordi Sala Clara\n')
  
            for i in range(fila*columna):
                f.write('\ndb ')
                for n in range(8):
                        valor=a[1][i][n]
                        f.write(str(valor))
                        if n<7:
                                f.write(',')
            f.close()
            print "...ok"

        else:
            for i in range(fila*columna):
                f.write('\ndb ')
                for n in range(32):
                        valor=a[0][i][n]
                        f.write(str(valor))
                        if n<31:
                                f.write(',')
            f.close()
            print "... ok"
        
            print "colors",
            f=open(nombre+'.col.asm','w')
            f.write('; Utilitat Extraccio de colors a Msx\n')
            f.write('; Programat per Jordi Sala Clara\n')
  
            for i in range(fila*columna):
                   f.write('\ndb ')
                   for n in range(32):
                        valor=a[1][i][n]
                        f.write(str(valor))
                        if n<31:
                                f.write(',')
            f.close()
            print "...ok"    
    else: 
        a=extreu_tot_spr(5,50,1,columna,fila,longitud,color_fondo)
        print "datas1"
        print a[0]
        print "datas2"
        print a[1]
        print "colors1"
        print a[2]
        print "colors2"
        print a[3]
        print "datas",
        f=open(nombre+'.spr.asm','w')
        f.write('; Utilitat Extraccio de TGA a Sprites Msx (2 colors)\n')
        f.write('; Programat per Jordi Sala Clara\n')
    
        if longitud==8:
            print "no implementat save 8x8"
            pass
        else:
            f.write('\n;datas1\n')
    
            for i in range(fila*columna):
                f.write('\ndb ')
                
                for n in range(32):
                        valor=a[0][i][n]
                        f.write(str(valor))
                        if n<31:
                                f.write(',')
         
            f.write('\n;datas2\n')
            for i in range(fila*columna):
                f.write('\ndb ')
                for n in range(32):
                        valor=a[1][i][n]
                        f.write(str(valor))
                        if n<31:
                                f.write(',')
        f.close()
        print "... ok"
        
        print "colors",
        f=open(nombre+'.col.asm','w')
        f.write('; Utilitat Extraccio de colors de Sprites Msx\n')
        f.write('; Programat per Jordi Sala Clara\n')
        
        f.write('\n;colors1\n')
        for i in range(fila*columna):
                f.write('\ndb ')
                valor=a[2][i][0]
                f.write(str(valor))
                if n<31:
                    f.write(',')

        f.write('\n;colors2\n')
        for i in range(fila*columna):
                f.write('\ndb ')
                valor=a[3][i][0]
                f.write(str(valor))
                if n<31:
                    f.write(',')
   
        f.close()
        print "...ok"    
  
   
    
#Main Loop
    while 1:
      

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
  


        pygame.display.flip()
    print"fi..."     




#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
