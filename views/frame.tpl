<!DOCTYPE html>
<html>
	<head>
		<title>{{userid}}</title>
	</head>
	<body style="margin:0px;">
		<h2>{{userid}}さんへのお勧め問題</h2>
		<h3>Easy Problem</h3>
		<ol>
		%for k in easy:
			<li><a href={{k['url']}} target="_blank">{{k['title']}}</a></li>
		%end
		</ol>

		<h3>Medium Problem</h3>
		<ol>
		%for k in medium:
			<li><a href={{k['url']}} target="_blank">{{k['title']}}</a></li>
		%end
		</ol>

		<h3>Hard Problem</h3>
		<ol>
		%for k in hard:
			<li><a href={{k['url']}} target="_blank">{{k['title']}}</a></li>
		%end
		</ol>
	</body>
</html>
