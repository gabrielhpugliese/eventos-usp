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
    
var create_estrelas = function(qtdade){
  var div_estrelas = jQuery('<div id="estrelas"></div>'),
      gif_src = 'media/img/star.gif',
      flag = false;
  
  if (!qtdade){
    qtdade = 5;
    gif_src = 'media/img/star-empty.gif';
    flag = true;
  }
  
  
  for (var i = 0; i < qtdade; i++){
    var estrela = jQuery('<img class="star" src="'+gif_src+'" />');
  
    if (flag){
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
    }
    div_estrelas.append(estrela);
  }
  
  for (var i = 0; i < 5 - qtdade; i++){
    var estrela = jQuery('<img class="star" src="media/img/star-empty.gif" />');
    div_estrelas.append(estrela);
  }
  
  return div_estrelas;
};

var make_vote = function() {
  jQuery('#estrelas .star').click(function(){
    var link = jQuery(this).parent().parent().find('a').attr('href'),
        url = '/votar/',
        index = jQuery(this).index();
        
    jQuery(this).parent().find('img.star').unbind('hover');
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
    }).error(function(){
      console.log('error');
    });
  });
}

jQuery(document).ready(function(){
  set_style();
  
  jQuery('li').each(function(){
      var link = jQuery(this).find('a').attr('href'),
          url = '/pegar_nota/' + link.split('/?events=')[1] + '/',
          $this_li = jQuery(this);
      jQuery.get(url, function(data){
          $this_li.append(create_estrelas(data));
          if (!data)
            make_vote();
      });
  });
});