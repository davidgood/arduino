#include <Arduino_BMI270_BMM150.h>  // Correct IMU library for BLE Sense
#include <ArduinoBLE.h>             // BLE library

// BLE service and characteristic UUIDs
BLEService imuService("180D");   // Create a BLE Service
BLEFloatCharacteristic accXChar("2A37", BLERead | BLENotify);  // Accelerometer X
BLEFloatCharacteristic accYChar("2A38", BLERead | BLENotify);  // Accelerometer Y
BLEFloatCharacteristic accZChar("2A39", BLERead | BLENotify);  // Accelerometer Z

void setup() {
  // Initialize BLE
  if (!BLE.begin()) {
    // If BLE initialization fails, just loop indefinitely
    while (1);
  }

  // Initialize IMU
  if (!IMU.begin()) {
    // If IMU initialization fails, just loop indefinitely
    while (1);
  }

  // Set Bluetooth device name and advertise the IMU service
  BLE.setLocalName("Nano 33 BLE IMU");
  BLE.setAdvertisedService(imuService);

  // Add characteristics to the service
  imuService.addCharacteristic(accXChar);
  imuService.addCharacteristic(accYChar);
  imuService.addCharacteristic(accZChar);

  // Add the service
  BLE.addService(imuService);

  // Start advertising BLE service
  BLE.advertise();
}

void loop() {
  // Wait for a BLE central to connect
  BLEDevice central = BLE.central();

  if (central) {
    // While central is connected, send IMU data
    while (central.connected()) {
      // Check if IMU data is available
      if (IMU.accelerationAvailable()) {
        float accX, accY, accZ;
        IMU.readAcceleration(accX, accY, accZ);

        // Transmit IMU data over BLE
        accXChar.writeValue(accX);
        accYChar.writeValue(accY);
        accZChar.writeValue(accZ);
      }
      delay(100);  // Adjust the delay to control transmission frequency
    }
  }
}