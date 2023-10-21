


float AnguloA{};
float AnguloB1{};
float AnguloB2{};
float AnguloC1{};

void setup() {

  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {

  String Texto_Recibido{};
  bool banderaRecibido{};

  while (Serial.available() > 0) {
    Texto_Recibido = Serial.readStringUntil(";");
    banderaRecibido = true;
    digitalWrite(13, HIGH);
  }


  if (banderaRecibido == true) {

    String Auxiliar = Texto_Recibido.substring(Texto_Recibido.indexOf("JA") + 2, Texto_Recibido.indexOf("JB"));

    AnguloA = Auxiliar.toFloat();

    Auxiliar = Texto_Recibido.substring(Texto_Recibido.indexOf("JB") + 2, Texto_Recibido.indexOf(","));
    AnguloB1 = Auxiliar.toFloat();

    Auxiliar = Texto_Recibido.substring(Texto_Recibido.indexOf(",") + 1, Texto_Recibido.indexOf("JC"));
    AnguloB2 = Auxiliar.toFloat();

    Auxiliar = Texto_Recibido.substring(Texto_Recibido.indexOf("JC") + 2, Texto_Recibido.indexOf(";"));
    AnguloC1 = Auxiliar.toFloat();

    banderaRecibido = false;
    //JA-25JB23,25JC12;
    digitalWrite(13, LOW);
    Serial.println("JA"+String(AnguloA)+"JB"+String(AnguloB1)+","+String(AnguloB2)+"JC"+String(AnguloC1)+";");
  }
}
