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

function CategoryViewModel(data) {

    var self = this;


    self.id = data.id;
    self.name = data.name;

    self.accounts = ko.observableArray(ko.utils.arrayMap(data.accounts, function (item) {
        return new AccountViewModel(item);
    }));

    self.categories = ko.observableArray(ko.utils.arrayMap(data.children, function (item) {
        return new CategoryViewModel(item);
    }));


}

function AccountViewModel(data) {
    var self = this;
    self.id = data.id;
    self.code = data.code;
    self.name = data.name;
    self.current_balance = data.current_balance;
}