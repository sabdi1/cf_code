float data[4] = {1.123456789f,2.654978321f,3.147258369f,4.963852741f};

void setup() {
  Serial.begin(9600);

}

void loop() {
  static byte cmd = 0x00;

  if(Serial.available())
  {
    cmd = Serial.read();
    
    switch(cmd)
    {
      case 0x77:
          Serial.write((byte *)data,4*sizeof(float));
          break;

      default: 
          break;

    }
  }

  delay(100);
  cmd = 0x00;
}
