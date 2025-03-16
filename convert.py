#!/usr/bin/python

#Programa per traspassar 
#levels a msx
#fet per Jordi Sala
#modificat per comprimir, v90914

#Import Modules
import os, pygame,sys
from pygame.locals import *
from sys import argv

def convert_level(fname):
    img = pygame.image.load(fname)
    w,h = img.get_width(),img.get_height()
    

    forma=[]
    forma2=[]
    pos=6144
    pos2=0
    xx=0
    yy=0
    for y in range(0,h):
        for x in range(0,w):
            t,b,c,_a = img.get_at((x,y))
            forma2.append(t)
	    
            if c==1:
		    xx=((pos-6144)%32*8)
		    yy=int((pos-6144)/32)*8
		    print "\nFound 1=",pos,", ",pos2," x=",xx," y=",yy
            pos+=2
	    pos2+=2
	print ".",
	pos+=32
	pos2+=32
        forma.append(forma2)
        forma2=[]
	
    return forma,w,h
    
def save_level(nombre,forma):
    f=open(nombre+'.lev.asm','w')
    f.write('; Utilitat Extraccio de Levels a Msx\n')
    f.write('; Programat per Jordi Sala Clara\n')
    
    f.write('; pantalla del '+str(nombre))
    f.write('\ndb ')
    n=0
    pos=0

    for i in range(len(forma)):
            print ".",
            n+=1
            if n>15:
                n=0
                f.write('\ndb ')
            #print "i=",i,"j=",j,"forma=",forma1[i][j],
            f.write(str(forma[pos]))
            if  n<15 and i!=len(forma)-1:
                f.write(',')
            pos+=1
    f.write('\ndb 255\n;---------------------\n')
    f.close()
    return
    
def comprimir_level(forma,x,y):
    forma2=[]
    con=1
    con2=0
    pos=0
    pos2=0
    val=forma[pos][pos2]
    pos2=1
    print x*y,"values:",x," -- ",y 

    while con2<(x*y)-1:
       print ".",
       ant=val
       val=forma[pos][pos2]
       pos2+=1
       if pos2>(x-1):    #319 o 15
	  pos2=0
	  pos+=1
       con2+=1
       if val==ant:
	 if con<126:
	    con+=1
	 else:
	    forma2.append(con+128)
	    con=1
       else:
	 if con>1:
	       forma2.append(con+128)
	       forma2.append(ant)
	       con=1
	 else:
	       forma2.append(ant)
    forma2.append(val)
    return forma2

    
def main():
    print
    print "Programa Convert v1.0"
    print "---------------------"
    print "starting.."
    args=int(len(argv))
    nombre='level1.tga'
    if args==2:
      nombre=argv[1]
    print "converting",
    forma1,w,h=convert_level(nombre)
    print "ok"
    #print forma1
    print "compressing",
    forma2=comprimir_level(forma1,w,h)
    #print forma2
    print "ok"
    
    print"saving...",
    save_level(nombre,forma2)
   
    print "...ok"
    redu=100-((len(forma2)*100)/(w*h))
    print "reduced ",redu,"%"

    print "End"
    #print w,h,forma1


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
  
