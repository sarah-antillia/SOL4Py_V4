# Copyright 2020-2021 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#  CubeRotationByTimerThread.py

# encodig: utf-8

import sys
import threading

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLTimerThread import *

class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):

    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle = 0
      self.timerThread = None
      

    def initializeGL(self):
      glEnable(GL_DEPTH_TEST)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)

      self.lock        = threading.Lock()

      self.timerThread = ZOpenGLTimerThread(self, 30)
      self.timerThread.start()
 
  
    def paintGL(self):
      self.lock.acquire()
      
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glLoadIdentity()
      glTranslatef(0.0, 0.0, 0.0)
      gluLookAt(2.0, 4.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0); 

      self.angle = self.angle + 0.4
      
      #
      vertices = [
      -0.5, -0.5,  0.5,
       0.5, -0.5,  0.5,
       0.5,  0.5,  0.5,
      -0.5,  0.5,  0.5,

      -0.5, -0.5, -0.5,
       0.5, -0.5, -0.5,
       0.5,  0.5, -0.5,
      -0.5,  0.5, -0.5
      ]
    
      #Colors(RGBs) for the 5 vertices
      colors = [ 
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        1.0, 1.0, 1.0,

        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        1.0, 1.0, 1.0
      ]
  
      #Indices for the 4 triangles.
      indices = [ 
        0, 1, 2,  2, 3, 0,
        3, 2, 6,  6, 7, 3,
        7, 6, 5,  5, 4, 7,
        4, 5, 1,  1, 0, 4,
        4, 0, 3,  3, 7, 4,
        1, 5, 6,  6, 2, 1
      ]

      #Rotation around y-axis.
      glRotate(self.angle, 0.0, 1.0, 0.0);
      
      glEnableClientState(GL_VERTEX_ARRAY); 
      glEnableClientState(GL_COLOR_ARRAY);

      #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

      glVertexPointer(3, GL_FLOAT, 0, vertices);
      glColorPointer (3, GL_FLOAT, 0, colors);
      dindices = np.array(indices, "int32")         
      glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, dindices);

      glFlush()
      self.lock.release()

      
    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)

      glMatrixMode(GL_MODELVIEW);


    def terminate(self):
      self.timerThread.terminate()
      self.timerThread.quit()
      self.timerThread.wait()
      print("TimerThread terminated")

  ##--------------------------------------------


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
     
    self.show()
  
    
  def closeEvent(self, ce):
    self.opengl_view.terminate()
    self.terminated = True
    sys.exit(0)

#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

