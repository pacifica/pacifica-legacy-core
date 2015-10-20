<?php
  $this->template_version = $this->config->item('template');
  $this->load->view("{$this->template_version}_template/view_header"); 
  $js = isset($js) ? 
"<script type='text/javascript'>
//<![CDATA[
  {$js}
//]]>
</script>" : '';  
?>
    <div id="container">
      <div id="main">
        <div id="header_container">
          <h1 class="underline"><?= $page_header ?></h1>
          <div id="login_id_container">
            <em><?= $this->nav_info['current_page_info']['logged_in_user'] ?></em>
          </div>
        </div>
        <div style="position:relative;">
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
          <div class="themed" id="item_info_container" style="margin-top:20px;">
            <?php if(!empty($message)): ?>
            <h2><?= $message ?></h2>
            <?php else: ?>
            <?=  $this->load->view('upload_item_view.html',$transaction_data); ?>
            <?php endif; ?>
          </div>
        </div>

      </div>
    </div>
    <?php $this->load->view("{$this->template_version}_template/view_footer_short"); ?>
<?= $js ?>  
</body>
</html>
