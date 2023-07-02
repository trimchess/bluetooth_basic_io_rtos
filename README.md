# bluetooth_basic_io_rtos
App for using bluetooth with micropython for the Pico-W.
The task timing is done by the pyRTOS task switcher (see https://github.com/Rybec/pyRTOS).
Copy the lib content to the Pico-W and rund the app (bluetooth_button_led_temp_pyRTOS.py) in Thonny
(or copy it as main.py on the Pico-W).
You need a bluetooth client to control. I use the BLE Serial Pro from the iOS App-Store.
You can switch the internal Pico-W LED with the command "toggle".
The app pushes the "pressed" event on button GPIO22 and periodically the temperature, measured with the internal ADC(4).
I wrote the app just for test the new BT feature. Have fun.
