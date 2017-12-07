$(document).ready(function() {
	var table = $('#example').DataTable();
	$('#example tbody').on('click', 'tr', 'td', function () {
        $("#myModal").modal("show");
        $("#txtID").val($(this).closest('tr').children()[0].textContent);
        $("#txtCatename").val($(this).closest('tr').children()[1].textContent);
        $("#txtShortname").val($(this).closest('tr').children()[2].textContent);
	    $("#txtType").val($(this).closest('tr').children()[3].textContent);
	    $("#txtDescription").val($(this).closest('tr').children()[4].textContent);
	    $("#txtDate").val($(this).closest('tr').children()[5].textContent);
    });		    
});