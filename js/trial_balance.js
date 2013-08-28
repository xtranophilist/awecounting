function TrialBalance(data) {

    console.log(data);

    var self = this;

//    for (var k in data)
//        self[k] = data[k];

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        return new CategoryViewModel(item);
    }));

    console.log(self);

}

function CategoryViewModel(data, parent_id) {

    var self = this;


    self.id = data.id;
    self.name = data.name;
    self.code = '';
    self.parent_id = parent_id;
    self.cls = 'category';

    self.current_balance = function () {
        return 100;
    }

    self.dr_amount = function () {
        return self.current_balance();
    }

    self.cr_amount = function () {
        return self.current_balance();
    }

    self.accounts = ko.observableArray(ko.utils.arrayMap(data.accounts, function (item) {
        return new AccountViewModel(item, self.id);
    }));

    self.categories = ko.observableArray(ko.utils.arrayMap(data.children, function (item) {
        return new CategoryViewModel(item, self.id);
    }));


}

function AccountViewModel(data, parent_id) {
    var self = this;
    self.id = data.id;
    self.code = data.code;
    self.name = data.name;
    self.current_balance = data.current_balance;
    self.parent_id = parent_id;
    self.cls = 'account';

    self.dr_amount = function () {
        return self.current_balance;
    }

    self.cr_amount = function () {
        return self.current_balance;
    }

}