#!/usr/bin/python
# -*- coding: UTF-8 -*-
import web
import json
from urllib.request import urlopen
web.config.debug = True
render = web.template.render('templates/')
# enter your youtube api key here
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
        youtube_data = urlopen('https://www.googleapis.com/youtube/v3/search?key={}&channelId=UColI-lvoN08jXBfc1EqDR8g&part=snippet,id&order=date&maxResults=11'.format(youtubeKey))
        youtube_json = youtube_data.read()
        data = json.loads(youtube_json)
        
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
        data["items"].pop(0)
        for i, item in enumerate(data["items"]):
            output += """<div class="video">
                <a href="https://www.youtube.com/watch?v={0}" target="_blank" title="view via youtube: {1}">
                    <img alt="{1}" width="196" src="https://i.ytimg.com/vi/{0}/mqdefault.jpg" />
                </a>
                <br />
                <a href="https://www.youtube.com/watch?v={0}" target="_blank">{1}</a>
            </div>""".format(item["id"]["videoId"], item["snippet"]["title"].encode('unicode-escape'))

        output += """
              </div>
              <p class="text-center"><a class="text-center" href="https://www.youtube.com/DSHelmondGames" target="_blank">want to see more videos?</a></p>
            </div>
            <hr>
        
        """
        return render.base("Videos", "videos", output)


def notfound():
    return web.notfound(render.base("404 not found", "404 not found",
                                    "<p class=\"text-center\">Your requested page could not be found</p>"))


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    app.notfound = notfound
    app.run()

