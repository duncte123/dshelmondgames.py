#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web, urllib2, json
web.config.debug = True
render = web.template.render('templates/')
youtubeKey = ""
urls = (
    '/', 'index',
    '/home', 'index',
    '/videos', 'videos'
)

class index:
    def GET(self):
        with open ("templates/index.html", "r") as myfile:
            data = myfile.read()
	    return render.base("Home", "home", data)

class videos:
    def GET(self):
        youtubeData = urllib2.urlopen('https://www.googleapis.com/youtube/v3/search?key={}&channelId=UColI-lvoN08jXBfc1EqDR8g&part=snippet,id&order=date&maxResults=11'.format(youtubeKey))
        youtubeJSON = youtubeData.read()
        data = json.loads(youtubeJSON)
        
        output = """<div class="container">
            <div class="row text-center">
                <div class="col-md-6 col-md-offset-3">Welcome to a collection of my latest videos.<br />You can find them on <a href="https://www.youtube.com/DSHelmondGames">youtube</a> if you want.</div>
            </div>
            <hr>
            <div class="row">
              <h2 class="text-center" style="margin: 10px auto;">Latest video</h2>
              <div id="latVid"><div class="container" style="max-width: 600px;">
                <div class="embed-responsive embed-responsive-16by9">
                    <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{}" allowfullscreen></iframe>
                </div>
            </div></div>
              <br /><br /><br /><br /><div id="videosList" class="text-center">""".format(data["items"][0]["id"]["videoId"])
        for i, item in enumerate(data["items"]):
            output += """<div class="video">
                <a href="https://www.youtube.com/watch?v={}" target="_blank" title="view via youtube: {}">
                    <img alt="{}" width="196" src="https://i.ytimg.com/vi/{}/mqdefault.jpg" />
                </a>
                <br />
                <a href="https://www.youtube.com/watch?v={}" target="_blank">{}</a>
            </div>""".format(item["id"]["videoId"], item["snippet"]["title"], item["snippet"]["title"], item["id"]["videoId"], item["id"]["videoId"], item["snippet"]["title"])

        output += """
              </div>
              <p class="text-center"><a class="text-center" href="https://www.youtube.com/DSHelmondGames" target="_blank">want to see more videos?</a></p>
            </div>
            <hr>
        
        """


        return render.base("Videos", "videos", output)


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    app.run()

