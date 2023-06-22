//float Sensibilidad=0.066; //sensibilidad en Voltios/Amperio para sensor de 30A
//float Sensibilidad=0.185; //sensibilidad en Voltios/Amperio para sensor de 5A



void setup() {
  
  Serial.begin(115200);

}

void loop() {

//  float voltaje = voltaje + (float)25*analogRead(A4)/1023;
//  float voltajeSensor = analogRead(A5)*(5.0 / 1023.0); //lectura del sensor   
//  float corriente = (voltajeSensor-2.5)/Sensibilidad; //Ecuación  para obtener la corriente
  
  
  delay(3);
  
//  Serial.print("Corriente: ");
//  Serial.println(corriente,3);
//  Serial.print("Voltaje: ");
//  Serial.println(voltaje);

  Serial.println(analogRead(A5));
  Serial.println(analogRead(A4));

}

