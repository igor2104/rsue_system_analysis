jQuery(document).ready(function($) {

	$('.group-name').on('click', '.btn-edit-group, .btn-cancel-group', function(event) {
		event.preventDefault();
		var name = $('.group-name-show');
		var form = $('.group-name-edit');

		if(name.hasClass('d-none')){
			name.removeClass('d-none');
			form.addClass('d-none');
			return;
		}

		name.addClass('d-none');
		form.removeClass('d-none');
		form.find('input[type="text"]').val(name.find('.name').text())
	});

	$('.form-save').on('click', '.btn-add, .btn-cancel', function(event) {
		event.preventDefault();

		var prefix = event.delegateTarget.dataset.prefix;
		var form_idx = $('#id_'+prefix+'-TOTAL_FORMS').val();

		if($(event.target).hasClass('btn-add'))
		{
			var empty_element = $(event.delegateTarget).find('.empty-element').clone();

			$(empty_element).removeClass('d-none').removeClass('empty-element');

			var new_empty_element = empty_element[0].outerHTML.replace(/__prefix__/g, form_idx);
			$(event.delegateTarget).find('.content-replace').append(new_empty_element);
			$('#id_'+prefix+'-TOTAL_FORMS').val(parseInt(form_idx) + 1);

			return;
		}

		$('.tooltip').tooltip('hide');
		$(event.target).parents('.element').remove();
		$('#id_'+prefix+'-TOTAL_FORMS').val(parseInt(form_idx) - 1);
	});

	$('.object-function').on('change', 'input[type="checkbox"]', function(event) {
		event.preventDefault();
		if(this.checked){
			$(this).parent().addClass('bg-success');
			return;
		}

		$(this).parent().removeClass('bg-success');
	});

	$('.group-name-form').on('submit', function(event) {
		event.preventDefault();
		var form = $(this);
		$.ajax({
			type: this.method,
			url: this.action,
			data: $(this).serialize(),
			success: function(data){
				form.find('.group-name').html(data.html);
				$('.tooltip').tooltip('hide');

				alert_show(alert_save);
			},
			error: function (jqXHR, exception){
				form.find('.group-name').html(jqXHR.responseJSON.html);
				$('.tooltip').tooltip('hide');
				alert_show(alert_error);
			}
		});
	});

	$('.form-save').on('submit', function(event) {
		event.preventDefault();

		var content_replace = $(this).find('.content-replace');

		var relation = $('.object-function');

		$.ajax({
			type: this.method,
			url: this.action,
			data: $(this).serialize(),
			success: function(data){
				$('.tooltip').tooltip('hide');

				if(data.hasOwnProperty('form_html')){
					content_replace.html(data.form_html);
				}

				if(data.hasOwnProperty('relation')){
					relation.html(data.relation);
				}

				alert_show(alert_save);
			},
			error: function (jqXHR, exception){
				$('.tooltip').tooltip('hide');

				if(jqXHR.responseJSON.hasOwnProperty('form_html')){
					content_replace.html(jqXHR.responseJSON.form_html);
				}

				if(jqXHR.responseJSON.hasOwnProperty('relation')){
					relation.html(jqXHR.responseJSON.relation);
				}

				alert_show(alert_error);
			}
		});
	});

	$('.form-delete').on('click', '.btn-delete', function(event) {
		event.preventDefault();

	});
});