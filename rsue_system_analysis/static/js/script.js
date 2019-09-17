function isTouchDevice() {
	return true == ("ontouchstart" in window || window.DocumentTouch && document instanceof DocumentTouch);
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


function makeUniqueId(){
	var counter = 0;
	return uniqueId = function(){
		return 'alert-'+ counter++
	}
};

window.uniqueId = makeUniqueId();

window.alert_save = `
	<div class="alert alert-success alert-dismissible fade show" role="alert" id='{0}'>
		<strong>Сохранено</strong>
		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		</button>
	</div>`;

window.alert_add = `
	<div class="alert alert-primary alert-dismissible fade show" role="alert" id='{0}'>
		<strong>Добавлено</strong>
		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		</button>
	</div>`;

window.alert_delete = `
	<div class="alert alert-danger alert-dismissible fade show" role="alert" id='{0}'>
		<strong>Удалено</strong>
		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		</button>
	</div>`;

window.alert_error = `
	<div class="alert alert-danger alert-dismissible fade show" role="alert" id='{0}'>
		<strong>Ошибка</strong>
		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			<span aria-hidden="true">&times;</span>
		</button>
	</div>`;


function remove_alert(id) {
	window.alert_container.find('#'+id).remove();
}

window.alert_show = function(alert){
	id = window.uniqueId();

	alert_container.append(alert.replace('{0}', id));
	setTimeout(remove_alert, 3000, id);
}


jQuery(document).ready(function($) {
	window.alert_container = $('#alert-container');
	var suportTouch = isTouchDevice();

	document.documentElement.className += (suportTouch ? ' touch' : ' no-touch');

	if(!suportTouch) {
		$('.content').tooltip({
			trigger: 'hover',
			animation: false,
			container: 'body',
			selector: '[data-toggle="tooltip"], [data-tooltip="tooltip"]'
		});
	}
});