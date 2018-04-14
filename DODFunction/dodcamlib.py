from . import utilidades
import firebase_admin
from firebase_admin import credentials, db
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

cred = credentials.Certificate('c.json')
default_app = firebase_admin.initialize_app(cred, {'databaseURL':  'https://pushtest-231c6.firebaseio.com/'})
root = db.reference()

DEATH_TIME = 10
PASSANTE_TRESHOLD = 6
def start_routine(func):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=func,
        trigger=IntervalTrigger(seconds=5),
        id='coletor_de_memoria',
        name='Limpa os dados em memoria enviados pelo servidor',
        replace_existing=True)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

class Singleton(type):
   _instances = {}
   def __call__(cls, *args, **kwargs):
       if cls not in cls._instances:
           cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
       return cls._instances[cls]


class DodCamLib:
    def __init__(self):
        self.list = []
        start_routine(self.clear_mm)

    def register_event(self, form):
        to_append = self.format_form(form)
        #print("ENTRADA REGISTRADA")
        self.list.append(to_append)

        if len(self.list) > 150:
            self.clear_mm()

    def clear_list(self):   #TODO Criar uma metrica para limpar possiveis falhas na inteligencia( E.g.: 'Pessoa' que aparece em so 1 frame, ou 'pessoa' que fica parada o tempo todo)
        for i in self.list:
            tmp = utilidades.get_timeNow() - i['created']
            if tmp.seconds > DEATH_TIME:
                i = None

    def clear_mm(self):
        #self.clear_list()
        if len(self.list) < 4:
            return
        #print("Fazendo upload para o Firebase")
        self.upload_to_firebase()
        #print("PRONTO")

    def raw_to_data(self, tmp):
        #print(tmp[len(tmp) - 1]['timestamp'], tmp[0]['timestamp'])
        timelapse = utilidades.get_timestring_to_mili(tmp[len(tmp) - 1]['timestamp']) - utilidades.get_timestring_to_mili(tmp[0]['timestamp'])
        sample = tmp[len(tmp) - 1]
        status = 'vitrine'
        ano, mes, diaMes, hora = sample['timestamp'].split('.')[:-3]
        semana = int(int(diaMes) / 7)
        diaSemana = utilidades.get_timestring_to_mili(sample['timestamp']).strftime("%A")
        if timelapse.seconds < PASSANTE_TRESHOLD:
            ret['status'] = 'passante'

        return {'frame_id': sample['frame_id'],
                'person_id': sample['person_id'],
                'algorithm_id': sample['algorithm_id'],
                'camera_id': sample['camera_id'],
                'area_id': sample['area_id'],
                'store_id': sample['store_id'],
                'ano': ano,
                'mes': mes,
                'dia': diaSemana,
                'hora': hora,
                'semana': semana,
                'status': status}

    def upload_to_firebase(self):
        #print("Entrando na funcao")
        if(len(self.list) <= 1):
            return
        tmp = [self.list.pop(0)]
        to_rmv = []
        cont = 0
        for i in self.list:
            if i['person_id'] == tmp[0]['person_id']:
                 tmp.append(i)
                 to_rmv.append(cont)
                 #print("REMOVENDO", cont, len(self.list))
            cont += 1
        to_rmv = sorted(to_rmv, reverse=True)
        for i in to_rmv:
            #print("POPPANDo", i)
            self.list.pop(i)
        to_upload = self.raw_to_data(sorted(tmp, key=lambda k: k['timestamp']))
        #print("Upando para o Firebase...")
        root.child(str(to_upload['store_id']) ).child(str(to_upload['ano']) ).child(str(to_upload['mes'])).child(str(to_upload['semana'])).child(str(to_upload['dia'])).child(str(to_upload['hora'])).child(str(to_upload['camera_id'])).child(utilidades.get_timeNow_str().replace(".", " - ") + str(to_upload['person_id']) ).update(to_upload)
        return self.upload_to_firebase()
    def format_form(self, form):
        ts = "" + str(form['timestamp'].year) +"." + str(form['timestamp'].month) + "." +str(form['timestamp'].day) + "." +str(form['timestamp'].hour) + "." +str(form['timestamp'].minute) + "." +str(form['timestamp'].second) + "." +str(form['timestamp'].microsecond)
        return {
        'frame_id': form['frame_id'],
        'person_id': form['person_id'],
        'algorithm_id': form['algorithm_id'],
        'camera_id': form['camera_id'],
        'area_id': form['area_id'],
        'store_id': form['store_id'],
        'created': utilidades.get_timeNow(),
        'timestamp': ts}
