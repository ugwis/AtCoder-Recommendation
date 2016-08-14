<!DOCTYPE html>
<html>
	<head>
		<title>{{userid}}</title>
	</head>
	<body style="margin:0px;">
		<h2>{{userid}}さんへのお勧め問題</h2>
		<h3>Easy Problem</h3>
		%for k in easy:
			<a href={{k}}>{{k}}</a>
		%end
		<h3>Medium Problem</h3>
		<h3>Hard Problem</h3>
	</body>
</html>
