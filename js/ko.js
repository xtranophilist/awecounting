function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}


function InvoiceModel(invoice){
    var self = this;
    self.particulars = ko.observableArray(ko.utils.arrayMap(activities, function(item) {
        return new ParticularModel(item);
    }));
}

function ParticularModel(particuar){
    var self = this;
    for(var k in particular)
        self[k]=particular[k];
}
