if (django) $ = jQuery = django.jQuery;

wymeditor_filebrowser = function(wym, wdw) {
  // the URL to the Django filebrowser, depends on your URLconf
  var fb_url = '/admin/filebrowser/browse/';
  
  var dlg = jQuery(wdw.document.body);
  if (dlg.hasClass('wym_dialog_image')) {
    // this is an image dialog
    dlg.find('.wym_src').css('width', '200px').attr('id', 'filebrowser')
      .after('<a id="fb_link" title="Filebrowser" href="#">Filebrowser</a>');
    dlg.find('fieldset')
      .append('<a id="link_filebrowser"><img id="image_filebrowser" /></a>' +
              '<br /><span id="help_filebrowser"></span>');
    dlg.find('#fb_link')
      .click(function() {
        fb_window = wdw.open(fb_url + '?pop=1', 'filebrowser', 'height=600,width=840,resizable=yes,scrollbars=yes');
        fb_window.focus();
        return false;
      });
  }
}

$(document).ready(function(){
    $('textarea').wymeditor({
        //'updateSelector': 'input:submit',
        'updateSelector': '.submit-row input[type=submit]',
        'updateEvent': 'click',
        'skin': 'default',
        'lang': 'ru',
        'plugins': ['embed'],
        'postInitDialog': wymeditor_filebrowser,
        'editorStyles': [
    	    {'name': '.text-center', 'css': 'text-align:center;'}
	],
        'classesItems': [
    	    {'name': 'text-center', 'title': 'По центру', 'expr': 'p'}
        ]
    });
});
