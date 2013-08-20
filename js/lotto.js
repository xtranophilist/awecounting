function LottoDetailModel(data){
    var self = this;

    for (var k in data)
        self[k]=data[k];

    $.ajax({
        url: '/ledger/accounts/json',
        dataType: 'json',
        async: false,
        success: function(data) {
            self.accounts = data;
        }
    });

    self.accounts_by_tag = function(tags, is_or){
        var filtered_accounts = [];
        for (var i in self.accounts){
            var account_tags = self.accounts[i].tags
            if( typeof tags === 'string' ) {
                if ($.inArray(tags, account_tags) !== -1){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else if(typeof is_or != 'undefined'){
                if (intersection(tags, account_tags).length){
                    filtered_accounts.push(self.accounts[i]);
                }
            }else{
                if (compare_arrays(tags, account_tags)){
                    filtered_accounts.push(self.accounts[i]);
                }
            }
        }
        return filtered_accounts;
    };

    var validate = function(msg, rows, tr_wrapper_id){
        var selection = $("#" + tr_wrapper_id + " > tr");
        selection.each(function (index) {
            $(selection[index]).addClass('invalid-row');
        });
        for (var i in msg['saved']){
            rows[i].id = msg['saved'][''+i+''];
            $(selection[i]).removeClass('invalid-row');
        }
        var model = self[tr_wrapper_id.toUnderscore()];
        var saved_size = Object.size(msg['saved']) ;
        if(saved_size==rows.length)
            model.message('Saved!');
        else if(saved_size==0){
            model.message('No rows saved!');
            model.status('error');
        }
        else if(saved_size<rows.length){
            var message = saved_size.toString() +' row' + ((saved_size==1)?'':'s') + ' saved! ';
            message += (rows.length-saved_size).toString() +' row' + ((rows.length-saved_size==1)?' is':'s are') + ' incomplete!';
            model.message(message);
            model.status('error');
        }
    }

    var key_to_options = function(key){
        return {
            rows: data['rows'],
            save_to_url : '/payroll/save/',
            properties : {id : self.id},
            onSaveSuccess : function(msg, rows){
                validate(msg, rows, key.toDash());
            }
        };
    }

    self.lotto_detail = new TableViewModel(key_to_options('lotto_detail'), LottoDetailRow);

}



function LottoDetailRow(row){
    var self = this;

    self.type = ko.observable();
    self.rate = ko.observable()
    self.opening = ko.observable();
    self.purchase_pack = ko.observable();
    self.purchase_quantity = ko.observable();
    self.purchase_total = ko.observable();
    self.purchase_amount = ko.observable();
    self.total = ko.observable();
    self.sold_quantity = ko.observable();
    self.sold_amount = ko.observable();
    self.closing_quantity = ko.observable();
    self.closing_amount = ko.observable();
    self.actual_quantity = ko.observable();
    self.actual_amount = ko.observable();
    self.difference_quantity = ko.observable();
    self.difference_amount = ko.observable();

    for (var k in row){
        self[k] = ko.observable(row[k]);
    }

}

