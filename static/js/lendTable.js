$(document).ready(function() {
	$('#example tbody').on('click', 'tr', 'td', function () {
        $("#myModal").modal("show");
        $("#txtLendNO").val($(this).closest('tr').children()[1].textContent);
        $("#txtDate").val($(this).closest('tr').children()[2].textContent);
	    $("#txtName").val($(this).closest('tr').children()[3].textContent);
	    $("#txtSurname").val($(this).closest('tr').children()[4].textContent);
	    $("#txtType").val($(this).closest('tr').children()[5].textContent);
	    $("#sFaculty").val($(this).closest('tr').children()[6].textContent);
	    $("#sClass").val($(this).closest('tr').children()[7].textContent);

	    $("#txtILendNO").val($(this).closest('tr').children()[1].textContent);
	    $("#txtEID").val($(this).closest('tr').children()[8].textContent);
	    $("#txtIeid").val($(this).closest('tr').children()[8].textContent);
	    $("#txtSerial").val($(this).closest('tr').children()[9].textContent);
	    $("#txtEquipment").val($(this).closest('tr').children()[10].textContent);
    });		
});


