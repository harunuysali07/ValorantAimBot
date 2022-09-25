#include <Mouse.h>//Mouse kütüphanemizi dahil ediyoruz

int incomingByte = 0; // for incoming serial data
String ReceivedDataString = "";

void setup()
{  
  Serial.begin(115200);
}

void loop()
{
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if(char(incomingByte) == 'X')
    {
      int movementX = ReceivedDataString.toInt();
      if(movementX > 125) {
        Mouse.move(movementX - 125,0, 0);
        movementX = 125;
      }else if(movementX < -125){
        Mouse.move(movementX + 125,0, 0);
        movementX = -125;
      }
      Mouse.move(movementX,0, 0);
      ReceivedDataString = "";
    }else if(char(incomingByte) == 'Y')
    {
      int movementY = ReceivedDataString.toInt();
      if(movementY > 125) {
        Mouse.move(0,movementY - 125, 0);
        movementY = 125;
      }else if(movementY < -125){
        Mouse.move(0,movementY + 125, 0);
        movementY = -125;
      }
      Mouse.move(0,movementY, 0);
//      Mouse.press(MOUSE_LEFT);
//      Mouse.release(MOUSE_LEFT);    
      ReceivedDataString = "";
    }else {
      ReceivedDataString += char(incomingByte);
      //124 = '|'
      //45 =  '-'
      //43 =  '+'
      //88 = 'X'
      //89 = 'Y'
    }
  }
} 
