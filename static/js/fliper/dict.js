function DictFliper() {
    SetFliper.apply(this);
    // Override list
    var parent = {
        bind: this.bind,
        listen: this.listen
    };
    var self = this;
    $('<button id="btn-exporter" type="button" class="btn btn-primary pull-right"> \
        <span class="glyphicon glyphicon-cloud-upload"></span> Export \
    </button>').insertAfter(this.dom.button.right);
    this.dom.button.exporter = $('#btn-exporter');
    this.dom.block.exporter = $('#board');
    // Public
    this.listen = function() {
        parent.listen.apply(this);
        $(this).on('display', function(event) {
        
        });
        $(this).on('flip', function(event) {
            $.get('/api/dict/' + this.displaying(), this.callback);
        });
        $(this).on('callback', function(event, response) {
            self.dom.block.back.html(
                '<writing>' + response.dict[0] + '</writing>' +
                '<reading>' + response.dict[1] + '</reading>' +
                response.dict[2]
            );
        });
        $(this).on('end', function() {
            
        });
    }
    this.exporter = function() {
        var text = '';
        var row = _.template("<%= writing %> (<%= reading %>) \t <%= brief %>");
        list = self.get_list();
        for (i in self.dom.button) {
            self.dom.button[i].hide();
        }
        while (true) {
            entry = list.pop();
            if (! entry) break;
            $.get('/api/dict/' + entry + '?brief=true', function(response) {
                text += row(response) + "\n";
                self.set_progress(list.length);
                if (list.length == 0) {
                    self.dom.block.exporter.html('<pre id="export-data">' + text + '</pre>');
                }
            });
        }
    }
    this.bind = function() {
        parent.bind.apply(this);
        this.dom.button.exporter.click(this.exporter);
    }
}