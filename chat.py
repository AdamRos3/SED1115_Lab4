# Uses serial blocking input given in announcement
'''
Uses serial blocking input given in announcement
Although you can recieve multiple messages without hanging,
when in input mode, no messages can be recieved
'''

from machine import Pin, UART
import time
import uasyncio as asyncio

# Initialize UART for internal use
uart_internal = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart_internal.init(bits=8, parity=None, stop=1) 

# Initialize UART to simulate eternal pico
uart_external = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart_external.init(bits=8, parity=None, stop=1)

# Configure button input with internal pull-up
blocking_button = Pin(13, Pin.IN, Pin.PULL_DOWN)

# Will simulate message being sent from other pico for self testing
sim_button = Pin(11, Pin.IN, Pin.PULL_DOWN)

data_to_send = "Button pressed!"
print("Press Westbount button to send message over UART")
print("Press Eastbound button to simulate sending message over UART to device")
print()

blocking_prev_state = 0
sim_prev_state = 0

while True:
    
    blocking_current_state = blocking_button.value()
    sim_current_state = sim_button.value()

    # Detect button press (HIGH to LOW)
    if (blocking_prev_state == 1 and blocking_current_state == 0):
        # get (blocking) user input
        data_to_send = input("Data to send? ")
        uart_internal.write(data_to_send.encode('utf-8'))
        print("Message sent: <", data_to_send.strip(), ">")
        
        # Debounce delay
        time.sleep(0.3)
    
    # Detect button press (HIGH to LOW)
    if (sim_prev_state == 1 and sim_current_state == 0):
        # send message to pico
        uart_external.write("Message from other pico".encode('utf-8'))

        time.sleep(0.3)

    blocking_prev_state = blocking_current_state
    sim_prev_state = sim_current_state
    time.sleep(0.01)

    # Check for any incoming UART data
    if (uart_internal.any()):
        data = uart_internal.read()
        if data:
            print("Recevied:", data.decode('utf-8').strip())
        else:
            print("Null message recevied")

    # sending keep alive, current time in milliseconds
    sending_time = int(time.time() * 1000)
    message_time = str(sending_time)

    uart_internal.write(message_time.encode('utf-8'))

    time.sleep(0.01)

    # receiving keep alive, time in milliseconds from other machine
    if (uart_internal.any()):
        received_time = uart_internal.read()

    
        if received_time:
            try:
                received_time = int(received_time.decode('utf-8').strip())

                if ((received_time - sending_time) >= 1):
                    print("Connection timeout")
                    break

            except:
                print("Error in keep alive")
                break

        else:
            print("Keep alive recieved but empty")
            break

    else:
        print("keep alive not recieved")
        break

print("... terminating connection")
