
from rest_framework import serializers
from e_checkapp.models import pp_path_m,PpPymntT




from rest_framework import serializers
from .models import Post
from e_checkapp .models import PpPymntT

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = Post
    fields = ['masterbankdata','cover']


class PpPymntTSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
    # entr_by = serializers.IntegerField(read_only=True)
    # pymnt_chq_dt=serializers.DateField(format="%d/%m/%Y", input_formats=['%d-%m-%Y',] )
    class Meta:
        model = PpPymntT
        fields = [
        'pymnt_id',
        'orgn',
        'pymnt_nm',
        'bnk_id',
        'usr',
        'pymnt_ac_no',
        'pymnt_chq_dt',
        'pymnt_chq_amt',
        'narration']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)


#printed check update with micker number, printed check image and other thinks

class printedcheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpPymntT
        fields = [
        # 'PYMNT_CHQ_MICR',
        # 'PYMNT_CHQ_ACCID',
        # 'PYMNT_CHQ_TRNSID',
        # 'PYMENT_CHQ_NO',
        'priented_imag'
        ]
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)
        
