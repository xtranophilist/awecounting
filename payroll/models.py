from django.db import models
from ledger.models import Account
from users.models import Company


class Entry(models.Model):
    entry_no = models.CharField(max_length=10)
    company = models.ForeignKey(Company)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return '/payroll/' + str(self.id)


class EntryRow(models.Model):
    sn = models.IntegerField()
    employee = models.ForeignKey(Account)
    pay_heading = models.ForeignKey(Account, related_name='row')
    amount = models.FloatField()
    hours = models.FloatField()
    tax = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entry = models.ForeignKey(Entry, related_name='rows')

    def get_absolute_url(self):
        return self.entry.get_absolute_url()


class Employee(models.Model):
    name = models.CharField(max_length=254)
    address = models.TextField(null=True, blank=True)
    tax_id = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    account = models.OneToOneField(Account)
    company = models.ForeignKey(Company)

    def save(self, *args, **kwargs):
        if self.pk is None:
            dummy_account = Account.objects.all()[:1][0]
            self.account = dummy_account
            super(Employee, self).save(*args, **kwargs)
            account = Account(code='13-0001-' + str(self.id), name=self.name)
            account.company = self.company
            account.add_category('Indirect Expenses')
            account.save()
            self.account = account
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AttendanceVoucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    employee = models.ForeignKey(Employee)
    from_date = models.DateField()
    to_date = models.DateField()
    total_working_days = models.FloatField(null=True, blank=True)
    full_present_day = models.FloatField(null=True, blank=True)
    half_present_day = models.FloatField(null=True, blank=True)
    half_multiplier = models.FloatField(default=0.5, null=True, blank=True)
    early_late_attendance_day = models.FloatField(null=True, blank=True)
    early_late_multiplier = models.FloatField(default=1, null=True, blank=True)
    total_ot_hours = models.FloatField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    #statuses = [('Approved', 'Approved'), ('Unapproved', 'Unapproved')]
    #status = models.CharField(max_length=10, choices=statuses, default='Unapproved')
    company = models.ForeignKey(Company)


class WorkTimeVoucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    company = models.ForeignKey(Company)


class WorkTimeVoucherRow(models.Model):
    employee = models.ForeignKey(Employee)
    work_time_voucher = models.ForeignKey(WorkTimeVoucher, related_name='rows')


class WorkDay(models.Model):
    in_time = models.TimeField()
    out_time = models.TimeField()
    work_time_voucher_row = models.ForeignKey(WorkTimeVoucherRow, related_name='work_days')
    day = models.DateField()
