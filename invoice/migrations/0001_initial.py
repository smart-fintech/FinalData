# Generated by Django 3.0 on 2021-12-02 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tallyapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_name', models.CharField(blank=True, max_length=40, null=True)),
                ('buyer_phone', models.CharField(blank=True, max_length=12, null=True)),
                ('buyer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('buyer_address', models.TextField(blank=True, null=True)),
                ('buyer_website', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer_state', models.CharField(blank=True, max_length=40, null=True)),
                ('buyer_gstin', models.CharField(blank=True, max_length=40, null=True)),
                ('created_by', models.CharField(blank=True, max_length=40, null=True)),
                ('buyer_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tallyapp.ladgernamedata')),
            ],
        ),
        migrations.CreateModel(
            name='CSVInvoiceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='recieveinvoice/')),
                ('created_by', models.CharField(blank=True, max_length=30, null=True)),
                ('companyname', models.CharField(blank=True, max_length=80, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=800, null=True)),
                ('subtotal', models.FloatField(blank=True, max_length=70, null=True)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('CGST', models.CharField(blank=True, max_length=700, null=True)),
                ('SGST', models.CharField(blank=True, max_length=700, null=True)),
                ('IGST', models.CharField(blank=True, max_length=700, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('StateCode', models.CharField(blank=True, max_length=10, null=True)),
                ('Company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tallyapp.companydata')),
            ],
            options={
                'unique_together': {('invoice_no', 'invoice_date')},
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Invoice_no', models.CharField(blank=True, max_length=20, null=True)),
                ('Invoice_date', models.DateField(blank=True, null=True)),
                ('P_O_no', models.CharField(blank=True, max_length=30, null=True)),
                ('P_O_date', models.DateField(blank=True, null=True)),
                ('Terms_of_payment', models.CharField(blank=True, max_length=30, null=True)),
                ('Reference_no', models.CharField(blank=True, max_length=100, null=True)),
                ('Delievry_note', models.CharField(blank=True, max_length=100, null=True)),
                ('Total', models.FloatField(blank=True, max_length=40, null=True)),
                ('Packageing', models.IntegerField(blank=True, null=True)),
                ('Insurance', models.IntegerField(blank=True, null=True)),
                ('Frieght', models.IntegerField(blank=True, null=True)),
                ('Others', models.IntegerField(blank=True, null=True)),
                ('CGSTPackageing', models.FloatField(blank=True, null=True)),
                ('CGSTInsurance', models.FloatField(blank=True, null=True)),
                ('CGSTFrieght', models.FloatField(blank=True, null=True)),
                ('CGSTOthers', models.FloatField(blank=True, null=True)),
                ('SGSTPackageing', models.FloatField(blank=True, null=True)),
                ('SGSTInsurance', models.FloatField(blank=True, null=True)),
                ('SGSTFrieght', models.FloatField(blank=True, null=True)),
                ('SGSTOthers', models.FloatField(blank=True, null=True)),
                ('IGSTPackageing', models.FloatField(blank=True, null=True)),
                ('IGSTInsurance', models.FloatField(blank=True, null=True)),
                ('IGSTFrieght', models.FloatField(blank=True, null=True)),
                ('IGSTOthers', models.FloatField(blank=True, null=True)),
                ('Roundoff', models.FloatField(blank=True, max_length=40, null=True)),
                ('GSTTotal', models.FloatField(blank=True, max_length=40, null=True)),
                ('IRN', models.CharField(blank=True, max_length=200, null=True)),
                ('Ack_No', models.CharField(blank=True, max_length=200, null=True)),
                ('Ack_Date', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.CharField(blank=True, max_length=40, null=True)),
                ('Buyer_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.BuyerData')),
            ],
        ),
        migrations.CreateModel(
            name='Uploadcsv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hsn_code', models.CharField(blank=True, max_length=20, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('CGst_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('SGst_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('IGst_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('Per', models.CharField(blank=True, max_length=30, null=True)),
                ('Rate', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherInvoiceEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=30, null=True)),
                ('Voucher_date', models.DateField(blank=True, null=True)),
                ('legdername', models.CharField(blank=True, max_length=50, null=True)),
                ('Voucher_type', models.CharField(blank=True, max_length=50, null=True)),
                ('Voucher_amount_cr', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('Voucher_amount_dr', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('Narration', models.TextField(blank=True, null=True)),
                ('CGSTlegderdata', models.CharField(blank=True, max_length=50, null=True)),
                ('CGSTlegderamount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('SGSTlegderdata', models.CharField(blank=True, max_length=50, null=True)),
                ('SGSTlegderamount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('IGSTlegderdata', models.CharField(blank=True, max_length=50, null=True)),
                ('IGSTlegderamount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('Vouchetype', models.CharField(blank=True, choices=[('DEBIT NOTE VOUCHER', 'DEBIT NOTE VOUCHER'), ('JOURNAL VOUCHER', 'JOURNAL VOUCHER'), ('CREDIT NOTE VOUCHER', 'CREDIT NOTE VOUCHER'), ('PURCHASE VOUCHER', 'PURCHASE VOUCHER'), ('SALES VOUCHER', 'SALES VOUCHER'), ('RECEIPT VOUCHER', 'RECEIPT VOUCHER'), ('PAYMENT VOUCHER', 'PAYMENT VOUCHER'), ('CONTRA VOUCHER', 'CONTRA VOUCHER')], max_length=100, null=True)),
                ('is_verified', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SellerData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_name', models.CharField(blank=True, max_length=40, null=True)),
                ('seller_phone', models.CharField(blank=True, max_length=12, null=True)),
                ('seller_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('seller_address', models.TextField(blank=True, null=True)),
                ('seller_website', models.CharField(blank=True, max_length=100, null=True)),
                ('seller_state', models.CharField(blank=True, max_length=40, null=True)),
                ('seller_gstin', models.CharField(blank=True, max_length=40, null=True)),
                ('created_by', models.CharField(blank=True, max_length=40, null=True)),
                ('seller_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tallyapp.companydata')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Products', models.TextField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('Amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('CGST', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('SGST', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('IGST', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('Hsn_code', models.CharField(blank=True, max_length=20, null=True)),
                ('Rate', models.CharField(blank=True, max_length=20, null=True)),
                ('Per', models.CharField(blank=True, max_length=40, null=True)),
                ('created_by', models.CharField(blank=True, max_length=40, null=True)),
                ('HSN_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='invoice.Uploadcsv')),
                ('Invoice_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice')),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='Seller_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.SellerData'),
        ),
        migrations.CreateModel(
            name='CSvTableData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Products', models.TextField(blank=True, null=True)),
                ('HSN_SAC', models.CharField(blank=True, max_length=20, null=True)),
                ('GST_rate', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('Rate', models.CharField(blank=True, max_length=100, null=True)),
                ('Per', models.CharField(blank=True, max_length=100, null=True)),
                ('Discount', models.CharField(blank=True, max_length=100, null=True)),
                ('Amount', models.CharField(blank=True, max_length=40, null=True)),
                ('Invoice_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.CSVInvoiceData')),
            ],
        ),
    ]
