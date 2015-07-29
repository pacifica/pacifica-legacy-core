$(function(){
      
  // $('.tree_holder').each(function(index, el){
    // $(el).fancytree({
      // lazyLoad: get_tree_data
    // });
  // });
  setup_tree_data();
  setup_metadata_disclosure();
  var bc_interval = lookup_type == 'j' ? 1500 : 15000;
  window.setInterval(check_cart_status, 30000);
  window.setInterval(update_breadcrumbs, bc_interval);
  setup_hover_info();
});