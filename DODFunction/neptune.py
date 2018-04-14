
from deepsense import neptune

def send_to_neptune(id_num,confidence,frame_id):
        ctx = neptune.Context()
        ctx.channel_send('{}'.format('person id %d' % int(id_num),int(frame_id),float(confidence)))
