(function (factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery', 'jquery.ui'], factory);
    } else {
        factory(jQuery);
    }
}(function ($) {
window.myemslLocalPredicateWizard = {
	'show': function() {
		var layout_url = "/myemsl/api/1/elasticsearch/generic-local-predicate-wizard-layout.html";
		if($('#myemsl_data_type_wizard').length > 0) {
			$('#myemsl_data_type_wizard').dialog('open');
		}
		else {
			var dialog = $('<div id="myemsl_data_type_wizard" title="Meta Data Attribute Wizard"><p>Loading...</p></div>');
			$('body').prepend(dialog);
			dialog.dialog({
				'modal': true,
				'resizable': false,
				'width': 1000
			});
			dialog.load(layout_url, function(dialog) { return function () {
				window.myemslLocalPredicateWizard.init();
			}}(dialog));
		}
	},
	'init': function() {
                $.fn.qtip.zindex = 15000000;
		function datatypepicker($fields) {
			$fields.datetimepicker('destroy');
			$fields.datepicker('destroy');
			$fields.myemslPredicateInput('destroy');
//					console.log($('#demoForm').find('input[name="type_question"][value="time"]'));
			if($('#demoForm').find('input[name="type_question"][value="time"]').is(":checked")) {
//FIXME if no day, don't use a date picker, just make months available via a slider.
				var showYear = $('#demoForm').find('input[name="date_year"]').is(":checked");
				var showMonth = $('#demoForm').find('input[name="date_month"]').is(":checked");
				var showDay = $('#demoForm').find('input[name="date_day"]').is(":checked");
				var showSecond = $('#demoForm').find('input[name="date_second"]').is(":checked");
				var showMinute = $('#demoForm').find('input[name="date_minute"]').is(":checked");
				var showHour = $('#demoForm').find('input[name="date_hour"]').is(":checked");
				var dateFormat = "";
				if(showYear) {
					dateFormat += "yy";
				}
				if(showMonth) {
					if(dateFormat != "") {
						dateFormat += '/';
					}
					dateFormat += "mm";
				}
				if(showDay) {
					if(dateFormat != "") {
						dateFormat += '/';
					}
					dateFormat += "dd";
				}
				var timeFormat = "";
				if(showHour) {
					timeFormat = "hh";
				}
				if(showMinute) {
					if(timeFormat != "") {
						timeFormat += ':';
					}
					timeFormat += "mm";
				}
				if(showSecond) {
					if(timeFormat != "") {
						timeFormat += ':';
					}
					timeFormat += "ss";
				}
				if(showHour) {
					timeFormat += " TT";
				}
				var timeOnly = (showYear || showMonth || showDay) == false;
				if(showHour || showMinute || showSecond) {
					if(showHour) {
						timeFormat += ' z';
					}
					$fields.datetimepicker({
						useLocalTimezone: true,
						changeMonth: true,
						changeYear: true,
						showTimezone: showHour,
						'timeFormat': timeFormat,
						'dateFormat': dateFormat,
						ampm: true,
						'timeOnly': timeOnly,
						'showSecond': showSecond,
						'showMinute': showMinute,
						'showHour': showHour,
						addSliderAccess: true,
						sliderAccessArgs: { touchonly: false },
						beforeShow: function(showDay) { return function(input, inst) {
							if(showDay == false) {
								inst.dpDiv.addClass('noday');
							}
						}} (showDay),
						onClose: function(dateText, inst) { 
							inst.dpDiv.removeClass('noday');
//							var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
//							var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
//							$(this).datepicker('setDate', new Date(year, month, 1));
						}
					});
				}
				else {
					$fields.datepicker({
						showButtonPanel: true,
						changeMonth: true,
						changeYear: true,
						'dateFormat': dateFormat,
						beforeShow: function(showDay) { return function(input, inst) {
							if(showDay == false) {
								inst.dpDiv.addClass('noday');
							}
						}} (showDay),
						onClose: function(dateText, inst) { 
							inst.dpDiv.removeClass('noday');
//							var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
//							var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
//							$(this).datepicker('setDate', new Date(year, month, 1));
						}
					});
				}
			}
			else if($('#demoForm').find('input[name="type_question"][value="number"]').is(":checked")) {
				var result = $('#number_default_class').myemslInputPlusFinder('selection');
				console.log(result);
				var options = {};
				if(result) {
					options['initial_select'] = result;
				}
				$fields.myemslPredicateInput(options);
			}
		}
		function step_after_datatype() {
			var openended;
			var retval = 'done';
			$('input[name="endedness"]').each(function() {
				if($(this).is(":checked")) {
					openended = $(this).val();
				}
			});
			$('input[name="enum_fetch"]').each(function() {
				if($(this).is(":checked")) {
					var val = $(this).val();
					if(openended == 'enumerated' && val == 'enum_fetch_manual') {
						retval = 'enum_fetch_form';
					}
				}
			});
			return retval;
		}
		function update_steps_after_datataype() {
			$('#openended').find('input[name="type_question"]').each(function() {
				if($(this).is(":checked")) {
					var step = $(this).val();
					if(step == "uri") {
						step = step_after_datatype();
					}
					$('#openended').find('input[name="step_next_openended"]').val(step);
				}
			});
		}
		$('#openended').find('input[name="type_question"]').change(function() {
			update_steps_after_datataype();
		});
		$('#openended').find('input[name="type_question"][value="number"]').attr('checked', 'checked').change();
		$('.radio_text').each(function() {
			var qtip = $(this);
			var help = qtip.parent().find('.radio_help');
			var $radio_help_button = $('<span class="radio_help_button"/>');
			$radio_help_button.button({
				icons: {
					primary: "ui-icon-help"
				},
				text: false
			});
			help.before($radio_help_button).hide();
			$(this).qtip({
				content: help.text(),
				position: {
					my: "bottom left",
					at: "top left"
				}
			});
			$radio_help_button.click(function(qtip) {return function() {
				qtip.qtip('show');
				return false;
			}} (qtip));
		});
		$('.checkbox_text').each(function() {
			var qtip = $(this);
			var help = qtip.parent().find('.checkbox_help');
			var $checkbox_help_button = $('<span class="checkbox_help_button"/>');
			$checkbox_help_button.button({
				icons: {
					primary: "ui-icon-help"
				},
				text: false
			});
			help.before($checkbox_help_button).hide();
			$(this).qtip({
				content: help.text(),
				position: {
					my: "bottom left",
					at: "top left"
				}
			});
			$checkbox_help_button.click(function(qtip) {return function() {
				qtip.qtip('show');
				return false;
			}} (qtip));
		});
		$('.textbox_help_target').each(function() {
			var qtip = $(this);
			var help = qtip.parent().find('.textbox_help');
			var $textbox_help_button = $('<span class="textbox_help_button"/>');
			$textbox_help_button.button({
				icons: {
					primary: "ui-icon-help"
				},
				text: false
			});
			help.before($textbox_help_button).hide();
			$(this).qtip({
				content: help.text(),
				position: {
					my: "bottom left",
					at: "top left"
				}
			});
			$textbox_help_button.click(function(qtip) {return function() {
				qtip.qtip('show');
				return false;
			}} (qtip));
		});
		$('.checkbox_text').click(function() {
			var $checkbox = $(this).parent().find('input')
			$checkbox.attr('checked', !$checkbox.attr('checked'));
			$checkbox.change();
		});
		$('input[name="enum_fetch"]').change(function() {
			var newval;
			$('input[name="enum_fetch"]').each(function() {
				if($(this).is(":checked")) {
					val = $(this).val();
				}
			});
			if(val == "bool") {
				newval = "done";
			}
			else if(val == "enum_fetch_download") {
				newval = "enum_fetch_download";
			}
			else if(val == "enum_fetch_manual") {
				newval = "openended";
			}
			$('input[name="step_next_enumerated"]').val(newval);
		});
		$('.radio_text').click(function() {
			var $radio = $(this).parent().find('input');
			$radio.attr('checked', true);
			$radio.change();
		});
		$('#myemsl_data_type_wizard').dialog({
			'autoOpen': false,
			'modal': true,
			'resizable': false,
			'width': 1000
		});
		$("#demoForm").formwizard({ 
			historyEnabled:true,
		 	formPluginEnabled: true,
		 	validationEnabled: true,
		 	focusFirstInput : true,
		 	formOptions: {
				success: function(data){$("#status").fadeTo(500,1,function(){ $(this).html("You are now registered!").fadeTo(1000, 0); })},
				beforeSubmit: function($this) { return function(data) {
					var td = $this.data('myemslPredicateWizard');
					console.log(data);
					$.ajax({
						type: "POST",
//FIXME
						url: '/myemsl/api/1/predicate',
						contentType: "application/json",
						data: JSON.stringify(td.form)
					});
					return false;
				}} ($("#demoForm")),
				dataType: 'json',
				resetForm: true
		 	}
		}).data('myemslPredicateWizard', {});
		var target = $('#demoForm');
		$('#demoForm').bind("step_shown", function(event, data) {
			if(data.currentStep == "openended") {
				$('.type_merge').val(step_after_datatype());
			}
			if(data.currentStep == "openended") {
				$('#form_container').find('.value').val('');
				update_steps_after_datataype();
			}
			if(data.currentStep == "enum_fetch_form") {
				datatypepicker($('#form_container').find('.value'));
			}
			if(data.isLastStep) {
				var number_default_type = "";
				console.log(data);
				$form = $('#demoForm');
				console.log($form);
				var form = {};
				form['description'] = {};
				form['description']['short'] = $form.find('input[name="short_description"]').val();
				form['description']['long'] = $form.find('textarea[name="description"]').val();
				form['multiple'] = $form.find('input[name="multiple"]').is(":checked");
				$form.find('input[name="endedness"]').each(function() {
					if($(this).is(":checked")) {
						form['endedness'] = $(this).val();
					}
				});
				var do_type = true;
				if(form['endedness'] == 'enumerated') {
					$form.find('input[name="enum_fetch"]').each(function() {
						if($(this).is(":checked")) {
							var val = $(this).val();
							if(val == 'bool') {
								form['type'] = 'bool';
								do_type = false;
							}
							else {
								form['fetch'] = val.substring(val.lastIndexOf('_') + 1) == 'download';
								do_type = form['fetch'] == false;
							}
						}
					});
				}
				if(do_type) {
					$form.find('input[name="type_question"]').each(function() {
						if($(this).is(":checked")) {
							if($(this).val() == 'number') {
								form['type'] = 'double';
								var result = $('#number_default_class').myemslInputPlusFinder('selection');
								if(result) {
									form['number_class'] = {};
									form['number_class']['default'] = result['val'];
									form['number_class']['type'] = result['type'];
									number_default_type = result['key'];
								}
							}
							if($(this).val() == 'string') {
								form['type'] = 'string';
								form['string_case_sensitive'] = $form.find('input[name="case_sensitive"]').is(':checked');
								form['string_word_split'] = $form.find('input[name="common_splitting"]').is(':checked');
							}
							if($(this).val() == 'time') {
								form['type'] = 'time';
								form['time_class'] = [];
								var list = ['year', 'month', 'day', 'hour', 'minute', 'second'];
								for(var i in list) {
									if($('#demoForm').find('input[name="date_' + list[i] + '"]').is(":checked")) {
										form['time_class'].push(list[i]);
									}
								}
							}
							else {
								form['type'] = $(this).val();
							}
						}
					});

				}
				if(form['endedness'] == 'enumerated' && form['fetch'] == false && form['type'] != 'bool') {
					form['values'] = [];
					$form.find('.form_user_value').each(function() {
						var name = $(this).attr('name');
						var friend = 'form_value_' + name.substr(name.lastIndexOf("_") + 1);
						form['values'].push({
							'user': $(this).val(),
							'system': $form.find('input[name="' + friend + '"]').val()
						});

					});
					if(form['values'].length == 0) {
						delete form['values'];
					}
				}
				var td = $(this).data('myemslPredicateWizard');
				td['form'] = form;
				console.log(form);

				$('.result_short_description').text(form['description']['short']);
				$('.result_long_description').text(form['description']['long']);
				$('.result_multiple').text(form['multiple']);
				$('.result_endedness').text(form['endedness']);
				$('.result_fetch').text('fetch' in form && form['fetch']);
				$('.result_values').html('');
				if(form['endedness'] == 'enumerated') {
					if('values' in form) {
						$('.result_values').prepend('<tr><td>User Value</td><td>System Value</td></tr>');
						for(var i = 0; i < form['values'].length; i++) {
							var row = $('<tr><td class="user_value"></td><td class="system_value"></td></tr>');
							row.find('.user_value').text(form['values'][i]['user']);
							row.find('.system_value').text(form['values'][i]['system']);
							row.appendTo('.result_values');
						}
					}
				}
				if('number_class' in form) {
					$('.result_number_class_default').text(number_default_type);
					$('.result_number_class_type').text(form['number_class']['type']);
					$('.result_number_class').show();
				}
				else {
					$('.result_number_class').hide();
				}
			}
		});
		target.find('.myemsl_predicate_wizard_form_item_add').removeClass('ui-formwizard-button');
		var form_value_ids = 2;
		target.find('.myemsl_predicate_wizard_form_item_add').button({
			icons: {
				primary: "ui-icon-plus"
			},
			text: true
		}).click(function() {
			var $row = $('<tr><td><input type="text" class="text_value ui-wizard-content ui-helper-reset ui-state-default"/></td><td><input type="text" class="value ui-wizard-content ui-helper-reset ui-state-default"></td><td><span class="form_value_row_remove">&nbsp;</span></td></tr>');
			datatypepicker($row.find('.value'))
			$row.find('.form_value_row_remove').button({
				icons: {
					primary: "ui-icon-minus"
				},
				text: false
			}).click(function($row) {return function() {
				$row.remove();
			}}($row));
			$row.find('.text_value').each(function() {
				$(this).addClass('myemsl_predicate_wizard_form_user_value').attr('name', 'form_text_value_' + form_value_ids);
			});
			$row.find('.value').each(function() {
				$(this).addClass('myemsl_predicate_wizard_form_system_value').attr('name', 'form_value_' + form_value_ids);
			});
			$row.appendTo('#form_container');
			form_value_ids += 1;
			return false;
		});
		$('#number_default_class').myemslInputPlusFinder({'widget': 'unit'});
	}
};
}));
