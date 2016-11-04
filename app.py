from flask import Flask, render_template, abort, g, Blueprint
import werkzeug.utils
import yaml
from enum import Enum

app = Flask(__name__)


app.config.from_object('config-example')

try:
    app.config.from_object('config')
except werkzeug.utils.ImportStringError:
    print("No config present: using example config.")

class Location(Enum):
    single = 0
    left = 1
    right = 2

comic_ids = yaml.load(open(app.config['DATA_DIR']+"comics.yaml"))
comics = {}

for comic_id in comic_ids:
    comics[comic_id] = yaml.load(open(app.config['DATA_DIR']+comic_id+"/comic.yaml"))
    blueprint = Blueprint(comic_id, __name__, static_url_path='/{}/img'.format(comic_id), static_folder=app.config['DATA_DIR']+comic_id+"/img")
    app.register_blueprint(blueprint)

def get_page_by_id(comic, page_id):
    page = None
    for i, p in enumerate(comic['pages']):
        if page_id == p['id']:
            pagei = i
            page = p
            break
    if page:
        return pagei, page
    else:
        return None

def get_page_physical_location(comic, page_id):
    current = None
    #for i, p in enumerate(comic['pages']):
    #    if comic['pages'] == 

@app.before_request
def before_request():
    g.comic_ids = comic_ids
    g.comics = comics
    g.sitename = app.config['SITENAME']
    g.debug = app.config['DEBUG']

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/<comic_id>/')
def comic(comic_id):
    if comic_id not in comics:
        abort(404)
    
    comic = comics[comic_id]
    
    return render_template("comic.html", comic=comic)

@app.route('/<comic_id>/<page_id>')
@app.route('/<comic_id>/<page_id>+<page2_id>')
def page(comic_id, page_id, page2_id=None):
    if comic_id not in comics: abort(404)
    
    comic = comics[comic_id]
    
    double = False
    pages = []
    pages.append(get_page_by_id(comic, page_id))
    if page2_id:
        pages.append(get_page_by_id(comic, page2_id))
        double = True
    
    page = pages[0][1]
    pagei = pages[0][0]
    
    if not page: abort(404)
    
    prev = comic['pages'][pagei-1] if pagei > 0 else None
    next = comic['pages'][pagei+1] if pagei < len(comic['pages'])-1 else None
    
    return render_template("page.html", comic=comic, page=page, prev=prev, next=next)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8002, threaded=True, debug=True)
