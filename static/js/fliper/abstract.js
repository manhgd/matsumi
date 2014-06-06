function AbstractFliper() {
    // Private
    var _list = [],
        queue = false,
        total = 0,
        count_right = 0
        displaying = false,
        
        self = this;
    // Public
    this.set_list = function(list) {
        _list = list;
        total = _list.length;
    }
    this.get_list = function() {
        return _.shuffle(_list);
    }
    this.set_progress = function(remain) {
        percent = 100*(1 - remain / total);
        self.dom.progress.attr('aria-valuenow', percent).css('width', percent + '%');
    }
    this.display = function() {
        if (queue === false) {
            queue = self.get_list();
        }
        word = queue.pop();
        displaying = word;
        var num_left = queue.length;
        self.set_progress(num_left);
        if (word) {
            $(self).triggerHandler('display', [word, num_left]);
            return true;
        } else {
            var score = Math.round(100 * count_right / total) + '%';
            $(self).triggerHandler('end', [score]);
            return false;
        }
    }
    this.displaying = function() { return displaying; }
    this.flip = function() {
        if (displaying) {
            $(self).triggerHandler('flip');
            displaying = false;
        }
    }
    this.callback = function(response) {
        if (response.error) {
            displaying = false;
            $(self).triggerHandler('error');
            return;
        } else {
            $(self).triggerHandler('callback', [response]);
        }
    }
    this.right = function() {
        count_right++;
        $(self).triggerHandler('right', [count_right]);
        self.display();
    }
    this.on_keys = function() {
        if (displaying) {
            self.flip();
        } else {
            self.display();
        }
        return false;
    }
    this.bind = function() {
        $(document).bind('keydown', 'space', this.on_keys);
        $(document).bind('keydown', 'right', this.on_keys);
        $(document).bind('keydown', 'v', this.right);
        
        $(self).on('end', function(event, score) {
            $(document).unbind('keydown', this.right);
            $(document).unbind('keydown', this.on_keys);
            $.each(self.dom.button, function(k, v) {
                v.hide();
            });
            self.dom.block.back.html('');
            self.dom.block.front.html('You did it! Score: <span class="red">' +
                score + '</span><a class="btn btn-primary" href="javascript:location.reload()">Re-do this</a>'
            );
        });
    }
}