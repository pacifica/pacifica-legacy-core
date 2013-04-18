(function (factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else {
        factory(jQuery);
    }
}(function ($) {
	var methods = {
		init: function(options) {
			return this.each(function() {
				var $this = $(this);
				var data = $this.data('myemslSearchPager');
				if(!data) {
					data = {
						target: $this,
						selected: null
					};
					data = $.extend(data, options);
					$(this).data('myemslSearchPager', data);
					data = $this.data('myemslSearchPager');
				}
				$this.myemslSearchPager('update_pager', 0, 25, 1, 1);
			});
 		},
		update_pager: function(count, per_page, current_page, page_width) {
			return this.each(function(){
				var $this = $(this);
				var data = $this.data('myemslSearchPager');
				var target = data.target;
				if(!data.switch_page) {
					data.switch_page = function(page) {};
				}
                        	var parts = myemsl_paginate_parts(count, per_page, current_page, page_width);
				var list = $('<ol class="myemsl_search_pager_list"></ol>');
				for(i = 0; i < parts['pager'].length; i++) {
					var p = parts['pager'][i]
					var li = $('<li>' + p + '</li>');
					if(p == current_page) {
						li.addClass('myemsl_search_pager_list_selected');
					}
					else {
						li.click(function(page, switch_page) { return function () {
							switch_page(page);
						}}(p, data.switch_page));
					}
					list.append(li);
				}
				target.empty();
				target.append(list);
				var buttonset = $("<div></div>");
				var button = $('<button></button>').button({
					icons: {primary: "ui-icon-arrowthick-1-e"},
					text: false
				});
				button.css('height', '100%');
				button.click(function(switch_page, page) { return function() {
					switch_page(page);
				}}(data.switch_page, current_page + 1));
				if(parts['greatest_page'] == current_page) {
					button.button('disable');
				}
				buttonset.append(button);
				var button = $('<button></button>').button({
					icons: {primary: "ui-icon-arrowthickstop-1-e"},
					text: false
				});
				button.css('height', '100%');
				button.click(function(switch_page, page) { return function() {
					switch_page(page);
				}}(data.switch_page, parts['greatest_page']));
				if(parts['greatest_page'] == current_page) {
					button.button('disable');
				}
				buttonset.append(button);
				buttonset.buttonset();
				buttonset.css('display', 'inline-block');
				buttonset.addClass('myemsl_search_pager_forwards');
				target.append(buttonset);
				var buttonset = $("<div></div>");
				var button = $('<button></button>').button({
					icons: {primary: "ui-icon-arrowthickstop-1-w"},
					text: false
				});
				button.css('height', '100%');
				button.click(function(switch_page, page) { return function() {
					switch_page(page);
				}}(data.switch_page, 1));
				if(current_page == 1) {
					button.button('disable');
				}
				buttonset.append(button);
				var button = $('<button></button>').button({
					icons: {primary: "ui-icon-arrowthick-1-w"},
					text: false
				});
				button.css('height', '100%');
				button.click(function(switch_page, page) { return function() {
					switch_page(page);
				}}(data.switch_page, current_page - 1));
				if(current_page == 1) {
					button.button('disable');
				}
				buttonset.append(button);
				buttonset.buttonset();
				buttonset.css('display', 'inline-block');
				buttonset.addClass('myemsl_search_pager_back');
				target.prepend(buttonset);
			});
		},
		destroy: function() {
			return this.each(function(){
				var $this = $(this);
				var data = $this.data('myemslSearchPager');
				if(data) {
					$this.removeData('myemslSearchPager');
				}
			})
		}
	};
	$.fn.myemslSearchPager = function(method) {
		if(methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if(typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.myemslSearchPager');
		}
	};
}));
