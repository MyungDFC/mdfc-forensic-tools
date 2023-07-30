import json
import requests
import math

from flask import Blueprint, render_template, request
from bs4 import BeautifulSoup

from config import tistory_api_token

bp = Blueprint("blog", __name__, url_prefix="/blog")

def pagination(records: list[dict], page: int, per_page: int):
    """
        This function returns a list of dict(json) data for the current page.
        :param records: list of dict(json) data
        :param page: current page number
        :param per_page: number of items per page
    """
    BLOCK_SIZE = 5  # number of pages in the navigation block

    # Pagination
    start = (page - 1) * per_page  # first item to display on this page
    end = start + per_page  # last item to display on this page
    items_on_page = records[start:end]  # items to display on this page

    total = len(records)  # total number of items in the list
    last_page = math.ceil(total / per_page)  # last page number

    block_num = int((page - 1) / BLOCK_SIZE)  # current block number
    block_start = int((BLOCK_SIZE * block_num) + 1)  # first page number in the block (1, 6, 11, ...
    block_end = math.ceil(block_start + (BLOCK_SIZE - 1))  # last page number in the block

    if block_end > last_page:
        block_end = last_page

    return items_on_page, total, last_page, block_start, block_end

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
                    "title": item["title"],
                    "postUrl": item["postUrl"],
                    "date": item["date"],
                }
            )

    for post in posts:
        post_url = f"https://www.tistory.com/apis/post/read?access_token={tistory_api_token}&output=json&blogName={blog_name}&postId={post['id']}"

        post_response = json.loads(requests.get(post_url).text)
        content = post_response["tistory"]["item"]["content"]

        soup = BeautifulSoup(content, "html.parser")
        img_tag = soup.find("img")
        post["thumbnail"] = img_tag["src"]
            
    # Pagination variables
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=6, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(posts, page, per_page)


    return render_template(
        "page/blog/main.jinja-html",
        posts=items_on_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
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

