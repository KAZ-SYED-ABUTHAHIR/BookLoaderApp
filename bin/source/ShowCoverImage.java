import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import processing.awt.PSurfaceAWT; 
import processing.awt.PSurfaceAWT.SmoothCanvas; 
import javax.swing.JFrame; 
import processing.core.PApplet; 
import java.awt.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class ShowCoverImage extends PApplet {








Point mouse = new Point(0, 0);
Point pmouse = new Point(0, 0);

int surfacePosX ;
int surfacePosY ;

int w, h ;
PImage webImg;

String url;
String prevUrl;
String[] linesFromFile;

public void setup() { 
  initFrame();
  prevUrl = url;
  frameRate(30);
}

public void initFrame() {
  PSurfaceAWT awtSurface = (PSurfaceAWT) surface;
  SmoothCanvas smoothCanvas = (SmoothCanvas) awtSurface.getNative();
  JFrame jframe = (JFrame)smoothCanvas.getFrame();
  jframe.setVisible(false);
  jframe.dispose();
  jframe.setUndecorated(true);
  //jframe.setOpacity(1.0f);
  PImage icon = loadImage("imgs/Books.png");
  surface.setIcon(icon);

  try {
    linesFromFile = loadStrings("data/CoverURL.txt");
    url = linesFromFile[0];
    webImg = loadImage(url, "png");
    println("Loading Image");
    w = webImg.width; 
    h = webImg.height;
  }
  catch(Exception e) {
    //Do Nothing
  }

  surface.setSize(w, h);
  surface.setResizable(true);
  surfacePosX = PApplet.parseInt(displayWidth/2-width/2);
  surfacePosY = PApplet.parseInt(displayHeight/2-height/2);
  surface.setLocation(surfacePosX, surfacePosY);
  try {
    image(webImg, 0, 0);
  }
  catch(Exception e) {
    //Do Nothing
  }
  jframe.setVisible(true);
  jframe.setAlwaysOnTop(true);
}

public void draw() {
  updateSurface();
  if (frameCount % 45 == 0) {
    thread("updateImage");
  }

  try {
    image(webImg, 0, 0);
  }
  catch(Exception e) {
  }

  try {
    String[] commandLines = loadStrings("data/commands.txt");
    if (commandLines[0].equals("EXIT")) {
      println("Exiting");
      exit();
    }
  }
  catch(Exception e) {
  }
}

public void updateImage() {
  try {
    linesFromFile = loadStrings("data/CoverURL.txt");
    url = linesFromFile[0];
  }
  catch(Exception e) {
  }

  if (!url.equals(prevUrl)) {
    try {
      webImg = loadImage(url, "jpg");
      w = webImg.width; 
      h = webImg.height;
      surface.setSize(w, h);
      prevUrl = url;
    }
    catch(Exception e) {
    }
  }
}

public void updateSurface() {
  pmouse = mouse;
  mouse = MouseInfo.getPointerInfo().getLocation();
  if (mousePressed) {
    surfacePosX -= (pmouse.x - mouse.x);
    surfacePosY -= (pmouse.y - mouse.y);
    surface.setLocation(surfacePosX, surfacePosY);
  }
}



  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "ShowCoverImage" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
