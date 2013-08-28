function TrialBalance(data) {

    var self = this;

    self.root_nodes = [];

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        self.root_nodes.push(item.id);
        return new CategoryViewModel(item);
    }));

    self.expandRoot = function () {
        for (var k in self.root_nodes) {
            $('.tree-table').treetable('expandNode', self.root_nodes[k]);
        }
    }

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