#define PIN_PULSADOR 2
#define PIN_LED_PULSADOR 9
#define PIN_LED_CONN 10
#define PIN_BUZZER 8

int seconds = 0;

bool CONN = false;
char HANDSHAKE[]   = "{milo}";
char SALUDO[]      = "{tatu}";
char EXIT_CONN[]   = "{piolin}";

char S_MSJ[] = "(";
char F_MSJ[] = ")";
//char TCD[]         = "(tcd)";
int VENTANA_HANDSHAKE = 1000;
int DELAY_BALIZA = 500;

unsigned long tiempo1 = 0;
unsigned long tiempo2 = 0;

unsigned long tiempo3 = 0;
unsigned long tiempo4 = 0;
int TIC = 60;
byte LINEA  = 8;
byte PUNTO  = 2;

int OFFSET=0;

byte MAX_TIC = 7;
int LIMITE = (LINEA*MAX_TIC+MAX_TIC)*TIC;
int CLEAR  = TIC*10;
int default_time_blanco=2500;
int BLANCO = default_time_blanco;
  
bool last_is_space=false;
int LAST = 0;
int LAST_BLANCO = 0;
int MORSE_BUFFER[100];
int puntero_buffer=0;
int ESTADO = 0;
int valor_falso = 2;
char caracter[][5]= {"A","B","C","CH","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9",".",","};
char anotacion[][15]= {".-","-...","-.-.","----","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","--.--","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..","-----",".----","..---","...--","....-",".....","-....","--...","---..","----.",".-.-.-","--..--"};


void agregar_espacio(){
  if(!last_is_space){
    Serial.println("( )");
    last_is_space=true;
    }
  }

void decodificar(char code[]){
    int tam=50;
    char deco[tam]="";
    char desconocido[]="(?)";
    bool bandera=false;
    int size_anotacion;
    size_anotacion = sizeof(anotacion)/sizeof(anotacion[0]);
    for(int i=0;i<size_anotacion;i++){
      char str1[tam];
      //Serial.println(anotacion);
      strcpy(str1,anotacion[i]);
      int result = strcmp(str1, code);
      if(result==0){
        bandera=true;
        strcat(deco,S_MSJ);
        strcat(deco,caracter[i]);
        strcat(deco,F_MSJ);
        break;
    }
    };
  if(bandera){Serial.println(deco);last_is_space=false;}
  else{Serial.println(desconocido);last_is_space=false;}
 }

void limpiar_buffer()
  {
  int size;
  size = sizeof(MORSE_BUFFER)/sizeof(MORSE_BUFFER[0]);
  for(int i=0;i<size;i++){
    MORSE_BUFFER[i]=0;
    };
  puntero_buffer=0;
  }

int sumar_buffer()
  {
  int size;
  size = sizeof(MORSE_BUFFER)/sizeof(MORSE_BUFFER[0]);
  int suma=0;
  for(int i=0;i<size;i++){
    int val=MORSE_BUFFER[i];
    suma+=val;
    //else{break;}
    }
  return suma;
  }


void imprimir(){
      int size;
      size = sizeof(MORSE_BUFFER)/sizeof(MORSE_BUFFER[0]);
      Serial.print("[");
      for(int i=0;i<size;i++){
      Serial.print(MORSE_BUFFER[i]);
        };
      Serial.print("]");
      Serial.println("");
}


void interpretar()
  {
  char code[100]="";
    int tam_buffer=sumar_buffer();
    if (tam_buffer>0){
      //imprimir();
      int size_buffer;
      size_buffer = sizeof(MORSE_BUFFER)/sizeof(MORSE_BUFFER[0]);
      int last=0;
      int duracion=0;
      for(int i=0;i<size_buffer;i++){
      if(MORSE_BUFFER[i]==0){
          if(duracion>0){
          int abs_to_line= abs(LINEA-duracion);
          int abs_to_dot = abs(PUNTO-duracion); 
          if (abs_to_line<abs_to_dot){
            char linea[]="-";
            strncat(code, linea, sizeof(code)-1);}
          else{
            char linea[]=".";
            strncat(code, linea, sizeof(code)-1);};          
          };
          duracion=0;
          }
        else if(MORSE_BUFFER[i]==1){
          duracion+=1;}
        }
    //Serial.print("DECODIFICAR : ");
    //Serial.println(code);
    decodificar(code);
      }
  }

void append_estado()
  {
  int size;
  size = sizeof(MORSE_BUFFER)/sizeof(MORSE_BUFFER[0]);
  if (puntero_buffer<size){
    MORSE_BUFFER[puntero_buffer]=ESTADO;
    puntero_buffer+=1;
    }
     //strncat(MORSE_BUFFER, ESTADO, sizeof(MORSE_BUFFER));
  }

void control_tic()
  {
  LAST+=TIC;
  LAST_BLANCO+=TIC;
  append_estado();
  if (LAST_BLANCO>=BLANCO){
    if(BLANCO!=default_time_blanco){BLANCO=default_time_blanco;};
    agregar_espacio();LAST_BLANCO=0;}
  if (ESTADO){LAST = 0;LAST_BLANCO=0;}
  else{
    if (LAST>=CLEAR or LAST>=LIMITE){
    interpretar();
    LAST=0;
      limpiar_buffer(); //MORSE_BUFFER=[];
    };
    }
  //actualizar ticker tic .. raiz.after(TIC,leer_estado)
  }
void prender_led_conn(){
         digitalWrite(PIN_LED_CONN, HIGH);
         digitalWrite(PIN_BUZZER,HIGH);
         delay(100);
         digitalWrite(PIN_LED_CONN, LOW);
         digitalWrite(PIN_BUZZER,LOW);
         delay(100);
         digitalWrite(PIN_LED_CONN, HIGH);
         digitalWrite(PIN_BUZZER,HIGH);
         delay(100);
         digitalWrite(PIN_LED_CONN, LOW);
         digitalWrite(PIN_BUZZER,LOW);
         delay(50);
         digitalWrite(PIN_LED_CONN, HIGH);    
  }

bool broken_conn(){
  char incoming_msj[50]="";
  int cursor_msj=0;
  while (Serial.available() > 0) {
    // get incoming byte:
    char inByte;
    inByte = Serial.read();
    if (cursor_msj==sizeof(incoming_msj)-2){
      break;
      }
    else if (inByte!='\n'){
      incoming_msj[cursor_msj]=inByte;
      cursor_msj++;
      }
    else{
      //incoming_msj[cursor_msj]='\n';
      //cursor_msj++;
      incoming_msj[cursor_msj]='\0';
      }
    }
    if (cursor_msj>0){
        int result = strcmp(incoming_msj, EXIT_CONN);
        //Serial.print("incoming_msj:");
        //Serial.print(incoming_msj);
        //Serial.print("  -  ");
        //Serial.println(result);
        if(result==0){
          digitalWrite(PIN_LED_CONN, HIGH);
          digitalWrite(PIN_BUZZER,HIGH);
          delay(1000);
          digitalWrite(PIN_LED_CONN, LOW);
          digitalWrite(PIN_BUZZER,LOW);
          delay(100);
          
          digitalWrite(PIN_LED_CONN, HIGH);
          digitalWrite(PIN_BUZZER,HIGH);
          delay(200);
          digitalWrite(PIN_LED_CONN, LOW);
          digitalWrite(PIN_BUZZER,LOW);
          delay(100);
          
          digitalWrite(PIN_LED_CONN, HIGH);
          digitalWrite(PIN_BUZZER,HIGH);
          delay(200);
          digitalWrite(PIN_LED_CONN, LOW);
          digitalWrite(PIN_BUZZER,LOW);
          delay(100);

          return true;
        }    
      
      };
    return false;
  }

void saludar() {
  if (Serial.available() <= 0) {
    Serial.println(SALUDO);   
  }
}

void escuchar() {
  char incoming_msj[50]="";
  int cursor_msj=0;
  while (Serial.available() > 0) {
    // get incoming byte:
    char inByte;
    inByte = Serial.read();
    if (cursor_msj==sizeof(incoming_msj)-2){
      return;
      }
    else if (inByte!='\n'){
      incoming_msj[cursor_msj]=inByte;
      cursor_msj++;
      }
    else{
      //incoming_msj[cursor_msj]='\n';
      //cursor_msj++;
      incoming_msj[cursor_msj]='\0';
      }
    }
    if (cursor_msj>0){
        int result = strcmp(incoming_msj, HANDSHAKE);
        Serial.print("incoming_msj:");
        Serial.print(incoming_msj);
        Serial.print("  -  ");
        Serial.println(result);
        if(result==0){
          CONN=true;
          Serial.println(">> CONN ESTABLECIDA");  
          prender_led_conn(); 
      }    
      
      }
  }

void setup()
{
  Serial.begin(9600);
  tiempo1 = millis();
  tiempo3 = millis();
  Serial.println("setup completo");
  Serial.flush();
  pinMode(PIN_LED_PULSADOR, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_PULSADOR, INPUT);
  //pinMode(PIN_CLEAR_LAST, INPUT);
  
}

void loop()
{  
  bool btn_pulsador;
  btn_pulsador = digitalRead(PIN_PULSADOR);
  if (btn_pulsador == HIGH) {
      // turn LED on:
      ESTADO=1;
      digitalWrite(PIN_LED_PULSADOR, HIGH);
      digitalWrite(PIN_BUZZER,HIGH);
      } else {
            // turn LED off:
          ESTADO=0;
          digitalWrite(PIN_LED_PULSADOR, LOW);
          digitalWrite(PIN_BUZZER,LOW);
            };
  
  /*bool btn_clear_all;
  btn_clear_all = digitalRead(PIN_CLEAR_ALL);
  if(btn_clear_all == HIGH) {
      clear_all();
      delay(500);
      };*/
  tiempo2 = millis();
  if(tiempo2 > (tiempo1+TIC)){  
    tiempo1 = millis(); //Actualiza el tiempo actual
    tiempo2 = millis();
    control_tic();
   };
  
  tiempo4 = millis();
  if(tiempo4 > (tiempo3+DELAY_BALIZA)){
    tiempo3 = millis();
    tiempo4 = millis();
    if(!CONN){
      saludar();
      escuchar();
      }
    else{
      if(broken_conn()){
        CONN = false;
        Serial.println("<< BROKEN CONN ");  
        };}
      }
}
