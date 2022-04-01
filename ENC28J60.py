import spidev
import time

class ENC28J60():
  def __init__(
    self,
    bus,
    device
    ):

    super(ENC28J60, self).__init__()

    # SPI setup
    self.spi = spidev.SpiDev()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 524288
    self.spi.mode = 0

    self.ADDR_MASK	= 0x1F
    self.ENC28J60_BIT_FIELD_SET	= 0x80
    self.ENC28J60_BIT_FIELD_CLR	= 0xA0

    # Addresses
    self.ECON1 = 0x1F
    self.ECON2 = 0x1E

    # Bit masks
    self.ECON1_RXEN = 0x04 
    self.ECON2_PWRSV = 0x20

  def spi_write_op(self, op, address, mask):
    msg = [(op | (address & self.ADDR_MASK)), mask]
    ret = self.spi.xfer2(msg)

  def BFCReg(self, address, mask):
    self.spi_write_op(
      self.ENC28J60_BIT_FIELD_CLR, 
      address, 
      mask
    )

  def BFSReg(self, address, mask):
    self.spi_write_op(
      self.ENC28J60_BIT_FIELD_SET, 
      address, 
      mask
    )

  def power_down(self):

    # Disable packet reception
    self.BFCReg(address=self.ECON1, mask=self.ECON1_RXEN)

    time.sleep(1)
    # Make sure any last packet which was in-progress when RXEN was cleared is completed
    # while(ReadETHReg(ESTAT).ESTATbits.RXBUSY

    # If a packet is being transmitted, wait for it to finish
    # while(ReadETHReg(self.ECON1).ECON1bits.TXRTS)

    #Enter sleep mode
    self.BFSReg(self.ECON2, self.ECON2_PWRSV)

  def power_up(self):

    # Leave power down mode
    self.BFCReg(self.ECON2, self.ECON2_PWRSV)

    #Wait for the 300us Oscillator Startup Timer (OST) to time out.  This
    #delay is required for the PHY module to return to an operational state.
    # while(!ReadETHReg(ESTAT).ESTATbits.CLKRDY)

    time.sleep(1)

    #Enable packet reception
    self.BFSReg(self.ECON1, self.ECON1_RXEN)

  def close_spi(self):
    self.spi.close()
