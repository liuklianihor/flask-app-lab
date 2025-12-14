from flask import render_template, request, url_for, redirect, flash, current_app, session
from datetime import datetime
from . import post_bp
from .forms import PostForm
from .models import Post, Tag
from app.users.models import User
from app import db
from sqlalchemy import select


@post_bp.route('/', methods=['GET'])
def list_posts():
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('posts/all_posts.html', posts=posts)


@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    tags = db.session.scalars(select(Tag).order_by(Tag.id)).all()
    form.tags.choices = [(t.id, t.name) for t in tags]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=True,
            user_id=form.author_id.data
        )

        if form.publish_date.data:
            post.posted = form.publish_date.data
        else:
            post.posted = datetime.utcnow()

        selected_tag_ids = form.tags.data
        if selected_tag_ids:
            post.tags = db.session.scalars(
                select(Tag).where(Tag.id.in_(selected_tag_ids))
            ).all()

        db.session.add(post)
        db.session.commit()
        flash("Post створено", "success")
        return redirect(url_for('posts.view_post', id=post.id))
    return render_template('posts/add_post.html', form=form, action="Create")


@post_bp.route('/<int:id>', methods=['GET'])
def view_post(id):
    post = db.get_or_404(Post, id)
    return render_template('posts/detail_post.html', post=post)


@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.category.data = post.category

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = bool(form.enabled.data)
        if form.publish_date.data:
            post.posted = form.publish_date.data
        db.session.commit()
        flash("Post оновлено", "success")
        return redirect(url_for('posts.view_post', id=post.id))
    return render_template('posts/add_post.html', form=form, action="Update")


@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post видалено", "success")
        return redirect(url_for('posts.list_posts'))
    return render_template('posts/delete_confirm.html', post=post)
