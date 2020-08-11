jQuery(document).ready(function() {
	$('#delModal').on('show.bs.modal', function(e) {
		let threadId = $(e.relatedTarget).data('thread-id');
		$(e.currentTarget).find('input[name="tid"]').val(threadId);
		let datasetName = $(e.relatedTarget).data('dataset-name');
		$(e.currentTarget).find('input[name="dname"]').val(datasetName);
	});
});

function delNotify(){
    let thread_id = $('#tid').val();
    let d_name = $('#dname').val();
    let $form = document.createElement('form');
    $form.setAttribute('id', 'data_form');
    $form.setAttribute('action', `/dataset/list/${thread_id}/${d_name}/delete`);
    $form.setAttribute('method', 'post');
    document.body.appendChild($form);
    $form.submit();
	document.body.removeChild($form);
}