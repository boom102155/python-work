// script table
$(document).ready(function() {
	$('#example').DataTable();			
	$('#example tbody').on('click', 'tr', 'td', function () {
	    $("#myModal").modal("show");
	    $("#txtID").val($(this).closest('tr').children()[0].textContent);
	    $("#txtEquipname").val($(this).closest('tr').children()[1].textContent);
	    $("#cateID").val($(this).closest('tr').children()[3].textContent);
	    $("#sCategory").val($(this).closest('tr').children()[3].textContent);
	    $("#txtCallnumber").val($(this).closest('tr').children()[4].textContent);
	    $("#txtSerial").val($(this).closest('tr').children()[5].textContent);
	    $("#txtDate").val($(this).closest('tr').children()[6].textContent);
    });
});
	        			


