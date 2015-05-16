__author__ = 'Tommy Ekh'

from azure.servicebus import *

class AzureTestQ:
    def SendMsg(self):


        bus_service = ServiceBusService(
        service_namespace='tomandlab',
#        shared_access_key_name='All',
#        shared_access_key_value='KnSJV2mW7DXJOTkxZZob8x8HGuDSvOnLUftPTrzQD4E=')
        shared_access_key_name='RootManageSharedAccessKey',
        shared_access_key_value='v7su/w9CbM9tNCJaiXmVxPI6MbvooAuyFFACj9aKICM=')

        queues=bus_service.list_queues()
        #bus_service.create_queue('taskqueue')
        msg = Message(b'Test Message')
        bus_service.send_queue_message('taskqueue', msg)

        msg = bus_service.receive_queue_message('taskqueue', peek_lock=False)
        print(msg.body)

        #This code is for initiating the AMQP messenger
        #Primary key for All: KnSJV2mW7DXJOTkxZZob8x8HGuDSvOnLUftPTrzQD4E=
        #Secondary key for All: WMTLNgI5jntx717rbx13nuilOdDoF7zz6SugPHsIJ/Q=
        #ConnStr: Endpoint=sb://tomandlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=v7su/w9CbM9tNCJaiXmVxPI6MbvooAuyFFACj9aKICM=
        #amqpmng = proton.Messenger()

