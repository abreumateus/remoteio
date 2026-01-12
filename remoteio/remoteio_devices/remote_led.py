#!/usr/bin/env python3
import logging

from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory

from remoteio.remoteio_client import RemoteDigitalDevice, RemoteServer
from remoteio.remoteio_helper import (
    getFunctionName,
    getFunctions,
    getReadOnlyProperties,
    getWriteableProperties,
)

logger = logging.getLogger(__name__)


class Remote_LED(RemoteDigitalDevice):
    """
    class Remote_LED(
        remote_server:RemoteServer,
        *args,
        **kwargs
    )
    class LED(
        pin: Any | None = None,
        *,
        active_high: bool = True,
        initial_value: bool = False,
        pin_factory: Any | None = None
    )
    initializes the corresponding gpiozero-device on the remote server by args and kwargs
    """

    def __init__(self, remote_server: RemoteServer, *args, **kwargs):
        if args != ():
            if len(args) == 1:
                kwargs["args"] = args
            else:
                raise ValueError("LED has 1 positional parameter")
        super().__init__(remote_server, "LED", **kwargs)

        try:
            Device.pin_factory = MockFactory()
            self.gpiozero_info = LED(17)
            self.functions = getFunctions(self.gpiozero_info)
            self.readOnlyProperties = getReadOnlyProperties(self.gpiozero_info)
            self.writeableProperties = getWriteableProperties(self.gpiozero_info)
        except Exception as e:
            logger.error(f"{e.__class__}: {str(e)}")
            self.functions = [
                "blink",
                "close",
                "ensure_pin_factory",
                "off",
                "on",
                "toggle",
            ]
            self.readOnlyProperties = ["closed", "is_active", "is_lit", "pin", "values"]
            self.writeableProperties = [
                "active_high",
                "pin_factory",
                "source",
                "source_delay",
                "value",
            ]

    def blink(self, **kwargs):
        self.func_exec(getFunctionName(), **kwargs)

    def ensure_pin_factory(self, **kwargs):
        self.func_exec(getFunctionName(), **kwargs)

    def off(self, **kwargs):
        self.func_exec(getFunctionName(), **kwargs)

    def on(self, **kwargs):
        if "on_time" in kwargs.keys():
            self.blink(on_time=kwargs["on_time"], off_time=0, n=1)
        else:
            self.func_exec(getFunctionName(), **kwargs)

    def toggle(self, **kwargs):
        self.func_exec(getFunctionName(), **kwargs)

    # Treated in super_class: open and close

    # Properties with get
    @property
    def closed(self):
        return self.getProperty(getFunctionName())

    @property
    def is_active(self):
        return self.getProperty(getFunctionName())

    @property
    def is_lit(self):
        return self.getProperty(getFunctionName())

    @property
    def pin(self):
        return self.getProperty(getFunctionName())

    @property
    def class_name(self):
        return self.__class__.__name__

    # Properties with get and set
    @property
    def active_high(self):
        return self.getProperty(getFunctionName())

    @active_high.setter
    def active_high(self, wert):
        self.func_exec("set", active_high=wert)

    @property
    def pin_factory(self):
        return self.getProperty(getFunctionName())

    @pin_factory.setter
    def pin_factory(self, wert):
        self.func_exec("set", pin_factory=wert)

    @property
    def source_delay(self):
        return self.getProperty(getFunctionName())

    @source_delay.setter
    def source_delay(self, wert):
        self.func_exec("set", source_delay=wert)

    # Treated in super_class: source and values


if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.INFO, style="{", format="{asctime}[{levelname:8}]{message}"
        )
        logger = logging.getLogger(name="remoteio")
        logger.setLevel(logging.INFO)

        server_ip = "pi5mateus"
        server_port = 1234
        rs = RemoteServer(server_ip, server_port)

        led = Remote_LED(rs, pin=17, initial_value=False)

        # Gpiozero functions and properties info
        print(f"{led.class_name} get functions: {led.functions}")
        print(f"{led.class_name} get properties: {led.readOnlyProperties}")
        print(f"{led.class_name} get and set properties: {led.writeableProperties}")

        led.blink()
        rs.close()
    except Exception as e:
        logger.error(f"{e.__class__}: {str(e)}")
