from flask import Flask, render_template, abort, g, Blueprint
import yaml

data_dir = "data-example/"

app = Flask(__name__)

comic_ids = yaml.load(open(data_dir+"comics.yaml"))
comics = {}

for comic_id in comic_ids:
    comics[comic_id] = yaml.load(open(data_dir+comic_id+"/comic.yaml"))
    blueprint = Blueprint(comic_id, __name__, static_url_path='/{}/img/', static_folder=data_dir+comic_id+"/img")
    app.register_blueprint(blueprint)

@app.before_request
def before_request():
    g.comic_ids = comic_ids
    g.comics = comics

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/<comic_id>/')
def comic(comic_id):
    if comic_id not in comics:
        abort(404)
    
    comic = comics[comic_id]
    
    return render_template("comic.html", comic=comic)

@app.route('/<comic_id>/<page>')
def page(comic_id, page):
    if comic_id not in comics: abort(404)
    
    comic = comics[comic_id]
    
    if page not in comic['pages']: abort(404)
    #page = comic['pages'].find[page]
    pagei = comic['pages'].index(page)
    prev = comic['pages'][pagei-1] if pagei > 0 else None
    next = comic['pages'][pagei+1] if pagei < len(comic['pages'])-1 else None
    
    return render_template("page.html", comic=comic, page=page, prev=prev, next=next)

if __name__ == '__main__':
    app.run(debug=True)
