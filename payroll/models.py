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

    def get_unpaid_days(self):
        total = 0
        attendance_vouchers = AttendanceVoucher.objects.filter(employee=self, paid=False)
        for voucher in attendance_vouchers:
            total += voucher.total_present_days()
        return total

    def get_unpaid_hours(self):
        total = 0
        work_time_voucher_rows = WorkTimeVoucherRow.objects.filter(employee=self, paid=False)
        for row in work_time_voucher_rows:
            for work_day in row.work_days.all():
                total += work_day.work_minutes()
        return round(float(total) / 60, 2)

    def get_unpaid_ot_hours(self):
        total = 0
        attendance_vouchers = AttendanceVoucher.objects.filter(employee=self, paid=False)
        for voucher in attendance_vouchers:
            total += voucher.total_ot_hours
        return total

    def save(self, *args, **kwargs):
        if self.pk is None:
            dummy_account = Account.objects.all()[:1][0]
            self.account = dummy_account
            super(Employee, self).save(*args, **kwargs)
            account = Account(code='13-0001-' + str(self.id), name=self.name)
            account.company = self.company
            account.add_category('Employee')
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

    def total_present_days(self):
        return self.full_present_day + self.half_present_day * self.half_multiplier + self.early_late_attendance_day * self.early_late_multiplier


class WorkTimeVoucher(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    company = models.ForeignKey(Company)


class WorkTimeVoucherRow(models.Model):
    employee = models.ForeignKey(Employee)
    paid = models.BooleanField(default=False)
    work_time_voucher = models.ForeignKey(WorkTimeVoucher, related_name='rows')


class WorkDay(models.Model):
    in_time = models.TimeField()
    out_time = models.TimeField()
    work_time_voucher_row = models.ForeignKey(WorkTimeVoucherRow, related_name='work_days')
    day = models.DateField()

    def get_in_time(self):
        hms = str(self.in_time)
        pieces = hms.split(':')
        hm = pieces[0] + ':' + pieces[1]
        return hm

    def get_out_time(self):
        hms = str(self.out_time)
        pieces = hms.split(':')
        hm = pieces[0] + ':' + pieces[1]
        return hm

    def work_minutes(self):
        return (self.out_time.hour - self.in_time.hour) * 60 + self.out_time.minute - self.in_time.minute


class GroupPayroll(models.Model):
    voucher_no = models.CharField(max_length=50)
    date = models.DateField()
    company = models.ForeignKey(Company)


class GroupPayrollRow(models.Model):
    employee = models.ForeignKey(Employee)
    rate_day = models.FloatField()
    rate_hour = models.FloatField()
    rate_ot_hour = models.FloatField()
    payroll_tax = models.FloatField()
    pay_head = models.ForeignKey(Account)
    group_payroll = models.ForeignKey(GroupPayroll, related_name='rows')
