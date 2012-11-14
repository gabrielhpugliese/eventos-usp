var set_style = function(){
  var style;
  style = '<style type="text/css">\n';
  style += 'img.star{ cursor: pointer; }';
  style += '\n</style>';
  jQuery('head').append(style);
};

var preencher_estrelas = function($this, img, index){
    if (img == 'vazio'){
        img = 'media/img/star-empty.gif'
    } else {
        img = 'media/img/star.gif'
    }
    
    for(var j = 1; j < index + 1; j++){
      $this.parent().find('img:nth-child('+j+')').attr('src', img);   
    }
    $this.attr('src', img); 
}
    
var create_estrelas = function(){
  var div_estrelas = jQuery('<div id="estrelas"></div>');
  
  for (var i = 0; i < 5; i++){
    var estrela = jQuery('<img class="star" src="media/img/star-empty.gif" />');
  
    estrela.hover(
      function() {
        var index = jQuery(this).index();
        preencher_estrelas(jQuery(this), 'cheio', index);
      },
      function(){
        var index = jQuery(this).index();
        preencher_estrelas(jQuery(this), 'vazio', index);
      }
    );
    div_estrelas.append(estrela);
  }
  
  return div_estrelas;
};

var make_vote = function() {
  jQuery('#estrelas .star').click(function(){
    var link = jQuery(this).parent().parent().find('a').attr('href'),
        url = 'http://localhost:8080/votar/',
        index = jQuery(this).index();
        
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    jQuery.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader('X-CSRFToken', jQuery.cookie('csrftoken'));
        }
      }
    });
    
    url = url + link.split('/?events=')[1] + '/';
    jQuery.post(url, {'nota': index}, function(data){
      preencher_estrelas(jQuery(this), 'cheio', index);
      jQuery(this).parent().find('img.star').unbind('hover');
    }).error(function(){
      console.log('error');
    });
  });
}

jQuery(document).ready(function(){
  set_style();
  
  jQuery('li').append(create_estrelas());
  make_vote();
});