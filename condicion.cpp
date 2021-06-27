#include <iostream>


namespace std;

int main(){
    cout<<"hola";



}


  var numeroFactorial = 6;
  while (numeroFactorial > -1) {
      var fact = 1;
      var cadena1 = "El factorial de: " + numeroFactorial + " = ";
      if (numeroFactorial =! 0) {
        for (var i = numeroFactorial; i > 0; i--) {
          fact = fact * i;
          cadena1 = cadena1 + i;
          if (i > 1) {
            cadena1 = cadena1 + " * ";
          } else {
            cadena1 = cadena1 + " = ";
          }
        }
      }
      cadena1 = cadena1 + fact;
      print(cadena1);
      numeroFactorial=numeroFactorial-;
  }



      print("----------------CICLO WHILE Y FOR---------------");
    var numeroFactorial = 0;
    while (numeroFactorial > -1) {
        var fact = 1;
        var cadena1 = "El factorial de: " + numeroFactorial + " = ";
        if (numeroFactorial =! 0) {
          for (var i = numeroFactorial; i > 0; i--) {
            fact = fact * i;
            cadena1 = cadena1 + i;
            if (i > 1) {
              cadena1 = cadena1 + " * ";
            } else {
              cadena1 = cadena1 + " = ";
            }
          }
        }
        cadena1 = cadena1 + fact;
        print(cadena1);
        numeroFactorial--;
    }

