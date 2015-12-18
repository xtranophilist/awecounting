
```
./manage.py syncdb
```

Also, add a new superuser.


From admin panel, add role with a new company and new `SuperOwner` group.

Also, add a new Currency.

```
./manage.py shell
```

```
from users.models import Company, create_default
company = Company.objects.get()
create_default(company)
```

