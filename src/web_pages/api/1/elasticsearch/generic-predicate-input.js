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
				var data = $this.data('myemslPredicateInput');
				if(!data) {
					data = {
						target: $this,
						wrapper: null
					};
					data = $.extend(data, options);
					$(this).data('myemslPredicateInput', data);
					data = $this.data('myemslPredicateInput');
					$(this).wrap('<div>');
					var wrapper = $(this).parent();
					data.wrapper = wrapper;
/*					var marker = $('<span />').insertBefore(data.target);
					data.target.detach().attr('type', 'hidden').insertAfter(marker);
					marker.remove();*/
					data.target.addClass('myemsl_hidden');
					var number_input = $('<input size="5" type="text" class="numbermod number" value="0" />');
					wrapper.append(number_input);
					wrapper.append('<span class="tentothei"> x 10<span style="font-size: 50%; vertical-align: super;"><input style="border-style: dotted; border-color: #d0d0d0; width: 3em;" class="numbere numbermod " maxlength="3" type="text" value="0"></input></span> = <span class="numbereq" style-"float:left">0</span>');
					number_input.autocomplete({'source': function() {}});
					wrapper.find('.numbermod').focus(function() {
						if($(this).val() == '0') {
							$(this).val('');
						}
					}).blur(function() {
						if($(this).val() == '') {
							$(this).val('0');
						}
					}).keyup(function(wrapper, data) { return function() {
						wrapper.find('.numbereq').text(wrapper.find('.number').val() * Math.pow(10, wrapper.find('.numbere').val()));
						data.target.myemslPredicateInput('sync_fields');
					}}(wrapper, data));
					var type = $('<input class="numbertype" type="text"/>');
					wrapper.append(type);
					var tmpoptions = {
						'widget': 'unit'
					}
					if('initial_select' in data && data['initial_select']['type'] != 'unknown') {
						tmpoptions['finder_options'] = {
							'facets_set': [
								{
									'facet':'type',
									'term':data['initial_select']['type'],
									'query_term':'type:"' + data['initial_select']['type'] + '"'
								}
							]
						};
					}
					type.myemslInputPlusFinder(tmpoptions);
					type.bind('myemsl_selection_changed', function(data) {return function() {
						data.target.myemslPredicateInput('sync_fields');
					}}(data));
//FIXME
				//	type.myemslInputPlusFinder('select', '(si:cm)');
					if('initial_select' in data) {
						 type.myemslInputPlusFinder('select', data['initial_select']);
					}
					data.target.myemslPredicateInput('sync_fields');
				}
			});
 		},
		sync_fields: function() {
			return this.each(function(){
				var $this = $(this);
				var data = $this.data('myemslPredicateInput');
				var val = data.wrapper.find('.numbertype').myemslInputPlusFinder('selection');
				var exp = data.wrapper.find('.numbere').val()
				if(val == null) {
					val = "";
				}
				else {
					val = val['val'];
				}
				if(exp == '') {
					exp = '0';
				}
				$this.val(JSON.stringify({
					'val': data.wrapper.find('.number').val(),
					'exp': exp,
					'type': val
				}));
			});
		},
		destroy: function() {
			return this.each(function(){
				var $this = $(this);
				var data = $this.data('myemslPredicateInput');
				if(data) {
					/*data.target.detach().attr('type', 'text').insertAfter(data.wrapper);*/
					data.target.insertAfter(data.wrapper);
					data.target.removeClass('myemsl_hidden');
					data.wrapper.remove();
					$(window).unbind('.myemslPredicateInput');
					$this.removeData('myemslPredicateInput');
				}
			})
		}
	};
	$.fn.myemslPredicateInput = function(method) {
		if(methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if(typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.myemslPredicateInput');
		}
	};
}));
