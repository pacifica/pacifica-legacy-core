<?php
require_once('baseline_controller.php');

class Status extends Baseline_controller {

  function __construct() {
    parent::__construct();
    $this->load->model('status_model','status');
    $this->load->model('Myemsl_model','myemsl');
    $this->load->model('Cart_model','cart');
    $this->load->helper(array('inflector','item','url','opwhse_search','form','network'));
    $this->load->library(array('table'));
    $this->status_list = array(
      0 => 'Submitted', 1 => 'Received', 2 => 'Processing',
      3 => 'Verified', 4 => 'Stored', 5 => 'Available', 6 => 'Archived'
    );
    
  }
  
  public function index(){
    redirect('status/overview');
  }
  
  public function view($lookup_type,$id){
    $this->page_data['page_header'] = "Upload Report";
    $this->page_data['title'] = "Upload Report";
    $this->page_data['css_uris'] = array(
      base_url()."resources/scripts/fancytree/skin-lion/ui.fancytree.css",
      base_url()."resources/stylesheets/status.css",
      base_url()."resources/stylesheets/status_style.css",
      base_url()."resources/stylesheets/file_directory_styling.css"
    );
    $this->page_data['script_uris'] = array(
      base_url()."resources/scripts/fancytree/jquery.fancytree-all.js",
      base_url()."resources/scripts/status_common.js",
      base_url()."resources/scripts/single_item_view.js"
    );
    $this->page_data['load_prototype'] = false;
    $this->page_data['load_jquery'] = true;  
    
    if($lookup_type == 'j' || $lookup_type == 'job'){
      //lookup transaction_id from job
      $lookup_type = 't';
      $id = $this->status->get_transaction_id($id);
    }
    $inst_id = $this->status->get_instrument_for_id('t',$id);
    $lookup_type_description = $lookup_type = 't' ? 'transaction' : 'job';
    $transaction_list = array();
    $transaction_list[] = $id;
    
    $transaction_info = $this->status->get_formatted_object_for_transactions($transaction_list);
    $this->page_data['status_list'] = $this->status_list;
    if(empty($transaction_info)){
      $this->page_data['message'] = "No {$lookup_type_description} with an identifier of {$id} was found";
      $this->page_data['script_uris'] = array();
    }
    $this->page_data['transaction_data'] = $transaction_info;
    $this->page_data['js'] = "var initial_inst_id = {$inst_id};";
        // var_dump($transaction_info);
    $this->page_data['show_instrument_data'] = true;
    $this->load->view('single_item_view',$this->page_data);
    
    
    
    
}

  
  public function overview($proposal_id = false, $instrument_id = false, $time_period = false){
    $time_period = $this->input->cookie('myemsl_status_last_timeframe_selector') ? $this->input->cookie('myemsl_status_last_timeframe_selector') : $time_period;
    $instrument_id = $this->input->cookie('myemsl_status_last_instrument_selector') ? $this->input->cookie('myemsl_status_last_instrument_selector') : $instrument_id;
    $proposal_id = $this->input->cookie('myemsl_status_last_proposal_selector') ? $this->input->cookie('myemsl_status_last_proposal_selector') : $proposal_id;
    if(!$this->input->is_ajax_request()){
      $view_name = 'emsl_mgmt_view';
      $this->page_data['page_header'] = "MyEMSL Status Reporting";
      $this->page_data['title'] = "Overview";
      $this->page_data['informational_message'] = "";
      $this->page_data['css_uris'] = array(
        base_url()."resources/scripts/fancytree/skin-lion/ui.fancytree.css",
        base_url()."resources/stylesheets/status.css",
        base_url()."resources/stylesheets/status_style.css",
        base_url()."resources/scripts/select2/select2.css",
        base_url()."resources/stylesheets/file_directory_styling.css"
      );
      $this->page_data['script_uris'] = array(
        base_url()."resources/scripts/spinner/spin.min.js",
        base_url()."resources/scripts/fancytree/jquery.fancytree-all.js",
        base_url()."resources/scripts/myemsl_file_download.js",
        base_url()."resources/scripts/status_common.js",
        base_url()."resources/scripts/emsl_mgmt_view.js",
        base_url()."resources/scripts/select2/select2.js",
        base_url()."resources/scripts/moment.min.js"
      );
      $full_user_info = $this->myemsl->get_user_info();
      $proposal_list = array();
      
      foreach($full_user_info['proposals'] as $prop_id => $prop_info){
        $proposal_list[$prop_id] = $prop_info['title'];
      }
      krsort($proposal_list);
      
      $js = "var initial_proposal_id = '{$proposal_id}';
var initial_instrument_id = '{$instrument_id}';
var initial_time_period = '{$time_period}';
var email_address = '{$this->email}';
var initial_instrument_list = [];";
      
      $this->page_data['proposal_list'] = $proposal_list;
      
      $this->page_data['load_prototype'] = false;
      $this->page_data['load_jquery'] = true;
      $this->page_data['selected_proposal'] = isset($proposal_id) ? $proposal_id : false;
      $this->page_data['time_period'] = $time_period;
      $this->page_data['instrument_id'] = $instrument_id;
      // $this->page_data['instrument_list'] = $instrument_group_xref;
      $this->page_data['js'] = $js;
    }else{
      $view_name = 'upload_item_view.html';
    }
    // $this->page_data['informational_message'] = "";
    // if($proposal_id && $instrument_id && $time_period){
    if(isset($instrument_id) && isset($time_period) && $time_period > 0){
      $inst_lookup_id = $instrument_id >= 0 ? $instrument_id : "";
      $group_lookup_list = $this->status->get_instrument_group_list($instrument_id);
      if(array_key_exists($instrument_id,$group_lookup_list['by_inst_id']) ){
        $results = $this->status->get_transactions_for_group(
          array_keys($group_lookup_list['by_inst_id'][$instrument_id]),
          $time_period,
          $proposal_id
        );
      }elseif($instrument_id < 0){
        $results = array(
          'transaction_list' => array(),
          'time_period_empty' => false,
          'message' => ""
        );
        foreach($group_lookup_list['by_inst_id'] as $inst_id => $group_id_list){
          $transaction_list = $this->status->get_transactions_for_group(array_keys($group_id_list), $time_period, $proposal_id);
          if(!empty($transaction_list['transaction_list'])){
            foreach($transaction_list['transaction_list']['transactions'] as $group_id => $group_info){
              if(!array_key_exists('transactions',$results['transaction_list'])){
                $results['transaction_list']['transactions'] = array();
              }
              if(!array_key_exists($group_id,$results['transaction_list']['transactions'])){
                $results['transaction_list']['transactions'][$group_id] = $group_info;
              }
            }
          }
          if(!empty($transaction_list['transaction_list']['times'])){
            foreach($transaction_list['transaction_list']['times'] as $ts => $tx_id){
              if(!array_key_exists('times',$results['transaction_list'])){
                $results['transaction_list']['times'] = array();
              }
              if(!array_key_exists($ts, $results['transaction_list']['times'])){
                $results['transaction_list']['times'][$ts] = $tx_id;
              }
            }
            
          }
        }
      }else{
        $results = array(
          'transaction_list' => array(), 
          'time_period_empty' => true, 
          'message' => "No data uploaded for this instrument"
        );
      }
    }else{
      $results = array(
        'transaction_list' => array(), 
        'time_period_empty' => true, 
        'message' => "No data uploaded for this instrument"
      );
    }
      // var_dump($group_lookup_list);
    // }else{
      // $results = array('transaction_list' => array(), 'time_period_empty' => true, 'message' => "Select an EUS Proposal and Instrument to load data");
    // }
    $this->page_data['cart_data'] = array('carts' => $this->cart->get_active_carts($this->user_id, false));
    $this->page_data['status_list'] = $this->status_list;
    $this->page_data['transaction_data'] = $results['transaction_list'];
    $this->page_data['informational_message'] = $results['message'];    
    $this->load->view($view_name,$this->page_data);
  }
  
  
  public function get_files_by_transaction($transaction_id){
    $treelist = $this->status->get_files_for_transaction($transaction_id);
    $output_array = format_folder_object_json($treelist['treelist']);
    // var_dump($output_array);
    transmit_array_with_json_header($output_array);
  }
  
  public function get_latest_transactions($instrument_id,$proposal_id,$latest_id){
    $group_list = $this->status->get_instrument_group_list($instrument_id);
    $new_transactions = array();
    if(array_key_exists($instrument_id,$group_list['by_inst_id'])){
      $new_transactions = $this->status->get_latest_transactions(array_keys($group_list['by_inst_id'][$instrument_id]),$proposal_id,$latest_id);    
    }    
    if(empty($new_transactions)){
      print "";
      return;
    }
    $results = $this->status->get_formatted_object_for_transactions($new_transactions);
    $group_list = $this->status->get_groups_for_transaction($new_transactions);
    foreach($group_list['groups'] as $tx_id => $group_info){
      $results['transactions'][$tx_id]['groups'] = $group_info;
    }
      
    
    $this->page_data['status_list'] = $this->status_list;
    $this->page_data['transaction_data'] = $results;
    $view_name = 'upload_item_view.html';
    // var_dump($results);
    if(!empty($results['times'])){
      $this->load->view($view_name, $this->page_data);
    }else{
      print "";
    }
  }
  
  public function get_status($lookup_type, $id = 0){
    //lookup by (j)ob or (t)ransaction
    //check for list of transactions in post
    if($this->input->post('transaction_list')){
      $lookup_type = 't';
      $item_list = $this->input->post('transaction_list');
    }elseif($this->input->post('job_list')){
      $lookup_type = 'j';
      $item_list = $this->input->post('job_list');
    }elseif($id > 0){
      $item_list = array($id);
    }

    $item_keys = array_keys($item_list);
    sort($item_keys);
    $last_id = array_pop($item_keys);
        
    $status_info = array();
    
    $status_obj = $this->status->get_status_for_transaction($lookup_type,array_keys($item_list));
    if(!empty($status_obj)){
      foreach($status_obj as $item_id => $item_info){
        $sortable = $item_info;
        krsort($sortable);
        $latest_step_obj = array_shift($sortable);
        $latest_step = intval($latest_step_obj['step']);
        $status_info_temp = array(
          'latest_step' => $latest_step,
          'status_list' => $this->status_list,
          'transaction_id' => $item_id
        );
        $item_text = trim($this->load->view('status_breadcrumb_insert_view.html',$status_info_temp, true));
        if($item_list[$item_id] != sha1($item_text)){
          $status_info[$item_id] = $item_text;
        }
      }
      krsort($status_info);
      if($this->input->is_ajax_request()){
      // if(sizeof($status_info) > 1){
        transmit_array_with_json_header($status_info);
      }elseif(sizeof($status_info) == 1){
        $this->load->view('status_breadcrumb_insert_view.html',$status_info[$id]);
      }
      
    }
  }

  public function get_lazy_load_folder(){
    if(!$this->input->post('parent')){
      print("");
      return;
    }
    $node = intval(str_replace("treeData_","",$this->input->post('parent')));
    $treelist = $this->status->get_files_for_transaction($node);
    $output_array = format_folder_object_json($treelist['treelist'],"test");
    transmit_array_with_json_header($output_array);
  }

  public function job_status($job_id = -1){
    $HTTP_RAW_POST_DATA = file_get_contents('php://input');
    $values = json_decode($HTTP_RAW_POST_DATA,true);
    if(!$values && $job_id > 0){
      //must not have a list of values, so just check the one
      $values = array($job_id);
    }
    $results = $this->status->get_job_status($values, $this->status_list);
    transmit_array_with_json_header($results);
  }
  
  
  public function get_instrument_list($proposal_id){
    // $instruments = $this->eus->get_instruments_for_proposal($proposal_id);
    $full_user_info = $this->myemsl->get_user_info();
    $instruments = array();
    $instruments_available = $full_user_info['proposals'][$proposal_id]['instruments'];
    $instruments[-1] = "All Available Instruments for Proposal {$proposal_id}";
    foreach($instruments_available as $inst_id){
      $instruments[$inst_id] = "Instrument {$inst_id}: {$full_user_info['instruments'][$inst_id]['eus_display_name']}";
    }
    
    asort($instruments);
    
    format_array_for_select2(array('items' => $instruments));
  }  
  
  public function test_get_instrument_list(){
    var_dump($this->status->get_instrument_group_list());
  }
  
  public function test_get_groups_for_proposal($proposal_id){
    $results = $this->status->get_proposal_group_list($proposal_id);
    var_dump($results);
  }
  
  public function test_get_groups_for_transaction($transaction_id){
    $this->status->get_groups_for_transaction($transaction_id);
    
  }
  
  public function test_get_transactions_for_proposal($proposal_id){
    $results = $this->status->get_transactions_for_group(-1, 30,$proposal_id);
    var_dump($results);
  }
  
  public function test_get_userinfo(){
    $user_info = $this->myemsl->get_user_info();
    var_dump($user_info);
  }
  
  public function test_get_proposals_for_instrument($instrument_id){
    $inst_list = $this->eus->get_proposals_for_instrument($instrument_id);
    var_dump($inst_list);
  }
  
  
}

?>