__author__ = 'tommy'

import telldusCtrl

print 'Hej'

tlds=telldusCtrl.TelldusCtrl()

print 'Devs'
print tlds.devs

print 'Get dev for NightLamp'
dev=tlds.devs.get('NightLamp')

print dev

print 'Shut off ' + dev.name
tlds.turn_off(dev)
