function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

function InvoiceViewModel(data){
    var self = this;
    for (var k in data)
        self[k]=data[k]
    self.particulars = ko.observableArray(ko.utils.arrayMap(data.particulars, function(item) {
        return new ParticularViewModel(item);
    }));
    self.addParticular = function() {
        self.particulars.push({
            name: "",
            price: ""
        });
    };
    self.removeParticular = function(particular) {
        self.particulars.remove(particular);
    };
    self.save = function(){
        console.log(self);
    }


}

function ParticularViewModel(particular){
    var self = this;
    for(var k in particular)
        self[k] = particular[k];
}