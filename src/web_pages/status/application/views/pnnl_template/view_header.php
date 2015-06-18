<?= doctype('html5'); ?>
<?php
  $form_object = isset($form_object) ? $form_object : '';
  $table_object = isset($table_object) ? $table_object : "";
?>
<html>
  <head>
<?php
  $page_header = isset($page_header) ? $page_header : "Untitled Page";
  $title = isset($title) ? $title : $page_header;
  $rss_link = isset($rss_link) ? $rss_link : "";  
?>  
    <title>MyEMSL Status - <?= $title ?></title>
      <?= $rss_link ?>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    <meta  name="description" content="" />
    <meta name="keywords" content="" />
<?php $this->load->view('pnnl_template/globals'); ?>
  <?php if(isset($script_uris) && sizeof($script_uris) > 0): ?>
    <?php foreach($script_uris as $uri): ?>
    <script type="text/javascript" src="<?= $uri ?>"></script>
    <?php endforeach; ?>
    
  <?php endif; ?>
  <?php if(isset($css_uris) && sizeof($css_uris) > 0): ?>
    <?php foreach($css_uris as $css): ?>
    <link rel="stylesheet" type="text/css" href="<?= $css ?>" />
    <?php endforeach; ?>
    
  <?php endif; ?>
    <script type="text/javascript">
      var base_url = "<?= base_url() ?>";
    </script>
  </head>