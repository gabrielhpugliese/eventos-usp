var STAR_EMPTY_SRC = 'media/img/star-empty.gif', 
    STAR_EMPTY_IMG = '<img class="star" src="' + STAR_EMPTY_SRC + '" />', 
    STAR_SRC = 'media/img/star.gif', 
    STAR_IMG = '<img class="star" src="' + STAR_SRC + '" />';

var set_style = function() {
    var style;
    style = '<style type="text/css">\n';
    style += 'img.star{ cursor: pointer; }';
    style += '\n</style>';
    jQuery('head').append(style);
};

var fill_stars = function($this, img, index) {
    var star_src = img == 'empty' ? STAR_EMPTY_SRC : STAR_SRC;
    for (var j = 1; j < index + 2; j++) {
        $this.parent().find('img:nth-child(' + j + ')').attr('src', star_src);
    }
}
var create_stars = function(quantity) {
    var $div_stars = jQuery('<div id="stars"></div>'), 
        gif_img = STAR_IMG,  
        enable_hover = false;

    if (!quantity) {
        quantity = 5;
        gif_img = STAR_EMPTY_IMG;
        enable_hover = true;
    }

    for (var i = 0; i < quantity; i++) {
        var $star_img = jQuery(gif_img);

        if (enable_hover) {
            $star_img.hover(function() {
                var $self = jQuery(this),
                    index = $self.index();
                fill_stars($self, 'full', index);
            }, function() {
                var $self = jQuery(this),
                    index = $self.index();
                fill_stars($self, 'empty', index);
            });
        }
        $div_stars.append($star_img);
    }

    for (var i = 0; i < 5 - quantity; i++) {
        var $star_img = jQuery(STAR_EMPTY_IMG);
        $div_stars.append($star_img);
    }

    return $div_stars;
};

var enable_click_for_vote = function($this_li) {
    $this_li.find('.star').click(function() {
        var $self = jQuery(this),
            link = $self.parent().parent().find('a').attr('href'), 
            url = '/vote/' + link.split('/?events=')[1] + '/', 
            index = $self.index();


        jQuery.post(url, {
            'grade' : index
        }, function(data) {
            $self.parent().find('img.star').unbind('hover');
            fill_stars($self, 'fill', index);
        });
    });
}

