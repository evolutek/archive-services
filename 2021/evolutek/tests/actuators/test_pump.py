from evolutek.lib.actuators.pump import PumpController
from evolutek.lib.gpio.gpio_factory import GpioType, create_gpio

from time import sleep

pumps = {
    1: [
        create_gpio(0, 'pump1', dir=True, type=GpioType.MCP),
        create_gpio(1, 'ev1', dir=True, type=GpioType.MCP)
    ],
    2 : [
        create_gpio(2, 'pump2', dir=True, type=GpioType.MCP),
        create_gpio(3, 'ev2', dir=True, type=GpioType.MCP)
    ],
    3 : [
        create_gpio(4, 'pump3', dir=True, type=GpioType.MCP),
        create_gpio(5, 'ev3', dir=True, type=GpioType.MCP)
    ],
    4: [
        create_gpio(6, 'pump4', dir=True, type=GpioType.MCP),
        create_gpio(7, 'ev4', dir=True, type=GpioType.MCP)
    ],
    5 : [
        create_gpio(8, 'pump5', dir=True, type=GpioType.MCP),
        create_gpio(9, 'ev5', dir=True, type=GpioType.MCP)
    ],
    6 : [
        create_gpio(10, 'pump6', dir=True, type=GpioType.MCP),
        create_gpio(11, 'ev6', dir=True, type=GpioType.MCP)
    ],
    7 : [
        create_gpio(12, 'pump7', dir=True, type=GpioType.MCP),
        create_gpio(13, 'ev7', dir=True, type=GpioType.MCP)
    ],
    8 : [
        create_gpio(14, 'pump8', dir=True, type=GpioType.MCP),
        create_gpio(15, 'ev8', dir=True, type=GpioType.MCP)
    ],
    9 : [
        create_gpio(18, 'pump9', dir=True, type=GpioType.MCP),
        create_gpio(19, 'ev9', dir=True, type=GpioType.MCP)
    ],
    10 : [
        create_gpio(20, 'pump10', dir=True, type=GpioType.MCP),
        create_gpio(21, 'ev10', dir=True, type=GpioType.MCP)
    ]
}


pump_controller = PumpController(pumps, 1)
print(pump_controller)

for pump in pump_controller:
    pump_controller[pump].get()
    sleep(1)
    pump_controller[pump].drop()
