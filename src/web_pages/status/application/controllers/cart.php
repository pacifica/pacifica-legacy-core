<?php
require_once('baseline_controller.php');

class Cart extends Baseline_controller {

  function __construct() {
    parent::__construct();
    $this->load->model('Cart_model','cart');
    $this->load->helper(array('url','network'));
  }
  
  public function get_cart_token($item_id = false){
    $HTTP_RAW_POST_DATA = file_get_contents('php://input');
    $values = json_decode($HTTP_RAW_POST_DATA,TRUE);
    if(empty($values) && $item_id){
      $item_list = array($item_id);
    }else{
      $item_list = $values['items'];
    }
    echo generate_cart_token($item_list,$this->user_id);
  }
  
  
  public function listing($optional_message = ""){
    $cart_list = $this->cart->get_active_carts($this->user_id);
    $cart_list['optional_message'] = $optional_message;
    $this->load->view('cart_list_insert.html',array('carts' => $cart_list));
  }
  
  
  public function delete($cart_id){
    $success_info = $this->cart->delete_dead_cart($cart_id);
    $this->listing($success_info['message']);
  }
  
  
  
  public function test_generate_cart_token(){
    $item_list = array(105655);
    echo $this->get_cart_token(105655);
  }
  
  public function test_get_cart_list(){
    echo "<pre>";
    var_dump($this->cart->get_active_carts($this->user_id, false));
    echo "</pre>";
  }
}