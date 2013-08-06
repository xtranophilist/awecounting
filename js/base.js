$(document).ready(function () {

    $('.collapsible-head').on('click', function(e) {
        e.preventDefault();
        var $this = $(this);
        var $collapse = $this.closest('.collapse-group').find('.collapse');
        $collapse.collapse('toggle');
    });

});


function get_target(e){
    return $((e.currentTarget) ? e.currentTarget : e.srcElement); //for IE <9 compatibility
}

$(document).on('mouseup mousedown', '[contenteditable]',function(){
    this.focus();
});

//setup ajax requests to include csrf token
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function TableViewModel(options, row_model){

    var self = this;

    if (typeof(options.properties)!='undefined'){
        /** @namespace options.properties */
        for (var k in options.properties)
            self[k]=options.properties[k];
    }

    self.message = ko.observable();

    self.rows = ko.observableArray(ko.utils.arrayMap(options.rows, function(item) {
        return new row_model(item);
    }));

    //if there are any rows
    if(self.rows().length){
        //if row has a sn() field, sort it
        if (self.rows()[0].sn()){
            self.rows().sort(function (l, r) {
                return l.sn() > r.sn() ? 1 : -1
            });
        }
    }

    self.hasNoRows = ko.computed(function(){
        return self.rows().length === 0;
    });

    self.addRow = function() {
        var new_item_index = self.rows().length+1;
        self.rows.push(new row_model());
    };

    self.removeRow = function(row) {
        self.rows.remove(row);
    };

    if (self.hasNoRows()){
        self.addRow();
    }

    self._initial_rows = self.rows().slice(0);

    if (typeof(options.save_to_url) != 'undefined'){
        self.save = function(model, e){
            var el = get_target(e);
            self.message('Saving...');
            console.log(self.rows());
            $.ajax({
                type: "POST",
                url: options.save_to_url,
                data: ko.toJSON(self),
                success: function(msg){
                    self.message('Saved!');
                    if (typeof(options.onSaveSuccess) != 'undefined'){
                        options.onSaveSuccess(msg, self.rows());
                    }

                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    self.message('Saving Failed!');
                }
            });

        }
    }
    else{
        self.save= function(){
            throw new Error("'save_to_url' option not passed to TableViewModel or save() not implemented!");
        }
    }

    self.reset= function(){
        self.rows(self._initial_rows);
    }
}