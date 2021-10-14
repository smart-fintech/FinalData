from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import User,PpBnkM,PpOrgnM,PpPayeeM,Filleupload,PpPymntT,masterBank,pp_path_m,pp_bankcrd_m,term_condition,BalancesheetData
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


# serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # email=serializers.CharField(max_length=68,min_length=6,write_only=True)    

    default_error_messages = {
        'email': 'The email should  be valid'}

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile',
                  'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        # username = attrs.get('username', '')

        if email.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # email=serializers.CharField(max_length=68,min_length=6,write_only=True)

    default_error_messages = {
        'email': 'The email should  be valid'}

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile',
                  'password', 'type', 'is_delete', 'is_edit', 'is_views']

    def validate(self, attrs):
        email = attrs.get('email', '')
        # username = attrs.get('username', '')

        if email.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # username = serializers.CharField(
    # max_length=255, min_length=3, read_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            # 'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)




class admingetotheruserdataserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'




# serializer for email varification
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


# serializer for user login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # username = serializers.CharField(
        # max_length=255, min_length=3, read_only=True)
    # tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        print(user)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            # 'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


# serializer for user password reset
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

# serializer for user log out
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
 

class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalancesheetData
        fields = ['sheet','profitloss','trialbalance']





from rest_framework import serializers
# serializer for insert bank detail
class PpBnkMSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # entr_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = PpBnkM
        fields = ['bnk_id','usr','bnk_msg_type','bnk_msg_to','bnk_msg_frmt','actv_flg','entr_dt','ip_addr','mac_addr']

    def create(self, validated_data):
        return PpBnkM.objects.create(**validated_data)

class OrgSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # entr_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = PpOrgnM
        fields = ['orgn_id',
        'usr',
        'orgn_nm',
        'orgn_email',
        'orgn_mobile',
        'orgn_address',
        'orgn_website',
        'orgn_state',
        'orgn_gstin',
        'vat_no',
        'cst_no',
        'pan_no',
        'orgn_ex_nm',
        ]


    def create(self, validated_data):
        return PpOrgnM.objects.create(**validated_data)        



class PpeSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # entr_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = PpPayeeM
        fields = ['usr','payee_nm','payee_ac_no','ex_flg','ex_masterid','ex_vchr_typ','entr_dt','ip_addr','mac_addr']

    def create(self, validated_data):
        return PpPayeeM.objects.create(**validated_data)


class Geeks(object): 
    def __init__(self, integers): 
        self.integers = integers 

class FileSerializer(serializers.Serializer):
    integers = serializers.ListField( 
    child = serializers.IntegerField(min_value = 0, max_value = 100) 
    )
    class Meta:
        model = Filleupload
        fields = ['filedata']

        def create(self, validated_data):
            return Filleupload.objects.create(**validated_data)


class PpeSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # entr_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = PpPayeeM
        fields = ['usr','payee_nm','payee_ac_no','ex_flg','ex_masterid','ex_vchr_typ','entr_dt','ip_addr','mac_addr']

    def create(self, validated_data):
       return PpPayeeM.objects.create(**validated_data)

# masterbank_id  mstbnk_nm

class PpPymntTSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    pymnt_nm=serializers.CharField(source='pymnt_nm.ledeger_name')
    orgn=serializers.CharField(source='orgn.orgn_nm')
    bnk_id=serializers.CharField(source='bnk_id.masterbank_id')
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
        'PYMENT_CHQ_NO',
        'narration',]
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)
    # class Meta:
    #     model=PpPymntT
    #     fields="__all__"

class paymentbanklist(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
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
        'bnk_nm',
        'pymnt_sts',
        'priented_imag',
        # 'message_type',
        # 'message_to',
        'narration']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)


class OrgListSerializer(serializers.ModelSerializer):
    orgn_nm=serializers.CharField(source='orgn_nm.comp_name')
    class Meta:
        model = PpOrgnM
        fields = '__all__'

    def create(self, validated_data):
        return PpOrgnM.objects.create(**validated_data)        

class BnkListSerializer(serializers.ModelSerializer):
    mstbnk_nm=serializers.CharField(source='masterbank_id.mstbnk_nm')
    class Meta:
        model = PpBnkM
        fields = ['masterbank_id','mstbnk_nm']

    def create(self, validated_data):
        return PpBnkM.objects.create(**validated_data)


# vdds.pythonanywhere.com
# function for serialize all data and getting data by theid 
class masterbankSerializer(serializers.ModelSerializer):
    # orgn_nm = serializers.CharField(source='orgn_id.orgn_nm')
    # mstbnk_nm=serializers.CharField(source='masterbank_id.mstbnk_nm')
    class Meta:
        model = PpBnkM
        fields = ['bnk_id','masterbank_id','orgn_id','account_no','ifsc_code','bnk_msg_to','cover']

    def create(self, validated_data):
        return PpBnkM.objects.create(**validated_data)

class masterbankSerializer1(serializers.ModelSerializer):
   

    # orgn_nm = serializers.CharField(source='orgn_id.orgn_nm')
    # mstbnk_nm=serializers.CharField(source='masterbank_id.mstbnk_nm')
    class Meta:
        model = PpBnkM
        fields = ['bnk_id','masterbank_id','orgn_id','bnk_msg_to','cover']

            

   
# function for get all master data
class masterbanklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = masterBank
        fields = ['mstbnk_id','mstbnk_nm']

    def create(self, validated_data):
        return PpBnkM.objects.create(**validated_data)

# serializer for all get by id naame data 
class idnameSerializer(serializers.ModelSerializer):
    orgn_nm = serializers.CharField(source='orgn_id.orgn_nm')
    mstbnk_nm=serializers.CharField(source='masterbank_id.mstbnk_nm')
    class Meta:
        model = PpBnkM
        fields = ['bnk_id','masterbank_id','orgn_id','bnk_msg_to','orgn_nm','mstbnk_nm']

    def create(self, validated_data):
        return PpBnkM.objects.create(**validated_data)

# function for get all bank list data 
class blankimgSerializer(serializers.ModelSerializer):
    class Meta:
        model = pp_bankcrd_m
        fields = ['path_img_nm1','label','x1','y1','x2','y2']

    def create(self, validated_data):
       return pp_bankcrd_m.objects.create(**validated_data)

class termandconditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = term_condition
        fields = ['descreption','is_activate','created_by','created_at']

    def create(self, validated_data):
       return term_condition.objects.create(**validated_data)

#payment dashbord screen serializer
class paymentdsahSerializer(serializers.ModelSerializer):
    # usr = serializers.CharField(read_only=True)
    bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
    # entr_by = serializers.IntegerField(read_only=True)
    # pymnt_chq_dt=serializers.DateField(format="%d/%m/%Y", input_formats=['%d-%m-%Y',] )
    class Meta:
        model = PpPymntT
        fields = [
        'pymnt_id',
        'orgn',
        'bnk_nm',
        'pymnt_nm',
        'bnk_id',
        'pymnt_ac_no',
        'pymnt_chq_dt',
        'pymnt_chq_amt',
        'priented_imag',
        'PYMENT_CHQ_NO',
        'narration']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)
#payment dashbord blankchq payment screen
class blankchqprintscreenSerializer(serializers.ModelSerializer):
    # usr = serializers.CharField(read_only=True)
    bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
    # entr_by = serializers.IntegerField(read_only=True)
    # pymnt_chq_dt=serializers.DateField(format="%d/%m/%Y", input_formats=['%d-%m-%Y',] )
    class Meta:
        model = PpPymntT
        fields = [
        'pymnt_id',
        'orgn',
        'bnk_nm',
        'pymnt_nm',
        'bnk_id',
        'pymnt_ac_no',
        'pymnt_chq_dt',
        'pymnt_chq_amt']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)

#payment dashbord screen updatestatus serializer
class paymentdsahupdatestatusSerializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    # bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
    # entr_by = serializers.IntegerField(read_only=True)
    # pymnt_chq_dt=serializers.DateField(format="%d/%m/%Y", input_formats=['%d-%m-%Y',] )
    class Meta:
        model = PpPymntT
        fields = ['paymentactive_status','usr','PYMENT_CHQ_NO']
       
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)

class paid_model_serializer(serializers.ModelSerializer):
    usr = serializers.CharField(read_only=True)
    bnk_nm=serializers.CharField(source='bnk_id.masterbank_id')
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
        'bnk_nm',
        'pymnt_sts',
        'select_month',
        # 'message_to',
        'narration']
    def create(self, validated_data):
        return PpPymntT.objects.create(**validated_data)


class BlankPictureSerialiser(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = pp_path_m
        fields = ('path_img_nm', 'image_url')

    def get_image_url(self, obj):
        return obj.path_img_nm.url
