from flask import Flask, render_template, request, flash
import time, os
from searcher import search
from glob import glob
from flask_paginate import Pagination, get_page_args
app=Flask(__name__)

def getUsers(urls, offset=0, per_page=10):
    return urls[offset: offset + per_page]

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search")
def searchResult():
    query = request.args.get('query')
    urls = [''] * 5
    searchEni = search(glob(os.path.join("indexFile", "*TokenDocId.txt"))[0])
    if query != None and query!= "":
        start = time.time()
        try:
            urls = searchEni.start(query)
        except:
            urls = [''] * 5
        searchTime = time.time() - start
        flash(f"Searching completed in {round(searchTime, 5)} seconds.")

    # add pagination
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_urls = getUsers(urls, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=len(urls), alignment="center",
                            css_framework='bootstrap4')

    query = "Enter here" if query == None else query
    return render_template("searchResult.html",
        query=query, 
        urls=pagination_urls,
        page=page,
        per_page=per_page,
        pagination=pagination)


if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=2021,host="127.0.0.1",debug=True)
