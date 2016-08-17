<!DOCTYPE html>

<html>
<head>
<script type="text/javascript">
<!--
var getUrlVars = function(){
    var vars = {}; 
    var param = location.search.substring(1).split('&');
    for(var i = 0; i < param.length; i++) {
        var keySearch = param[i].search(/=/);
        var key = '';
        if(keySearch != -1) key = param[i].slice(0, keySearch);
        var val = param[i].slice(param[i].indexOf('=', 0) + 1);
        if(key != '') vars[key] = decodeURI(val);
    } 
    return vars; 
}
function func(){
	var vars = getUrlVars();
	console.log(vars);
	if('target' in vars){
		location.href="http://sandbox.ugwis.net/recommend/" + vars.target;
	}
}
-->
</script>
</head>
<body onload="func();">
<form id="form" action="/recommend/" method="GET">
<p>AtCoder ID:</p>
<input id="id" name="target">
<input type="button" value="送信" onClick="location.href='http://sandbox.ugwis.net/recommend/' + document.forms.form.id.value;">
</form>
</body>
</html>
