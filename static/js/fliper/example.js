function ExampleFliper() {
    SetFliper.apply(this);
    // Override list
    var parent = {
        listen: this.listen
    };
    var self = this;
    this.example = [];
    var question_tmpl = _.template('<li data-id="<%= id %>"><%= sentence %></li>');
    var answer_tmpl = _.template('<li data-id="<%= id %>"><%= translation %></li>');
    this.render = function(using) {
        var q = $('<ul><ul>');
        var item;
        for (var i in this.example) {
            item = _.object(['id', 'sentence', 'translation'], this.example[i]);
            q.append(using(item));
        }
        return q;
    }
    // Public
    this.listen = function() {
        parent.listen.apply(this);
        $(self).on('display', function(event, word, n) {
            $.get('/api/example/' + word, this.callback);
        });
        $(self).on('callback', function(event, response) {
            this.example = response.example;
            var el = self.render(question_tmpl);
            self.dom.block.front.html('').append(el);
        });
        $(self).on('flip', function(event) {
            var el = self.render(answer_tmpl);
            self.dom.block.back.html('').append(el);
        });
    }
}