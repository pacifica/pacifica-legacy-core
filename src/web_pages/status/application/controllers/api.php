<?php
require_once('baseline_controller.php');

class API extends Baseline_controller {

  function __construct() {
    parent::__construct();
    $this->load->model('status_model','status');
    $this->load->model('API_model','api');
    $this->load->model('Cart_model','cart');
    $this->load->helper(array('inflector','item','url','opwhse_search','form','network'));
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
  function item_search($metadata_field_name,$metadata_value){
    //look for additional terms?
    if($this->uri->total_rsegments() % 2 != 0){
      //got an odd number of segments, yields incomplete pairs
      return false;
    }
    $pairs = $this->uri->ruri_to_assoc();
    if(!$pairs){
      //return error message about not having anything to search for
      return false;
    }
    $results = $this->api->search_by_metadata($pairs);
    transmit_array_with_json_header($results);
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
  
  
}
?>