$(function(){
      
  $('.tree_holder').each(function(index, el){
    $(el).fancytree({
      lazyLoad: get_tree_data
    });
  });
  
  window.setInterval(update_breadcrumbs,10000);
  
  
  
});

