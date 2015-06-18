<?php
  $table_object = !empty($table_object) ? $table_object : "";
  $this->load->view('pnnl_template/view_header'); 
  $js = isset($js) ? $js : "";
  
?>
<body class="col1">
  <?php $this->load->view('pnnl_template/intranet_banner'); ?>
  <div id="page">
    <?php $this->load->view('pnnl_template/top',$navData['current_page_info']); ?>
    <div id="container">
      <div id="main">
        
        <h1 class="underline"><?= $page_header ?></h1>
        <div style="position:relative;">
          <div class="form_container">
            
            <form id="instrument_selection" class="themed">
              <fieldset id="inst_select_container">
                <legend>Instrument Selection</legend>
                <div class="full_width_block">
                  <select id="proposal_selector" class="criterion_selector" name="proposal_selector" style="width:96%;">
                    <option></option>
                    <?php foreach($proposal_list as $prop_id => $prop_title): ?>
                      <?php $selected_state = $prop_id == $selected_proposal ? ' selected="selected"' : ''; ?>
                      <?php $trunc_prop_title = truncate_text($prop_title, 110); ?>
                    <option value="<?= $prop_id ?>"<?= $selected_state ?> title="<?= $prop_title ?>">Proposal <?= $prop_id ?>: <?= $trunc_prop_title ?></option>
                    <?php endforeach; ?><br />
                    <?php $prop_list_object = "var initial_proposal_list = [".implode(',',array_keys($proposal_list))."];"; ?>
                    <?php $js .= "\n".$prop_list_object; ?>
                  </select>
                </div>
                
                <div class="full_width_block" style="margin-top:1em;">
                  <div class="left_block">
                    <input id="instrument_selector" class="criterion_selector" disabled="disabled" name="instrument_selector" type="hidden" style="width:95%;"/>
                    <div class="selector_spinner_container" id="instrument_selector_spinner"></div>
                  </div>
                  <div class="right_block">
                    <select id="timeframe_selector" class="criterion_selector" name="timeframe_selector" style="width:100%;">
                      <?php $period_list = array(
                        '1' => "Last 24 Hours",
                        '2' => "Last 48 Hours",
                        '7' => "Last 7 Days",
                        '14' => "Last 2 Weeks",
                        '30' => "Last Month",
                        '365' => "Last Year"); ?>
                      <option></option>
                      <?php foreach($period_list as $period => $desc): ?>
                        <?php $selected_state = $period == $time_period ? ' selected="selected"' : ''; ?>
                      <option value="<?= $period ?>"<?= $selected_state ?>><?= $desc ?></option>
                      <?php endforeach; ?>
                    </select>
                  </div>
                </div>
              </fieldset>
            </form>            
            
          </div>
          <?php $hide_cart_data = empty($cart_data['carts']) ? "display:none;" : ""; ?>
          <div id="cart_listing_container" class="themed" style="<?= $hide_cart_data ?>margin-top:1em;">
            <fieldset id="cart_listing_fieldset">
              <legend>Download Queue</legend>
              <div id="cart_listing">
                <?php $this->load->view('cart_list_insert.html', $cart_data); ?>
              </div>
            </fieldset>
          </div>
          
          <div class="loading_progress_container status_messages" id="loading_status" style="display:none;">
            <span class="spinner">&nbsp;&nbsp;&nbsp;</span>
            <span id="loading_status_text">Loading...</span>
          </div>

          <div class="themed" id="item_info_container" style="margin-top:20px;"></div>
        </div>

      </div>
    </div>
    <?php $this->load->view('pnnl_template/view_footer'); ?>
  </div>
<script type='text/javascript'>
//<![CDATA[
  <?= $js ?> 
//]]>
</script>  
 
</body>
</html>
