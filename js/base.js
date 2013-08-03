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

function TableViewModel(data, row_model, save_to_url){
    console.log(data);
    var self = this;
    for (var k in data)
        self[k]=data[k];

    self.rows = ko.observableArray(ko.utils.arrayMap(data.rows, function(item) {
        return new row_model(item);
    }));

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

    if (self.hasNoRows){
        self.addRow();
    }

    self._initial_rows = self.rows().slice(0);

    if (typeof(save_to_url) != 'undefined'){
        self.save = function(model, e){
            var el = get_target(e);
            el.on('mouseover', function() {
                el.html('Save');
            });
            el.html('Saving');
            $.ajax({
                type: "POST",
                url: save_to_url,
                data: ko.toJSON(self),
                success: function(msg){
                    el.html('Save');
                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    el.html("Saving Failed!");
                }
            });

        }
    }
    else{
        self.save= function(){
            throw new Error("'save_to_url' not passed to TableViewModel or save() not implemented!");
        }
    }

    self.reset= function(){
        self.rows(self._initial_rows);
    }
}