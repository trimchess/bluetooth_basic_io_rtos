# Source: electrocredible.com , Language: MicroPython
# Import necessary modules
from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import time
import pyRTOS

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Create a Pin object for the onboard LED, configure it as an output
led = Pin("LED", Pin.OUT)
led.value(0)

# Create a Pin object for Pin 0, configure it as an input with a pull-up resistor
pin = Pin(22, Pin.IN, Pin.PULL_UP)

# Create a Pin object for the internal temp sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    global led_state  # Access the global variable led_state
    if data == b'toggle':  # Check if the received data is "toggle"
        led.toggle()

# Define task for temp measuring
def taskTemperature(self):
    while True:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        print(temperature)
        if sp.is_connected():
            msg=f'Temperature: {temperature}C\n'
            sp.send(msg)
        yield [pyRTOS.timeout(10)]

# Define task for internal led control (toggle)
def taskLedInt(self):
    while True:
        # Check if a BLE connection is established
        if sp.is_connected():
            # Set the callback function for data reception
            sp.on_write(on_rx) 
        yield [pyRTOS.timeout(0.1)]

# Define task for button22 control
def taskButton22(self):
    while True:
        if ((pin.value() is 0) and not state_sent):
            if sp.is_connected():
                # Create a message string
                msg="pushbutton pressed\n"
                # Send the message via BLE
                sp.send(msg)
                state_sent = True
        # Update the debounce time    
        if pin.value() is 1:
            state_sent = False
        yield [pyRTOS.timeout(0.1)]



#Add pyRTOS task and start pyRTOS
pyRTOS.add_task(pyRTOS.Task(taskButton22))
pyRTOS.add_task(pyRTOS.Task(taskLedInt))
pyRTOS.add_task(pyRTOS.Task(taskTemperature))

pyRTOS.start()
                