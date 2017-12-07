$(document).ready(function() {
	var table = $('#example').DataTable();
	$('#example tbody').on('click', 'tr', 'td', function () {
        $("#myModal").modal("show");
        $("#txtDate").val($(this).closest('tr').children()[0].textContent);
	    $("#txtName").val($(this).closest('tr').children()[1].textContent);
	    $("#txtSurname").val($(this).closest('tr').children()[2].textContent);
	    $("#sFaculty").val($(this).closest('tr').children()[3].textContent);
	    $("#sClass").val($(this).closest('tr').children()[4].textContent);
	    $("#txtSerial").val($(this).closest('tr').children()[5].textContent);
	    $("#txtEquipment").val($(this).closest('tr').children()[6].textContent);
    } );
} );