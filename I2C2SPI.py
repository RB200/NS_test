import busio

class I2C2SPI:
    def __init__(self,i2c:busio.I2C,addr:int = hex(40)) -> None:
        self.addr = addr
        self.i2c = i2c
        self.gpio_states = []
        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0xF0,0x02])) # chip init
        self.i2c.unlock()

    def write(self,buffer:bytearray):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0x01]) + buffer) # target addr + function id + data
        self.i2c.unlock()
    
    def readinto(self,buffer:bytearray):
        self.i2c.try_lock()
        self.i2c.readfrom_into(self.addr,buffer) # read from target addr into buffer
        self.i2c.unlock()
    
    def write_readinto(self,out_buffer:bytearray,in_buffer:bytearray):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0x01]) + out_buffer) # target addr + function id + data
        self.i2c.readfrom_into(self.addr,in_buffer) # read from target addr into buffer
        self.i2c.unlock()
    
    def gpio_enable(self,gpios:list=[False,False,False]):
        """
        gpios: [GPIO0,GPIO1,GPIO2]\n
        True to enable GPIO, False to disable GPIO
        """
        gpio_dir = (gpios[0] << 2) + (gpios[1]<<1) + gpios[2]
        self.gpio_states = gpios
        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0xF6,gpio_dir]))
        self.i2c.unlock()

    def gpio_config(self,gpios:list = [0b01,0b01,0b01]):
        """
        gpios: [GPIO0,GPIO1,GPIO2]\n

        pg. 9 of datasheet:\n
        00: input-only (high impedance)\n
        01: push-pull (our default choice)\n
        10: input-only (high impedance)\n
        11: open-drain
        """
        if len(self.gpio_states) == 0:
            raise Exception("GPIOs not enabled: use gpio_enable() to enable")
        
        gpio_cfg = 0
        for i in range(len(self.gpio_states)): 
            if self.gpio_states[i] != 0:  # checking if the pin is a GPIO or SS
                gpio_cfg += gpios[i] << (4-(i*2))

        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0xF7,gpio_cfg]))
        self.i2c.unlock()
    
    def gpio_read(self,buffer):
        
        return

    def gpio_write(self,buffer:bytearray):
        self.i2c.try_lock()
        self.i2c.writeto(self.addr,bytearray([0xF4] + buffer)) # should be between 0x00 and 0x07
        self.i2c.unlock()
    


    
