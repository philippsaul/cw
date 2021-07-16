import cv2
import numpy as np


class menu:
    def __init__(self):
        self.frame = 0
        self.menu_content = ["Ball Jagen", "Mario Kart", "Tore fahren", "Settings", "bla", "back"]
        self.menu_images = ["../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg","../../assets/background_menu.jpg"]
        self.active_menu_item = 1
    
    def draw_background(self):
        self.frame = cv2.imread(self.menu_images[self.active_menu_item])

    def draw_shapes(self, shape_multiplier):
        for i in range(len(self.menu_content)):
            pts = np.array([[40,(i+1)*100-20],[20,(i+1)*100],[40, (i+1)*100+20],[shape_multiplier*200, (i+1)*100+20],[shape_multiplier*200+20, (i+1)*100],[shape_multiplier*200, (i+1)*100-20]], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.fillPoly(self.frame, [pts], (100,100,100))
            
    def draw_text(self):
        for i in range(len(self.menu_content)):
            if self.menu_content[i] == "back":
                    cv2.putText(self.frame,self.menu_content[i],(750,500), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0) if (self.active_menu_item == i) else (255, 255, 255), 2, cv2.LINE_AA)
            else:             
                cv2.putText(self.frame,self.menu_content[i],(50,(i+1)*100+12), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0) if (self.active_menu_item == i) else (255, 255, 255), 2, cv2.LINE_AA)
    
    def draw(self):
        self.draw_background()
        self.draw_shapes(1.5)
        self.draw_text()

    def open(self):   
        while True:   
          
            self.draw()
            cv2.imshow("name", self.frame)
            cv2.waitKey(0)
  
menu = menu()
menu.open()