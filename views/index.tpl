<!DOCTYPE html>

<html>
<head>
<!-- Place this tag in your head or just before your close body tag. -->
<script async defer src="https://buttons.github.io/buttons.js"></script>
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
<style>
main {
	width:800px;
	margin:auto;
	min-height:200px;
}
section {
	margin-bottom:10px;
}
</style>
</head>
<body onload="func();">
<main>
<section>
<h1>AtCoder Problem Recommender</h1>
<p>AtCoderの問題を推薦するレコメンダーです。AtCoderのIDを入力してください。</p>
<form id="form" action="/recommend/" method="GET">
<p>AtCoder ID:</p>
<input id="id" name="target">
<input type="button" value="送信" onClick="location.href='http://sandbox.ugwis.net/recommend/' + document.forms.form.id.value;">
</form>
</section>
<section>
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/ugwis/AtCoder-Recommendation" data-style="mega" data-count-href="/ugwis/AtCoder-Recommendation/stargazers" data-count-api="/repos/ugwis/AtCoder-Recommendation#stargazers_count" data-count-aria-label="# stargazers on GitHub" aria-label="Star ugwis/AtCoder-Recommendation on GitHub">Star</a>
</section>
</main>
</body>
</html>
