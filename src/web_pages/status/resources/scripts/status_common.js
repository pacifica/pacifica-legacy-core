var trans_id_list = {};
var latest_tx_id = 0;
var inst_id = 0;
var initial_load = true;

var spinner_opts = {
  lines: 9, // The number of lines to draw
  length: 4, // The length of each line
  width: 2, // The line thickness
  radius: 4, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#111', // #rgb or #rrggbb or array of colors
  speed: 1, // Rounds per second
  trail: 60, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: true, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '50%', // Top position relative to parent
  left: '50%' // Left position relative to parent
};




$(function(){
  inst_id = $('#instrument_selector').length > 0 ? $('#instrument_selector').val() : initial_inst_id;
});

var update_breadcrumbs = function(){
  inst_id = $('#instrument_selector').length > 0 ? $('#instrument_selector').val() : initial_inst_id;
  $('.bar_holder').each(function(index,el){
    var pattern = /\w+_\w+_(\d+)/i;
    var m = $(el).prop('id').match(pattern);
    var this_tx_id = parseInt(m[1],10);
    latest_tx_id = this_tx_id > latest_tx_id ? this_tx_id : latest_tx_id;
    if(!(this_tx_id in trans_id_list)){
      var hash = $(el).crypt({method:"sha1"});
      trans_id_list[this_tx_id] = hash;
    }
  });
  var data_obj = {
    'transaction_list' : trans_id_list,
    'instrument_id' : inst_id
  };
  if(inst_id && Object.keys(trans_id_list).length > 0){
    var ts = moment().format('YYYYMMDDHHmmss');
    var url = base_url + 'index.php/status/get_status/t/bc_' + ts;
    $.ajax({
      type: "POST",
      url: url,
      data: data_obj,
      success: function(data){
        if(data != 0){
          $.each(data, function(index,trans_entry){
            var new_item = $('#bar_holder_' + index);
            new_item.html(trans_entry);
            var hash = new_item.crypt({method:"sha1"});
            trans_id_list[index] = hash;
          });
        }
      },
      dataType: 'json'
    });
  }
  
};

var get_latest_transactions = function(){
  if(initial_instrument_id && latest_tx_id){
    var ts = moment().format('YYYYMMDDHHmmss');    
    var new_tx_url = base_url + 'index.php/status/get_latest_transactions/' + initial_instrument_id + '/' + initial_proposal_id + '/' + latest_tx_id + '/glt_' + ts;
    $.get(new_tx_url, function(data){
      if(data.length > 0){
        $('#item_info_container').prepend(data);
        setup_tree_data();
        setup_metadata_disclosure();
      }
    });  
  }
};

var update_content = function(event){
  var el = null;
  if(event != null){
    el = $(event.target);
    if(el.prop('id') == 'instrument_selector' && el.val() == initial_instrument_id && !initial_load){
      return false;
    }
    if(['proposal_selector','instrument_selector','timeframe_selector'].indexOf(el.prop('id')) >= 0){
      $.cookie('myemsl_status_last_' + el.prop('id'), el.val(),{ expires: 30, path: '/' });
    }
  }
  var proposal_id = $('#proposal_selector').select2('val').length > 0 ? $('#proposal_selector').select2('val') : initial_proposal_id;
  var instrument_id = $('#instrument_selector').select2('val').length > 0 ? $('#instrument_selector').select2('val') : initial_instrument_id;
  var time_frame = $('#timeframe_selector').select2('val').length > 0 ? $('#timeframe_selector').select2('val') : 0;
  var ts = moment().format('YYYYMMDDHHmmss');  
  var url = base_url + 'index.php/status/overview/' + proposal_id + '/' + instrument_id + '/' + time_frame + '/ovr_' + ts;
  if(proposal_id && instrument_id && time_frame){
    inital_load = false;
    $('#item_info_container').hide();
    $('#loading_status').fadeIn("slow", function(){
      var getting = $.get(url);
      getting.done(function(data){
        if(data){
          $('#loading_status').fadeOut(200,function(){
            $('#item_info_container').html(data);
            $('#item_info_container').fadeIn('slow',function(){
              setup_tree_data();
              setup_metadata_disclosure();
            });
          });
        }
      });
      getting.fail(function(jqxhr,textStatus,error){
        $('#loading_status').fadeOut(200,function(){
          $('#info_message_container h2').html("An Error occurred during refresh");
          $('#info_message_container').append("<span class='fineprint'>" + error + "</span>");
          $('#info_message_container').show();
        });
      });
    });
  }
  if(el && el.prop('id') == 'proposal_selector'){ 
    //check to see if instrument list is current
    if(el.val() != initial_proposal_id){
      get_instrument_list(el.val());
      initial_proposal_id = el.val();
    }
  }
  if(el){
    var identifier = el.prop('id').replace('_selector','');
    var initial_ident = 'initial_' + identifier + '_id';
    eval(initial_ident + ' = ' + el.val());
  }
};

var get_instrument_list = function(proposal_id){
  var inst_url = base_url + 'index.php/status/get_instrument_list/' + proposal_id;
  var target = document.getElementById('instrument_selector_spinner');
  var spinner = new Spinner(spinner_opts).spin(target);
  $.getJSON(inst_url,function(data){
    $('#instrument_selector').select2({
      data: data.items,
      placeholder: "Select an Instrument..."
    });
    $('#instrument_selector').enable();
    initial_instrument_list = [];
    
    $.each(data.items, function(index,item){
      initial_instrument_list.push(item.id);
    });
    // debugger;
    spinner.stop();
    if(initial_instrument_list.indexOf(parseInt(initial_instrument_id,10)) < 0){
      $('#instrument_selector').val('').trigger('change');
    }else{
      $('#instrument_selector').val(parseInt(initial_instrument_id,10)).trigger('change');
      update_content();
    }
  });
};

var setup_metadata_disclosure = function(){
  $('ul.metadata_container').hide();
  $('.disclosure_button').unbind('click').click(function(){
    var el = $(this);
    var container = el.parentsUntil('div').siblings('ul.metadata_container');
    if(el.hasClass('dc_up')){
      //view is rolled up and hidden
      el.removeClass('dc_up').addClass('dc_down');
      container.slideDown(200);
    }else if(el.hasClass('dc_down')){
      //view is open and visible
      el.removeClass('dc_down').addClass('dc_up');
      container.slideUp(200);

    }else{
      
    }
  });
  
};

var setup_tree_data = function(){
  $('.tree_holder').each(function(index, el){
    if($(el).find('ul.ui-fancytree').length == 0){
      var el_id = $(el).prop('id').replace('tree_','');
      $(el).fancytree(
        {
          checkbox:true,
          selectMode: 3,
          activate: function(event, data){
            
          },
          select: function(event, data){
            var dl_button = $(event.target).parent().find('#dl_button_container_' + el_id);
            var fileSizes = get_selected_files($(el));
            // var fileSizes = get_file_sizes($(el));
            var tree = $(el).fancytree('getTree');
            var totalSizeText = myemsl_size_format(fileSizes.total_size);
            var topNode = tree.getRootNode();
            var dataNode = topNode.children[0];
            var selectCount = Object.keys(fileSizes.sizes).length;
            
          },
          keydown: function(event, data){
            if(event.which === 32){
              data.node.toggleSelected();
              return false;
            }
          },
          lazyLoad: function(event, data){
            var node = data.node;
            data.result = {
              url: base_url + 'index.php/status/get_lazy_load_folder',
              data: {mode: "children", parent: node.key},
              method:"POST",
              cache: false,
              complete: function(xhrobject,status){
                setup_file_download_links($(el));
              }
            };
          },
          loadChildren: function(event, ctx) {
            ctx.node.fixSelection3AfterClick();
          },          
          expand: function(event,data){
            setup_file_download_links($(el));
          },
          cookieId: "fancytree_tx_" + el_id,
          idPrefix: "fancytree_tx_" + el_id + "-"
        }
      );
    }
  });
};

var get_tree_data = function(event, data){
  var id_matcher = /.+_(\d+)/i;
  var m = data.node.key.match(id_matcher);
  var trans_id = parseInt(m[1],10);
  // setup_file_download_links($(el));  
  // var url = 
};
