function SetFliper() {
    AbstractFliper.apply(this);
    // Keep parent reference
    var parent = {
        bind: this.bind
    };
    // Public
    this.dom = {
        // To read/write this from outsite, use dom() function
        button: {
            play: $('#btn-play'),
            flip: $('#btn-flip'),
            right: $('#btn-right')
        },
        block: {
            front: $('#block-front'),
            back: $('#block-back')
        },
        progress: $('#progress'), 
        count: {
            right: $('#btn-right .badge'),
            remainant: $('#btn-play .badge')
        }
    };
    this.bind = function() {
        parent.bind.apply(this);
        this.dom.button.play.click(this.display);
        this.dom.button.flip.click(this.flip);
        this.dom.button.right.click(this.right);
    }
    this.listen = function() {
        $(this).on('display', function(event, word, n) {
            this.dom.count.remainant.html(n);
            this.dom.block.back.html('');
            this.dom.block.front.text(word ? word : 'The end.');
        });
        $(this).on('right', function(event, n) {
            this.dom.count.right.html(n);
        });
        $(this).on('error', function(event) {
           this.display(); 
        });
    }
}