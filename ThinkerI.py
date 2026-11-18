import ollama 
import tkinter as tk 
import pyopengltk  
from pyopengltk import OpenGLFrame
import OpenGL.GL as gl
import OpenGL.GLU as glu
import time 
import os
import PIL
from PIL import Image

Textures=[]

os.startfile(r"C:/Users/Andrew Alexander/AppData/Local/Programs/Ollama/ollama.exe",show_cmd=0)

def texload(file): 
        gl.glEnable(gl.GL_TEXTURE_2D)
        texId=gl.glGenTextures(1) 
        image1=Image.open(file) 
        image1.convert("RGBA")
        imgData=image1.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
       
        gl.glBindTexture(gl.GL_TEXTURE_2D,texId)
        gl.glTexParameter(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,gl.GL_LINEAR)
        gl.glTexParameter(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,image1.width,image1.height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,imgData)
        return texId

def Texload():
     global Textures
     Textures.append(texload("C:/Commonstuff/airachnid.png"))

def sendMessage():
 global respond
 Utext=Uput1.get()
 respond=ollama.chat(model='llama3.2',messages=[{'role':'user','content':Utext}])
 Response.config(text=respond['message']['content'])

window1=tk.Tk()
window1.title("Hello there.")
Uput1=tk.Entry(window1)
Uput1.pack(pady=10)
Response=tk.Label(window1,text="response") 
Response.pack(pady=10)
btn1=tk.Button(window1,text="send message",command=sendMessage)
btn1.pack(pady=10)


def drawFace(x,y,z,r,g,b,scale,tex):
        gl.glPushMatrix()
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D,tex)
        gl.glTranslatef(x,y,z)
        gl.glScalef(scale,scale,1)
        gl.glColor3f(r,g,b)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2i(1,0)
        gl.glVertex3f(1,0,0)
        gl.glTexCoord2i(1,1)
        gl.glVertex3f(1,1,0)
        gl.glTexCoord2i(0,1)
        gl.glVertex3f(0,1,0)
        gl.glTexCoord2i(0,0)
        gl.glVertex3f(0,0,0)
        gl.glEnd()
        gl.glPopMatrix()

class AppOgl(OpenGLFrame):

     def initgl(self):
        """Initalize gl states when the frame is created"""
        gl.glViewport(0, 0, self.width, self.height)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(77,1,0.1,10000)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)    
        Texload()
        self.start = time.time()
        self.nframes = 0

     def redraw(self):
        """Render a single frame"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        drawFace(-2,0,-10,1,1,1,4,Textures[0])
        tm = time.time() - self.start
        self.nframes += 1
        print("fps",self.nframes / tm, end="\r" )


if __name__ == '__main__':
      app = AppOgl(window1, width=520, height=400)
      app.pack(fill=tk.BOTH, expand=tk.YES)
      app.animate = 1
      app.mainloop()
