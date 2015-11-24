$(function(){
  $('#proposal_selector').select2({
    placeholder: "Select an EUS Proposal..."
  });
  
  $("#instrument_selector").select2({
    data: [{id:0,text:""}],
    placeholder: "Select an Instrument..."
  });
  if(initial_proposal_id.length > 0){
    $('#proposal_selector').val(initial_proposal_id);
    get_instrument_list(initial_proposal_id);
  }
  
  $("#timeframe_selector").select2({
    placeholder: "Select a Time Frame..."
  });
  
  $('.criterion_selector').change(update_content);

  setup_tree_data();
  setup_metadata_disclosure();
  
  window.setInterval(check_cart_status, 30000);
  //window.setInterval(update_breadcrumbs,30000);
  window.setInterval(get_latest_transactions,60000);
  
});

