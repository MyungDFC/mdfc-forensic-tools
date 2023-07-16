import json
import requests
from flask import Blueprint, render_template

from config import tistory_api_token

bp = Blueprint("blog", __name__, url_prefix="/blog")

@bp.route("/")
def main():
    """
    [blog_info]
    id: 'm_dfc@naver.com'
    userId: '4988679'
    blogs: [
        {
            name: 'myung-dfc',
            url: 'https://myung-dfc.tistory.com',
            nickname: 'Myung_DFC',
            title: '명디지털포렌식센터(Myung Digital Forensic Center)',
            blogId: '4845051',
        }
    ]
    """

    blog_name = "myung-dfc"
    posts = []
    page = 1

    while True:
        postlist_url = f"https://www.tistory.com/apis/post/list?access_token={tistory_api_token}&output=json&blogName={blog_name}&page={page}"

        postlist_response = json.loads(requests.get(postlist_url).text)
        postlist = postlist_response["tistory"]["item"].get("posts", "")

        if postlist:
            page += 1
        else:
            break

        for item in postlist:
            posts.append(
                {
                    "id": item["id"],
                    "postUrl": item["postUrl"],
                    "title": item["title"],
                    "date": item["date"],
                }
            )

    return render_template(
        "page/blog/main.jinja-html",
        posts=posts
    )

@bp.route("/<int:post_id>")
def post(post_id):
    blog_name = "myung-dfc"

    post_url = f"https://www.tistory.com/apis/post/read?access_token={tistory_api_token}&output=json&blogName={blog_name}&postId={post_id}"

    post_response = json.loads(requests.get(post_url).text)
    post = post_response["tistory"]["item"]

    return render_template(
        "page/blog/post.jinja-html",
        post_title=post["title"],
        post_url=post["postUrl"],
        post_content=post["content"],
        post_date=post["date"],
    )

