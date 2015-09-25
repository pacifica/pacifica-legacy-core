<?php
require_once('baseline_controller.php');

class API extends Baseline_controller {

  function __construct() {
    parent::__construct();
    $this->load->model('status_model','status');
    $this->load->model('API_model','api');
    $this->load->model('Cart_model','cart');
    $this->load->helper(array('inflector','item','url','opwhse_search','form','network','myemsl'));
    $this->load->library(array('table'));
    $this->status_list = array(
      0 => 'Submitted', 1 => 'Received', 2 => 'Processing',
      3 => 'Verified', 4 => 'Stored', 5 => 'Available', 6 => 'Archived'
    );
  }
  
  /*
   * Expects alternating terms of field/value/field/value like...
   * <item_search/group.omics.dms.dataset_id/267771/group.omics.dms.instrument/ltq_4>
   */
  function item_search($search_operator = "AND"){
    //are we GET or POST?
    //check for POST body
    $HTTP_RAW_POST_DATA = file_get_contents('php://input');
    $values = json_decode($HTTP_RAW_POST_DATA,true);
    
    if(empty($values)){
      //must be GET request
      if($this->uri->total_rsegments() % 2 == 0){
        //got an even number of segments, yields incomplete pairs
        return false;
      }
      $pairs = $this->uri->ruri_to_assoc(4);
      if(!$pairs){
        //return error message about not having anything to search for
        return false;
      }
    }else{
      //looks like a POST, parse the body and rock on
      $search_operator = array_key_exists('search_operator',$values) && !empty($values['search_operator']) ? $values['search_operator'] : "AND";
      $pairs = array_key_exists('search_terms',$values) ? $values['search_terms'] : array();
    }
    $results = !empty($pairs) ? $this->api->search_by_metadata($pairs) : array('transactions' => array(), 'result_count' => 0, 'metadata' => array());
    transmit_array_with_json_header($results);
  }

  function iteminfo($item_id,$format = "xml"){
    $file_info = $this->api->get_item_info($item_id);
    if($format == 'json'){
      // $file_info_formatted = json_encode($file_info);
      transmit_array_with_json_header(array('myemsl' => $file_info));
    }else{
      $file_info_formatted = new SimpleXMLElement('<?xml version="1.0"?><myemsl></myemsl>');
      array_to_xml($file_info, $file_info_formatted);
      echo $file_info_formatted->asXML();
    }
  }
  
  function status($job_id){
    $status_info = $this->status->get_status_for_transaction('j',$job_id);
    
    $myemsl_obj = new SimpleXMLElement('<?xml version="1.0"?><myemsl></myemsl>');
    foreach($status_info as $job_id => $job_info){
      $status_obj = $myemsl_obj->addChild('status');
      $last_step = array_slice($job_info,-1,1,TRUE);
      $last_step_index = array_pop(array_keys($last_step));
      $last_step_info = array_pop(array_values($last_step));
      foreach($last_step as $step => $step_info){
        $status_obj->addAttribute('username',$step_info['person_id']);
        $transaction_obj = $status_obj->addChild('transaction');
        $transaction_obj->addAttribute('id',$step_info['trans_id']);
      }
      foreach($this->status_list as $index => $display_name){
        if(array_key_exists($index,$job_info)){
          $step_info = $job_info[$index];
        }else{
          $step_info = array(
            'status' => $index < $last_step_index ? "SUCCESS" : "UNKNOWN",
            'message' => $index < $last_step_index ? "completed" : "unknown",
            'step' => $index
          );
        }
        $status = $step_info['status'];
        $message = $step_info['message'];
        
        $step_obj = $status_obj->addChild('step');
        $step_obj->addAttribute('id',$index);
        $step_obj->addAttribute('message',$message);
        $step_obj->addAttribute('status', $status);
      }
    }
    $this->output->set_content_type('text/xml');
    echo $myemsl_obj->asXML();
    
    
    
  }
  
  
  
  
  
  /*
   * testing functions below this line
   */
  
  function test_get_available_group_types($filter = ""){
    $types = $this->api->get_available_group_types($filter);
    echo "<pre>";
    var_dump($types);
    echo "</pre>";
  }
  
  
  function test_iteminfo($item_id){
    $item_info = $this->api->get_item_info($item_id);
  }
  
  
}
?>