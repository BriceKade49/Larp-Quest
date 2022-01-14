#tileMapModule - to use, import this module in your code and use the Tilemap class to create an instance.
import pygame
import json

class Tile(object):
    def __init__(self,filename,collides="True"):
        self.filename=filename
        self.image=pygame.image.load(filename)
        self.collides=collides

class Tilemap(object):
    def __init__(self,renderSurface,tileMapWidth=25,tileMapHeight=18,tileWidth=32,tileHeight=32):
        self.renderSurface=renderSurface
        self.tileMapWidth=tileMapWidth
        self.tileMapHeight=tileMapHeight
        self.tileWidth=tileWidth
        self.tileHeight=tileHeight
        self.tileMap=[]
        for i in range(self.tileMapHeight):
            self.tileMap.append(["  "]*self.tileMapWidth)
            
        self.tileMapTextures={} #store the tile instances under a 2-character string name
        self.badTileColor=(255,100,200)
        self.windowX=0
        self.windowY=0
        self.windowWidth=800
        self.windowHeight=600
        self.EnemyDic = {"Skeleton" : 0, "WizBoss" : 0}
        self.PickupDic = {"pAmmo": 0, "sAmmo": 0, "mAmmo": 0, "miniGun": 0, "key": 0, "HP": 0}
    
    def render(self):
        rowTop=self.windowY//self.tileHeight
        if rowTop<0:
            rowTop=0
        rowBottom=rowTop+self.windowHeight//self.tileHeight+2
        if rowBottom>self.tileMapHeight:
            rowBottom=self.tileMapHeight

        colLeft=self.windowX//self.tileWidth
        if colLeft<0:
            colLeft=0
        colRight=colLeft+self.windowWidth//self.tileWidth+2
        if colRight>self.tileMapWidth:
            colRight=self.tileMapWidth
            
        for row in range(int(rowTop),int(rowBottom)):
            for col in range(int(colLeft),int(colRight)):
                if self.tileMap[row][col]!="  ":
                    cellString=self.tileMap[row][col]
                    if cellString in self.tileMapTextures:
                        tileX_world=col*self.tileWidth
                        tileY_world=row*self.tileHeight
                        tileX_screen=tileX_world-self.windowX
                        tileY_screen=tileY_world-self.windowY
                        self.renderSurface.blit(self.tileMapTextures[cellString].image,(tileX_screen,tileY_screen))
                    else:
                        tileX_world=col*self.tileWidth
                        tileY_world=row*self.tileHeight
                        tileX_screen=tileX_world-self.windowX
                        tileY_screen=tileY_world-self.windowY
                        pygame.draw.rect(self.renderSurface,self.badTileColor,(tileX_screen,tileY_screen,self.tileWidth,self.tileHeight),0)
    def checkTileMapCollision(self,x,y,width,height):
        #TODO: optimize this later to only check thtileMapTextureFilese parts of the map near the collision rectangle
        collideList=[]
        rowTop=y//self.tileHeight
        if rowTop<0:
            rowTop=0
        rowBottom=rowTop+height//self.tileHeight+2
        if rowBottom>self.tileMapHeight:
            rowBottom=self.tileMapHeight
        colLeft=x//self.tileWidth
        if colLeft<0:
            colLeft=0
        colRight=colLeft+width//self.tileWidth+2
        if colRight>self.tileMapWidth:
            colRight=self.tileMapWidth
        
        for row in range(int(rowTop),int(rowBottom)):
            for col in range(int(colLeft),int(colRight)):
                if self.tileMap[row][col]!="  ":
                    tileId=self.tileMap[row][col]
                    if self.tileMapTextures[tileId].collides=="True":
                        #check to see if this tile collides with the rectangle specified
                        tile_x_min=col*self.tileWidth#ttileMapTextureFileshe left pixel of the tile
                        tile_x_max=tile_x_min+self.tileWidth-1 #one less that the start x of the next tile
                        tile_y_min=row*self.tileHeight#the top pixel of the tile
                        tile_y_max=tile_y_min+self.tileHeight-1  #one less that the start y of the next tile
                        if tile_x_max>x and tile_x_min<x+width:
                            if tile_y_max>y and tile_y_min<y+height:                        
                                collideList.append(tileId)      
        return collideList

    def toString(self):
        outputString=""
        for row in range(0,self.tileMapHeight):
            for col in range(0,self.tileMapWidth):
                outputString+=self.tileMap[row][col]
            outputString+="\n"
        return outputString

    def fromString(self,map_string):
        #create blank tilemap
        self.tileMap=[]
        for i in range(self.tileMapHeight):
            self.tileMap.append(["  "]*self.tileMapWidth)

        #divide string into individual lines
        lines=map_string.split("\n")
        row=0
        for line in lines:
            for col in range(0,self.tileMapWidth):
                self.tileMap[row][col]=line[col*2:col*2+2]
            row+=1

    def fromFile(self,filename):
        print("ran"+filename)
        '''create the tilemap from the file that is specified by the filename.'''
        #read individual lines from file
        fhandle=open("NewRooms\\"+filename+".map","r")
        lines=fhandle.readlines()
        fhandle.close()
        mapstring=""
        for line in lines:
            line=line.strip()
            if line[0]=="#" and line=="":
                continue
            (lhs,rhs)=line.split("=")
            if lhs=="tileMapWidth":
                self.tileMapWidth=int(rhs)
            if lhs=="tileMapHeight":
                self.tileMapHeight=int(rhs)
            if lhs=="tileWidth":
                self.tileWidth=int(rhs)
            if lhs=="tileHeight":
                self.tileHeight=int(rhs)
            if lhs=="badTileColor":
                rhs=rhs.replace(")","")
                rhs=rhs.replace("(","")
                (r,g,b)=rhs.split(",")
                self.badTileColor=(int(r),int(g),int(b))
            if lhs=="EnemyDic":
                self.EnemyDic=json.loads(rhs)
            if lhs=="PickupDic":
                self.PickupDic=json.loads(rhs)
                print(self.PickupDic)
            if lhs=="tileMapLine":
                mapstring+=rhs+"\n"
            if lhs=="textureFile":
                (textureId,filename,collides)=rhs.split(",")
                self.loadTexture(textureId,filename,collides)                     
        if mapstring!="":
            self.fromString(mapstring.strip())
        
    def toFile(self,filename,EnemyList):
        '''save the tilemap into the file that is specified by the filename.'''
        maplines=[]
        for row in range(0,self.tileMapHeight):
            linestring=""
            for col in range(0,self.tileMapWidth):
                linestring+=self.tileMap[row][col]
            maplines.append(linestring)
        
        fhandle=open(filename,"w")
        fhandle.write("tileMapWidth="+str(self.tileMapWidth)+"\n")
        fhandle.write("tileMapHeight="+str(self.tileMapHeight)+"\n")
        fhandle.write("tileWidth="+str(self.tileWidth)+"\n")
        fhandle.write("tileHeight="+str(self.tileHeight)+"\n")
        fhandle.write("badTileColor="+str(self.badTileColor)+"\n")
                
        fhandle.write("EnemyDic="+json.dumps(self.EnemyDic)+"\n")
        fhandle.write("PickupDic="+json.dumps(self.PickupDic)+"\n")
                      
        for line in maplines:
            fhandle.write("tileMapLine="+line+"\n")
        for key in self.tileMapTextures.keys():
            fhandle.write("textureFile="+key+","+self.tileMapTextures[key].filename+","+str(self.tileMapTextures[key].collides)+"\n")
        fhandle.close()

    def loadTexture(self,textureId,textureFilename,collides):
        self.tileMapTextures[textureId]=Tile(textureFilename,collides)
            
