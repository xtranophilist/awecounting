function TrialBalance(data) {

    var self = this;

    self.root_nodes = [];

    self.categories = ko.observableArray(ko.utils.arrayMap(data.categories, function (item) {
        self.root_nodes.push(item.id);
        return new CategoryViewModel(item);
    }));

    self.expandRoot = function () {
        $('.tree-table').treetable('collapseAll');
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

    self.current_balance = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.current_balance))
                total += parseFloat(this.current_balance);
        });
        $.each(self.categories(), function () {
            if (isAN(this.current_balance()))
                total += parseFloat(this.current_balance());
        });
        return rnum(round2(total));
    }

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
        return round2(self.current_balance);
    }

    self.cr_amount = function () {
        return round2(self.current_balance);
    }

}