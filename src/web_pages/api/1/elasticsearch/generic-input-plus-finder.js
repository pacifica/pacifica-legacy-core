(function (factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery', 'label_over', 'myemsl.generic-finder'], factory);
    } else {
        factory(jQuery);
    }
}(function ($) {

function unit2row(unit) {
	var baseurl = '/myemsl/elasticsearch-raw/myemsl_unit_index_1346084652';
	var url = baseurl + '/unit/' + encodeURIComponent(unit);
	$.getJSON(url, function(data) {
		if(data.exists) {
			console.log(data._source.type);
			console.log(data._source.namep);
			console.log(data._source.name);
			console.log(data._id);
		}
	});
}

	var widgets = {
		'proposal': {
			'title': "Proposal Finder",
			'label': "proposal"
		},
		'unit': {
			'read-only': true
		}
	};
	var methods = {
		init: function(options) {
			return this.each(function() {
				var $this = $(this);
				var data = $this.data('myemslInputPlusFinder');
				if(!data) {
					$(this).data('myemslInputPlusFinder', {
						target: $this,
						title: "Finder",
						label: "Input"
					});
					var data = $this.data('myemslInputPlusFinder');
					if('widget' in options) {
						if(options['widget'] in widgets) {
							$.extend(data, widgets[options['widget']]);
						}
					}
					$.extend(data, options);
					if('widget' in data && !('finder_widget' in data)) {
						data['finder_widget'] = data['widget'];
					}
					var dialog = $('<div class="myemsl_proposal_search_dialog" title="' + data.title + '"><div class="myemsl_search_container">Loading...</div></div>');
					dialog.prependTo('body');
					$(dialog).dialog({
						bgiframe: true,
						position: 'center',
						draggable: false,
						resizable: false,
						width: $(window).width() - 50,
						height: $(window).height() - 50,
						stack: true,
						zIndex: 99999,
						autoOpen: false,
						modal: true
					});
					data.dialog = dialog;
					var tmp = function(data) {
						var resize_timer = 0;
						return function() {
							function resize_dialog() {
								dialog.dialog('option', 'width', $(window).width() - 50);
								dialog.dialog('option', 'height', $(window).height() - 50);
							};
							$(window).resize(function() {
								clearTimeout(resize_timer);
								resize_timer = setTimeout(resize_dialog, 100);
							});
						}
					} (data);
					tmp();
					finder_options = {}
					if('finder_widget' in data) {
						finder_options['widget'] = data.finder_widget;
					}
					if('finder_options' in data) {
						$.extend(finder_options, options['finder_options']);
					}
					dialog.find('.myemsl_search_container').myemslProposalFinderForm(finder_options);
					$(this).addClass('myemsl_search_textbox');
					$(this).attr('size', 8);
					$(this).wrap('<div style="display: inline-block;"><div class="myemsl_label_over_container"><span class="myemsl_search_wrapper"/></div></div>');
					var wrapper = $(this).parent().parent();
					var button;
					if('read-only' in data && data['read-only']) {
						button = $('<span class="myemsl_search_button_item">&nbsp;</span>')
						$(wrapper).prepend(button);
						button.button({
							icons: {
								secondary: "ui-icon-triangle-1-s"
							}
						});
/*						var marker = $('<span />');
						marker.insertBefore(data.target);
						data.target.detach().attr('type', 'hidden').insertAfter(marker);
						marker.remove();*/
						data.target.addClass('myemsl_hidden');
					}
					else {
						$(wrapper).prepend('<label class="pre" for="foo">' + data.label + '</label>');
						button = $('<span class="ui-icon ui-icon-search myemsl_search_button"><span>');
						$(wrapper).find('.myemsl_search_wrapper').append(button);
						$('.myemsl_label_over_container label').labelOver('over-apply');
					}
					var search_container = dialog.find('.myemsl_search_container');
					search_container.bind('myemsl_proposal_changed', function (data, button, dialog, search_container) { return function() {
						var proposal = search_container.myemslProposalFinderForm('proposal');
						if('read-only' in data && data['read-only']) {
							button.find('span').html(proposal['key']);
							data.target.val(proposal['val']);
						}
						else {
							data.target.val(proposal);
						}
						dialog.dialog('close');
						data.target.focus();
						data.target.trigger('myemsl_selection_changed');
					}}(data, button, dialog, search_container));
					button.click(function(data, button, dialog){ return function() {
						dialog.dialog('open');
					}}(data, button, dialog));
				}
			});
 		},
		destroy: function() {
			return this.each(function(){
				var $this = $(this);
				var data = $this.data('myemslInputPlusFinder');
				$(window).unbind('.myemslInputPlusFinder');
				$this.removeData('myemslInputPlusFinder');
			})
		},
		select: function(passed_data) {
			return this.each(function() {
				var $this = $(this);
				var data = $this.data('myemslInputPlusFinder');
//FIXME spinner
//If string, do spinner, get back row and pass it to select later.
				unit2row(passed_data);
//
				data.dialog.find('.myemsl_search_container').each(function () {
					console.log(this);
					$(this).myemslProposalFinderForm('select', passed_data);
				});
			});
		},
		selection: function() {
			var selection = null;
			this.each(function() {
				var $this = $(this);
				var data = $this.data('myemslInputPlusFinder');
				var i = data.dialog.find('.myemsl_search_container').myemslProposalFinderForm('proposal');
				selection = i;
			});
			return selection;
		}
	};
	$.fn.myemslInputPlusFinder = function(method) {
		if(methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if(typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.myemslInputPlusFinder');
		}
	};
}));
