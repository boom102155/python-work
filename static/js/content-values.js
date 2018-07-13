$(document).ready(function() {

  var cur = $('.today').val();
  var day = cur.slice(0, 2);
  var month = cur.slice(3, 5);
  var year = cur.slice(6);
  var conyeartoint = parseInt(year);
  $('#cont2').text(day);
  $("#cont2-1").text(month);
  $("#cont2-2").text((conyeartoint + 543));

	$("#writewhere").keyup(function() {
    	var value = $('#writewhere').val();
    	$("#cont1").text(value);
  	}).keyup();

  $('.today').change(function () {
      var value = $('.today').val();
      var day = value.slice(0, 2);
      var month = value.slice(3, 5);
      var year = value.slice(6);
      var conyeartoint = parseInt(year);
      $("#cont2").text(day);
      $("#cont2-1").text(month);
      $("#cont2-2").text((conyeartoint + 543));
  });

	$("#name").keyup(function() {
  	var value = $('#name').val();
  	$("#cont3").text(value);
	}).keyup();

	$("#position").keyup(function() {
  	var value = $('#position').val();
  	$("#cont4").text(value);
	}).keyup();

	$("#department").keyup(function() {
  	var value = $('#department').val();
  	$("#cont5").text(value);
	}).keyup();

	$("#totalday").keyup(function() {
  	var value = $('#totalday').val();
  	$("#cont6").text(value);
	}).keyup();

	$("#availableday").keyup(function() {
  	var value = $('#availableday').val();
  	$("#cont7").text(value);
	}).keyup();

	$("#dayresult").keyup(function() {
  	var value = $('#dayresult').val();
  	$("#cont8").text(value);
	}).keyup();

  $('.fromdate').change(function () {
      var value = $('.fromdate').val();
      var day = value.slice(0, 2);
      var month = value.slice(3, 5);
      var year = value.slice(6);
      var conyeartoint = parseInt(year);
      $("#cont9").text(day + "/" + month + "/" + (conyeartoint + 543));
  });

  $('.todate').change(function () {
      var value = $('.todate').val();
      var day = value.slice(0, 2);
      var month = value.slice(3, 5);
      var year = value.slice(6);
      var conyeartoint = parseInt(year);
      $("#cont10").text(day + "/" + month + "/" + (conyeartoint + 543));

      var dateresultvalue = $('.dateresult').val();
      $("#cont11").text(dateresultvalue);
  });

	$("#contact").keyup(function() {
  	var value = $('#contact').val();
  	$("#cont12").text(value);
	}).keyup();

  $('#contact').on('keyup',function(){
    var input = $(this);
    input.next('.textlength').text(input.val().length + "/80 ตัวอักษร");
  });

	$("#phonenumber").keyup(function() {
  	var value = $('#phonenumber').val();
  	$("#cont13").text(value);
	}).keyup();

  $('#phonenumber').on('keyup',function(){
    var input = $(this);
    input.next('.numberlength').text(input.val().length + "/10 ตัวอักษร");
  });   
});