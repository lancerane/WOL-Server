from ENC28J60 import ENC28J60

eth = ENC28J60(bus=0, device=0)

#eth.power_down()
#print('Ethernet put to sleep')

eth.power_up()
print('Ethernet brought up')

eth.close_spi()
