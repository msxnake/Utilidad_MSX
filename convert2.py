#!/usr/bin/python

#Programa per traspassar 
#levels a msx
#fet per Jordi Sala
#modificat per comprimir, v90914

#Import Modules
import struct
import os, pygame,sys
from pygame.locals import *
from sys import argv


# feina per fer ... convertir valors a un simpre vector

def convert_level(fname):
    img = pygame.image.load(fname)
    w,h = img.get_width(),img.get_height()
    

  
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
  
   
	
    return forma2,w,h
    
def save_level(nombre,forma):
    f=open(nombre+'.lev.bin','wb')
    pos=0
    print forma
    for i in range(len(forma)):
		#----------------------f.write(forma[pos])
		#data = struct.pack('i', forma[pos])
		data = forma[pos]
		f.write(chr(data))
		pos+=1
			
    f.close()
    return
 
    
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
    
    print"saving...",
    save_level(nombre,forma1)
   
    print "...ok"
    print "End"
    #print w,h,forma1


#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
  
