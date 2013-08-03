function InvoiceViewModel(data){

    var self = this;

    $.ajax({
      url: '/inventory/items/json/',
      dataType: 'json',
      async: false,
      success: function(data) {
        self.items = data;
      }
    });

    for (var k in data)
        self[k]=data[k];

    self.particulars = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
        return new ParticularViewModel(item);
    }));

    self.activate_ui = function(){

        // Typeahead
        var uber = {render: $.fn.typeahead.Constructor.prototype.render};
        $.extend($.fn.typeahead.Constructor.prototype, { render: function(items) { uber.render.call(this, items); this.$menu.prepend('<li class="nostyle"><a href="#item_new_form" class="btn" onclick="$(\'#item_new_form\').modal(\'show\')">Add a new item</a></li>'); return this; }});

        var fixHelper = function(e, ui) {
            ui.children().each(function() {
                $(this).width($(this).width());
            });
            return ui;
        };

        // Drag and sort
        var startIndex = -1;
        var sortable_setup = {
            helper: fixHelper,
            handle: '.drag_handle',
            start: function (event, ui) {
                // item index when the dragging starts
                startIndex = ui.item.index();
            },
            stop: function(event, ui){
                // get the new location item index
                var newIndex = ui.item.index();

                var prev_model = self.particulars()[startIndex];
                var curr_model = self.particulars()[newIndex];

                var prev_sn = prev_model.sn();
                var curr_sn = curr_model.sn();

                prev_model.sn(curr_sn);
                curr_model.sn(prev_sn);

                var particulars = self.particulars();
                var sorted_particulars = particulars.sort(function (a,b) {
                    if (a.sn() < b.sn())
                        return -1;
                    if (a.sn() > b.sn())
                        return 1;
                    return 0;
                });

                self.particulars([]);
                self.particulars(sorted_particulars);

            }
        };

        $(".table-sortable tbody").sortable(sortable_setup).disableSelection();
    }

    self.activate_ui();

    self.addParticular = function() {
        var new_item_index = self.particulars().length+1;
        self.particulars.push(new ParticularViewModel({ sn: new_item_index }));
    };
    self.removeParticular = function(particular) {
        for (var i = particular.sn(); i < self.particulars().length; i++) {
            self.particulars()[i].sn(self.particulars()[i].sn()-1);
        };
        self.particulars.remove(particular);
    };
    self.save = function(item, event){
        var el = get_target(event);
        el.html('Saving');
        $.post('/voucher/invoice/save/', ko.toJSON(self), function(){  el.html('Save'); });
    }

    self.grand_total = function(){
        var sum = 0;
        self.particulars().forEach(function(i){
            sum += i.amount();
        });
        return sum;
    }

    self.updateParticular = function(item, event){
        var key = $(event.currentTarget).data('selected');
        if(key){
            var selected_item = $.grep(self.items, function(e){ return e.id == key; })[0];
            var model = self.particulars()[item.sn()-1];
            model.description(selected_item.description);
            model.unit_price(selected_item.sales_price);
            model.item_name = selected_item.name;
        }
    }

}

function ParticularViewModel(particular){

    var self = this;
    //default values
    self.item_name = ko.observable('');
    self.description = ko.observable('');
    self.unit_price= ko.observable(0);
    self.quantity = ko.observable(1).extend({ numeric: 2 });
    self.discount = ko.observable(0).extend({ numeric: 2 });
    for(var k in particular)
        self[k] = ko.observable(particular[k]);

    self.amount = ko.computed(function(){
        var wo_discount = self.quantity() * self.unit_price();
        var amt = wo_discount - ((self.discount() * wo_discount)/100);
        return amt;
    });

    self.show_items = function(data, event){
        event.preventDefault();
        get_target(event).parent().find('.item-complete-box').trigger('focus').trigger('keyup');
    }
}

