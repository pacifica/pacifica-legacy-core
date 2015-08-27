<?= doctype('html5'); ?>
<?php
  $page_header = isset($page_header) ? $page_header : "Untitled Page";
  $title = isset($title) ? $title : $page_header;
  $rss_link = isset($rss_link) ? $rss_link : "";  
?>  
<html>
  <head>
    <title>MyEMSL Status - <?= $title ?></title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    <meta  name="description" content="" />
    <meta name="keywords" content="" />
<?php $this->load->view("{$this->template_version}_template/globals"); ?>

<?php if(isset($script_uris) && sizeof($script_uris) > 0): ?>

    <!-- begin page-wise javascript loads -->
  <?php foreach($script_uris as $uri): ?>
  <script type="text/javascript" src="<?= $uri ?>"></script>
  <?php endforeach; ?>
  <!-- end page-wise javascript loads -->

<?php endif; ?>
<?php if(isset($css_uris) && sizeof($css_uris) > 0): ?>

    <!-- begin page-wise css loads -->
  <?php foreach($css_uris as $css): ?>
  <link rel="stylesheet" type="text/css" href="<?= $css ?>" />
  <?php endforeach; ?>
  <!-- end page-wise css loads -->

<?php endif; ?>
    <script type="text/javascript">
      var base_url = "<?= base_url() ?>";
    </script>
  </head>
  <body>
    <div class="page_content">
      <header>
          <div id="page_header">
              <div id="logo_container">
                  <div id="logo_image">&nbsp;</div>
              </div>
              <div id="site_slogan">Environmental Molecular Sciences Laboratory</div>
              <div id="menu_block_container">
                  <nav>
                      <ul id="page_menu">
                          <li><a href="https://www.emsl.pnl.gov/emslweb/">Home</a><span class='menu_separator'>|</span></li>
                          <li>About<span class='menu_separator'>|</span></li>
                          <li>Science<span class='menu_separator'>|</span></li>
                          <li>Capabilities<span class='menu_separator'>|</span></li>
                          <li>Working With Us<span class='menu_separator'>|</span></li>
                          <li>News</li>
                      </ul>
                  </nav>
              </div>
          </div>
      </header>