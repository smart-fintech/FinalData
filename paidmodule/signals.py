from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from e_checkapp.models import PpBnkM,PpOrgnM,User,PpPymntT
from .models import clonedata
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import *
from dateutil.rrule import *
from datetime import datetime

def save_pre(sender,instance,**kwargs):
    data=PpPymntT.objects.all()
    print(data)

post_save.connect(save_pre,sender=PpPymntT)     


@receiver(post_save,sender=PpPymntT)
def prof(sender,instance,created,**kwargrs):
    if created:
        data=PpPymntT.objects.latest('pymnt_id')
        use_date=data.pymnt_chq_dt
        total_selectmonth=data.select_month
        use_date = use_date+relativedelta(months=-1)
        use_date = use_date+relativedelta(day=31)
        x = list(rrule(freq=MONTHLY, count=int(total_selectmonth), dtstart=use_date, bymonthday=(-1,)))
        #if user select a month
        if len(total_selectmonth) is not None:
            for i in x:
                savedata=clonedata.objects.create(bnk_id=instance)
                savedata.save()
                data=PpPymntT.objects.latest('pymnt_id')
                clonedata.objects.filter(pymnt_id=savedata.pymnt_id).update(payment_datefield=i)
        elif(total_selectmonth ==0):
            # if user not select month then this wxecute
            clonedata.objects.create(bnk_id=instance)
            print("done====") 
