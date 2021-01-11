
void setup() 
{
  Serial.begin(9600); // set the baud rate
  Serial.println("2.1"); // print "Ready" once
}

void loop() 
{
  static char buffer[50];
  static size_t pos;
  if (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {  // on end of line, parse the number
          buffer[pos] = '\0';
          float value = atof(buffer);
          //Serial.print("received: ");
          float new_value = value + 0.1;
          Serial.println(value);
          pos = 0;
      } else if (pos < sizeof buffer - 1) {  // otherwise, buffer it
          buffer[pos++] = c;
      }
  }
}
