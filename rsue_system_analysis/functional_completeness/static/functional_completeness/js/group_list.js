jQuery(document).ready(function($) {

	$('.group-form').on('click', '.btn-add-group', function(event) {
		event.preventDefault();
		var form = $(this).prev('form');

		if(!form.hasClass('d-none'))
			return;

		form.removeClass('d-none');
	});

	$('.group-form').on('click', '.btn-cancel-group', function(event) {
		event.preventDefault();

		var form = $(this).parents('form');
		form.find('input[type=text]').val("");
		form.addClass('d-none');
		form.find('ul.errorlist').remove();
	});

	$('.group-form').on('submit', '.form-group-add', function(event) {
		event.preventDefault();

		$.ajax({
			type: this.method,
			url: this.action,
			data: $(this).serialize(),
			success: function(data){
				$('.group-list').append(data.html);
				$('.group-form .btn-cancel-group').trigger('click');

				alert_show(alert_add);
			},
			error: function (jqXHR, exception){
				$('.group-form .dynamic-form').html(jqXHR.responseJSON.html);

				alert_show(alert_error);
			}
		});
	});

	$('.group-list').on('submit', '.form-group-delete', function(event) {
		event.preventDefault();

		var parent = $(this).parents('.group-element');
		var modal = $(this).parents('.modal');

		$.ajax({
			type: this.method,
			url: this.action,
			data: $(this).serialize() + "&csrfmiddlewaretoken=" + getCookie('csrftoken'),
			success: function(data){
				console.log('delete success');
				modal.modal('hide');
				parent.remove();

				alert_show(alert_delete);
			},
			error: function (jqXHR, exception){
				console.log('delete error');
				alert_show(alert_error);
			}
		});
	});
});