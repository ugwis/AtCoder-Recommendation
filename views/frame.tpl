<!DOCTYPE html>
<html>
	<head>
		<title>{{userid}}</title>
		<!-- Place this tag in your head or just before your close body tag. -->
		<script async defer src="https://buttons.github.io/buttons.js"></script>
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
	<a href="https://twitter.com/share" class="twitter-share-button" data-url="http://sandbox.ugwis.net/recommend/" data-text={{shareText}} data-size="large">Tweet</a>
	<script>
		!function(d,s,id){
			var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
			if(!d.getElementById(id)){
				js=d.createElement(s);
				js.id=id;
				js.src=p+'://platform.twitter.com/widgets.js';
				fjs.parentNode.insertBefore(js,fjs);
			}
		}(document, 'script', 'twitter-wjs');
	</script>
	<!-- Place this tag where you want the button to render. -->
	<a class="github-button" href="https://github.com/ugwis/AtCoder-Recommendation" data-style="mega" data-count-href="/ugwis/AtCoder-Recommendation/stargazers" data-count-api="/repos/ugwis/AtCoder-Recommendation#stargazers_count" data-count-aria-label="# stargazers on GitHub" aria-label="Star ugwis/AtCoder-Recommendation on GitHub">Star</a>
	</body>
</html>
