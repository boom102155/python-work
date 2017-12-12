$(document).ready(function() {
	$('#example').DataTable();			
	$('#example tbody').on('click', 'tr', 'td', function () {
	    $("#myModal").modal("show");
	    $("#txtID").val($(this).closest('tr').children()[0].textContent);
	    $("#txtEquipname").val($(this).closest('tr').children()[1].textContent);
	    $("#sCategory").val($(this).closest('tr').children()[2].textContent);
	    $("#txtCallnumber").val($(this).closest('tr').children()[3].textContent);
	    $("#txtSerial").val($(this).closest('tr').children()[4].textContent);
	    $("#txtDate").val($(this).closest('tr').children()[5].textContent);
    });
});