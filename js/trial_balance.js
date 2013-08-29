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
    };

    self.dr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.dr()))
                total += parseFloat(this.dr());
        });
        return rnum(round2(total));
    };

    self.cr_total = function () {
        var total = 0;
        $.each(self.categories(), function () {
            if (isAN(this.cr()))
                total += parseFloat(this.cr());
        });
        return rnum(round2(total));
    };

    self.balanced = function () {
        return self.cr_total() == self.dr_total();
    };


}

function CategoryViewModel(data, parent_id) {

    var self = this;

    self.id = data.id;
    self.name = data.name;
    self.code = '';
    self.parent_id = parent_id;
    self.cls = 'category';

    self.accounts = ko.observableArray(ko.utils.arrayMap(data.accounts, function (item) {
        return new AccountViewModel(item, self.id);
    }));

    self.categories = ko.observableArray(ko.utils.arrayMap(data.children, function (item) {
        return new CategoryViewModel(item, self.id);
    }));

    self.dr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.dr()))
                total += parseFloat(this.dr());
        });
        $.each(self.categories(), function () {
            if (isAN(this.dr()))
                total += parseFloat(this.dr());
        });
        return rnum(round2(total));
    }

    self.cr = function () {
        var total = 0;
        $.each(self.accounts(), function () {
            if (isAN(this.cr()))
                total += parseFloat(this.cr());
        });
        $.each(self.categories(), function () {
            if (isAN(this.cr()))
                total += parseFloat(this.cr());
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
    self.cr = ko.observable(data.cr);
    self.dr = ko.observable(data.dr);

}