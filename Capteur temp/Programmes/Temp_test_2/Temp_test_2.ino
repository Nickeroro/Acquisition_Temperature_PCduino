
#include <core.h>
int adc_id = 2;
int delay_ms = 2000;

void setup()
{
  
}

void loop()
{
    int value = analogRead(adc_id); // get adc value
    float tension = value * 3.3 / 4096;
    float temperatureC = (tension - 0.5) * 100 ;
    printf("ADC%d tension (V) : %.3f\n",adc_id, tension, "C");
    printf("temperature (C) : %.2f\n", temperatureC);
    printf("---------------------------\n");
  
    delay(delay_ms);  
}
