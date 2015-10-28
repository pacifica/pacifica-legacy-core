var bearer_token = "";
var url_base = '/myemsl/status/index.php';
var token_url_base = '/myemsl/itemauth/';
var token_url_base = url_base + '/cart/get_cart_token/';
var cart_url_base = '/myemsl/api/2/cart/';
var cart_info_url = url_base + '/cart/listing/';
var max_size = 1024 * 1024 * 1024 * 50; //50 GB (base 2)
var friendly_max_size = '';
var exceed_max_size_allow = false;

var setup_file_download_links = function(parent_item) {
  parent_item = $(parent_item);
  var tx_id = parent_item.prop('id').replace('tree_','');
  var file_object_collection = parent_item.find('.item_link');
  file_object_collection.unbind('click').click(function(e) {
    var file_object_data = JSON.parse($(e.target).siblings('.item_data_json').html());
    download_myemsl_item(file_object_data);
  });
  var dl_button = $('#dl_button_' + tx_id);
  dl_button.unbind('click').click(function(e){
    var el = $(e.target);
    cart_download(parent_item, tx_id, null);
  });
  
};


var cart_download = function(transaction_container, tx_id, cart_id){
  var selected_files = get_selected_files(transaction_container);
  //check for token
  var item_id_list = Object.keys(selected_files.sizes);
  get_token(item_id_list, tx_id);
};


var get_token = function(item_id_list, tx_id){
  var token_url = token_url_base;
  var cart_url = cart_url_base;
  var token_getter = $.ajax({
    url:token_url,
    type: 'POST',
    data: JSON.stringify({'items' : item_id_list})
  })
  .done(function(data){
    var cart_submitter = $.ajax({
      url: cart_url,
      type: 'POST',
      data: JSON.stringify({
        'items':item_id_list,
        'auth_token':data
      }),
      dataType: 'json'
    })
    .done(function(data){
      var status_box = $('#status_block_' + tx_id);
      status_box.html(item_id_list.length + " items added to download cart");
      var cart_id = data.cart_id;
      submit_cart_for_download(tx_id,cart_id);
    });
  })
  .fail(function(jq,textStatus,errormsg){
    
  });
};



var submit_cart_for_download = function(tx_id, cart_id){
  if(cart_id == null){
    return;
  }
  var submit_url = cart_url_base + cart_id + '?submit&email_addr=' + email_address;
  $.ajax({
    url:submit_url,
    data: JSON.stringify({}),
    dataType: 'text',
    type:'POST',
    processData:false
  })
  .done(function(data){
    $('#cart_id_' + tx_id).val(cart_id);
    var dialog_message = $('<div><p>A new download cart has been created for this data.</p><p>Status info will appear in the Download Queue shortly</p></div>');
    $('#dl_button_' + tx_id).fadeOut();
    $('#tree_' + tx_id).fancytree('getTree').visit(function(node){
        node.setSelected(false);
    });
    dialog_message.dialog({
      modal:true,
      buttons: {
        Ok: function(){
          check_cart_status(cart_id);
          $(this).dialog("close");
        }
      }
    });
  })
  .fail(function(jq,textStatus,errormsg){
    debugger;
  });
  
};

var cart_delete = function(cart_id){
  if (cart_id == null) {
    return;
  }
  var url = cart_url_base + cart_id;
  $.ajax({
    url : url,
    type : 'DELETE',
    processData : false,
    dataType : 'text'
  })
  .done(function(data){
    //check how many rows are left
    $('#cart_line_' + cart_id).remove();
    check_cart_status();
  })
  .fail(function(jq, textStatus, errormsg){
    var error = errormsg;
  });
};

var dead_cart_delete = function(cart_id){
  if (cart_id == null) {
    return;
  }
  var url = url_base + '/cart/delete/' + cart_id;
  $.get(url, function(data){
    $('#cart_listing').html(data);
    get_cart_count();
  });
};

var check_cart_status = function(tx_id){
  if(tx_id == undefined){ tx_id = ''; }
  var cart_url = cart_info_url + tx_id;
  $.get(cart_url, function(data){
    $('#cart_listing').html(data);
    get_cart_count();
  });
  
};

var get_cart_count = function(){
  var cart_count = $('.cart_line').length;
  if(cart_count > 0){
    if($('#cart_listing_container:visible').length == 0){
      $('#cart_listing_container').slideDown('slow');
    }
  }else{
    if($('#cart_listing_container:visible').length > 0){
      $('#cart_listing_container').slideUp('slow');
    }
  }
};

var get_selected_files = function(tree_container){
  if(typeof(tree_container) == "string"){
    tree_container = $('#' + tree_container);
  }
  var tree = tree_container.fancytree('getTree');
  var selCount = tree.countSelected();
  var selFiles = [];
  if(selCount > 0){
    var topNode = tree.getRootNode();
    var dataNode = topNode.children[0];
    //check lazyload status and load if necessary
    if(selCount == 1 && !dataNode.isLoaded()){
      dataNode.load()
      .done(function(){
        dataNode.render(true,true);
        selCount = tree.countSelected();
        selFiles = get_file_sizes(tree_container);
        update_download_status(tree_container,selCount);
        return selFiles;
      });
    }else{
      selFiles = get_file_sizes(tree_container);
      update_download_status(tree_container,selCount);
      return selFiles;
    }
  }else{
    selFiles = get_file_sizes(tree_container);
    update_download_status(tree_container,selCount);
  }
};



var get_file_sizes = function(tree_container){
  var tree = tree_container.fancytree('getTree');
  var total_size = 0;
  var sizes = {};
  var item_info = {};
  
  var item_id_list = $.map(tree.getSelectedNodes(), function(node){
    if(!node.folder){
      return parseInt(node.key.replace('ft_item_',''),10);
    }
  });

  
  tree.render(true,true);
  $.each(item_id_list, function(index,item){
    item_info = JSON.parse($('#item_id_' + item).html());
    sizes[item] = item_info.size;
    total_size += parseInt(item_info.size,10);
  });
  var message_container = tree_container.parents('.transaction_container').find('.error');
  friendly_max_size = friendly_max_size.length == 0 ? myemsl_size_format(max_size) : friendly_max_size;
  var friendly_total_size = myemsl_size_format(total_size);
  var dl_button = tree_container.parents('.transaction_container').find('.dl_button');
  var mc_html = '';
  dl_button.show();
  if(total_size > max_size){
    mc_html = '<div style="text-align:center;">';
    mc_html += '<p>The total size of the files you have selected';
    mc_html += ' (' + friendly_total_size + ') ';
    mc_html += 'is greater than the ';
    mc_html += friendly_max_size;
    mc_html += ' limit <br>imposed for unrestricted downloads from the system.</p>';
    if(exceed_max_size_allow){
      mc_html += '<p>Downloads exceeding the size cutoff are allowed, ';
      mc_html += 'but will be placed in an <em>Administrative Hold</em> state ';
      mc_html += 'pending approval from a MyEMSL administrator</p>';
      mc_html += '</div>';
      dl_button.enable();
    }else{
      dl_button.disable();
    }
    message_container.html(mc_html).parent().show();
  }else{
    dl_button.enable();
    message_container.html('').parent().hide();
  }
  return {'total_size' : total_size, 'sizes' : sizes};
};


var update_download_status = function(tree_container, selectCount){
  var el_id = $(tree_container).prop('id').replace('tree_','');
  var dl_button = $('#dl_button_container_' + el_id);
  if(selectCount > 0){
    var fileSizes = get_file_sizes(tree_container);
    var totalSizeText = myemsl_size_format(fileSizes.total_size);
    var pluralizer = Object.keys(fileSizes.sizes).length != 1 ? "s" : "";
    $('#status_block_' + el_id).html(Object.keys(fileSizes.sizes).length + ' file' + pluralizer + ' selected [' + totalSizeText + ']');
    dl_button.slideDown('slow');
  }else{
    $('#status_block_' + el_id).html('&nbsp;');
    dl_button.slideUp('slow');
  }
  
};

var download_myemsl_item = function(file_object_data) {
  //get a download token
  var item_id = file_object_data.item_id;

  var token_url = token_url_base + item_id;
  var token_getter = $.ajax({
    url: token_url,
    method:'get'
  });
  token_getter.done(function(data){
    bearer_token = data;
    var token = data;
    myemsl_tape_status(token, file_object_data);
  });
};

var myemsl_tape_status = function(token, file_object_data, cb) {
  var item_id = file_object_data.item_id;
  var file_name = file_object_data.name;

  var ajx = $.ajax({
    //FIXME foo, bar
    url : "/myemsl/item/foo/bar/" + item_id + "/2.txt/?token=" + token + "&locked",
    type : 'HEAD',
    processData : false,
    success : function(token, status_target) {
      return function(ajaxdata, status, xhr) {
        var custom_header = xhr.getResponseHeader('X-MyEMSL-Locked');
        if (custom_header == "false") {
          //pop up a dialog box regarding the item being on tape
        } else {
          window.location.href = '/myemsl/item/foo/bar/' + item_id + '/' + file_name + "?token=" + token;
        }
      };
    }(token, status),
    error : function(token, status_target) {
      // return function(xhr, status, error) {
        // if (xhr.status == 503) {
          // cb('slow');
        // } else {
          // cb('error');
        // }
      // };
    }//(token, status)
  });
  return ajx;
}; 


var myemsl_size_format = function(bytes) {
    var suffixes = ["B", "KB", "MB", "GB", "TB", "EB"];
    if (bytes == 0) {
        suffix = "B";
    } else {
        var order = Math.floor(Math.log(bytes) / Math.log(10) / 3);
        bytes = (bytes / Math.pow(1024, order)).toFixed(1);
        suffix = suffixes[order];
    }
    return bytes + ' ' + suffix;
};
