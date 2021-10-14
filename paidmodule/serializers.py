from django.db.models.base import Model
from rest_framework import serializers
from e_checkapp.models import pp_path_m,PpPymntT
from .models import sailary


class paidpaymentbanklist(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
    # entr_by = serializers.IntegerField(read_only=True)
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
        # 'bnk_nm',
        # 'pymnt_sts',
        'select_month',
        # 'message_to',
        'narration']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        # model = PpPymntT
        fields = ('file',)

class Getsailarydata(serializers.ModelSerializer):
    class Meta:
        model = sailary
        fields = ['uer','x1','y1','x2','y2']
    def create(self, validated_data):
        return sailary.objects.create(**validated_data)
