# remoteio
A Raspberry Pi GPIO remote control based on gpiozero

https://github.com/gpiozero/gpiozero

# remotio with extensions to non gpiozero devices
A remoteio device needs the remote server, where the device is situated, further an ident to identify it on the server for actions.
Last not least the obj_type of the device is needed to work with the right gpiozero device.
The client transfers the following parameter to the server to work with a gpiozero device:
  ident,obj_type,*args,**kwargs
While ident and obj_type are needed by remoteio the parameter *args and **kwargs are directly delegated to the gpiozero device

1. creating a gpiozero device
   rs=RemoteServer(ip_adress,port)
   led=Remote_XXX(rs,*args,**args), where xxx is the name of a gpiozero device like LED,PWMLED,RGBLED etc.
   The ident is automatically generated for the handling with the server, obj_type is just XXX

3. A command like blink(**kwargs) or on(*args) is to be used as described in the API of gpiozero.
   Further remoteio supports on(on_time) for a short impuls realized by blink(on_time=on_time,off_time=0,n=1).

4. remoteio supports a Remoteio_LEDCompositum device, defined by having the attributes on,off,toggle,blink. It supports
  pulse for the gpiozero devices of the Compositum that can pulse. The functions getClientDevice(), setClientDevice() are used to make messages more readable by
  the user. At this purpose gpiozero offers **namedpins and *_order. Note that the devices used in Remote_LEDCompositum may be situated on different server.

5. remoteio supports expressions like led.value=... by the use of properties.
   The attributes of a gpiozero device are reflected in the corresponding remoteio device. Remoteio differs between functions, attributes that are only readable and writeable attributes.
   The remoteio_client.py acts as a kernel for all devices, so that all remote devices are programmed in the same manner.

6. As extensions also non gpio zero devices may be used. But these classes must be wrapped in a form that they can be applied. As example Remote_W1ThermDevice in the folder remoteio_extensions and
   W1ThermDevice in the folder remoteio_wrapper are realized in order to read temperatures. 

For details study the documentation in remoteio/remoteio_doku and the examples in controller.py
      

## Server (remote Raspberry Pi)
Use this all-in-one command to install remoteio as deamon on port `8509`.
The server can be updated with this command.
```bash
bash -c "$(wget -qLO - https://github.com/schech1/remoteio/raw/master/install.sh)"
```

## Using uv

### Server configuration
```bash
uv init remoteio_server
cd remoteio_server
uv add git+ssh://git@github.com/abreumateus/remoteio.git
uv add lgpio
uv add RPi.GPIO
uv add smbus
uv add smbus2
uv add spidev
uv add pigpio
```

When you want to create the server by yourself, you can install the library via
pip or uv and use the examples below, for server- and client usage.


### Server usage
Start a remote server on port `1234`.
If no port is specified default port `8509` will be used

```python
from remoteio import run_server

if __name__ == "__main__":
   # Start remote server
    run_server(port=1234)
```

### Client configuration
```bash
uv init remoteio_client
cd remoteio_client
uv add git+ssh://git@github.com/abreumateus/remoteio.git
uv add lgpio
uv add RPi.GPIO
uv add smbus
uv add smbus2
uv add spidev
uv add pigpio
```

## Client usage
```python
import logging

from remoteio.remoteio_devices.remote_led import Remote_LED

from remoteio import RemoteServer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
   try:
      # Logging configuration and setup
      logging.basicConfig(level=logging.INFO, style="{", format="{asctime}[{levelname:8}]{message}")
      logger = logging.getLogger(name="remoteio")
      logger.setLevel(logging.INFO)

      # Remote server configuration and setup
      server_ip = "pi5mateus"
      server_port = 1234
      rs = RemoteServer(server_ip, server_port)

      # Remote LED configuration and setup
      led = Remote_LED(rs, pin=17, initial_value=False)

      # Gpiozero functions and properties
      print(f"{led.class_name} get functions: {led.functions}")
      print(f"{led.class_name} get properties: {led.readOnlyProperties}")
      print(f"{led.class_name} get and set properties: {led.writeableProperties}")
      
      # Remote LED blink
      led.blink()

      # Remote server close
      rs.close()
   except Exception as e:
      logger.error(f"{e.__class__}: {str(e)}")
```
