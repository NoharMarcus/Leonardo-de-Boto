#include <ESP8266WiFi.h>
#include <Servo.h>

const char* ssid = "De_Boto_wifi";
const char* password = "12345678";
const byte lift_code = 220;
const byte lower_code = 210;// this code is for lowering the pen in order to send it it is enoght to send it only in the alpha angle of the vector
const byte change_delay_time = 200; // change delay between commands
const int relay_pin = D1;
int delay_time = 1000;

// SERVO STRUCTURE
class our_Servo{
  private:
  Servo servo;
  public:  
    int port;//port to attach the servo
    int low;//low value of the servo
    int high;//high velue of the servo
    float step_size;//step size in microseconeds for the servo

    void attach(int port_to,int low_to, int high_to ,float step_size_to){
      port = port_to;
      low = low_to;
      high = high_to;
      step_size = step_size_to;
      servo.attach(port,low,high);
    }

    void write(int angle){
      if(angle<=180 & angle>=0){
//        servo.writeMicroseconds(low + (int)angle*step_size);
        servo.write(angle);
      }
      else
        Serial.printf("angle not in range");
    }

    void raise(){
        servo.writeMicroseconds(1900);
        }
    void lower(){
        servo.writeMicroseconds(2300);
        }
};





//UDP Setup paramters
#define SendKey 0  //Button to send data Flash BTN on NodeMCU

int port = 8888;  //Port number
WiFiServer server(port);

//AP-Acess Point setup parameters
IPAddress local_IP(192,168,4,22);
IPAddress gateway(192,168,4,9);
IPAddress subnet(255,255,255,0);

//Declering Servos
our_Servo alpha;
our_Servo beta;
our_Servo lift;

//initial angles for beta and alpha motors
int alpha_angle = 90;
int beta_angle = 120;

// function to start UDP SERVER on ESP 8266
void start_TCP() {

  server.begin();
  Serial.print("Open Telnet and connect to IP:");
  Serial.print(local_IP);
  Serial.print(" on port ");
  Serial.println(port);
}

//*********************************************

//function to open up  access point  on esp8266
void start_AP() { 
  
  Serial.println();

  Serial.print("Setting soft-AP configuration ... ");
  Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Ready" : "Failed!");

  Serial.print("Setting soft-AP ... ");
  Serial.println(WiFi.softAP(ssid, password, 1, false, 1) ? "Ready" : "Failed!");

  Serial.print("Soft-AP IP address = ");
  Serial.println(WiFi.softAPIP());
}

//*********************************************

int count = 0;

void setup() {
  //Staring Serial
  Serial.begin(115200); 
  Serial.println("strating");
  start_AP();//start Access point
  pinMode(relay_pin,OUTPUT);
  digitalWrite(relay_pin,HIGH);
  delay(1000);

  
   //setting up servo in D4 to be alpha angle
  //alpha.attach(D1,650,2200); //alpha angle motor 300 to 2500 pwm frequency
  alpha.attach(D4,880,2080,6.67);   //alpha angle motor 300 to 2500 pwm frequency yellow
  alpha.write(180-alpha_angle);
  
  
  //setting up servo in D8 to be beta angle
  //beta.attach(D2,550,2150); //beta angle motor 300 to 2500 pwm frequency
  beta.attach(D8,980,2310,7.78);   //beta angle motor 300 to 2500 pwm frequency green
  beta.write(beta_angle);

  lift.attach(D2,1900,2300,9);   //beta angle motor 300 to 2500 pwm frequency green
  lift.raise();
  

  
  start_TCP();// start usp server 

  delay(5000); // time for tal to go to see De- Boto
}

//*********************************************


void Lift_Pen() {

  lift.raise();
  Serial.println("Pen is lifted");
}

// TODO - THIS
// _end_of_drawing_vector_ functionality [lift pen up]
void Lower_Pen() {
  
  lift.lower();
  Serial.println("Pen is lowered");
}

//*********************************************

//Massage Handeler ONLY CHANGE THIS
void Message_Handler(byte alpha_angle , byte beta_angle) {
  
  if( (alpha_angle <= 180) & (alpha_angle >= 0) & (beta_angle >= 0) & (beta_angle <= 180) )  {

    //moving servo in D1 which is alpha angle
    alpha.write(int(180-alpha_angle));
    

    //moving servo in D2 which is beta angle
    beta.write(int(beta_angle));
    
    delay(delay_time);//optinal
  }  
  else {
    // if lift is requested 
    if((alpha_angle == lift_code ) & (beta_angle == lift_code )) { 
      Lift_Pen();
      delay(delay_time);
      
    } else if((alpha_angle == lower_code ) & (beta_angle == lower_code )) {
      Lower_Pen();
      delay(delay_time);
    } 
    else if(alpha_angle == change_delay_time ) {
      delay_time = 100*beta_angle;
      Serial.printf(" changed delay time to: %d ",delay_time);
    } 
    else {

      Serial.printf("alpha: %d ,beta : %d are not in range, and not special commands\n",alpha_angle ,beta_angle);
    }
  } 
}

//*********************************************

//*********************************************

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    if(client.connected()) {
      Serial.println("Client Connected");
      client.print(lift_code);
      client.print(lower_code);
      digitalWrite(relay_pin,LOW);
      //client.print(change_delay_time);
    }

    while(client.connected()) {    

      // main vector loop
      while(client.available()>0) {

        // read data from the connected client
        byte alpha_angle = client.read();
        byte beta_angle = client.read();

        // move pen to vec coordinates
        Message_Handler(alpha_angle,beta_angle);
        //delay(9000);
      }
    }
  
    client.stop();
    Serial.println("Client disconnected");
    delay(2000);
    digitalWrite(relay_pin,HIGH);
  }
}
