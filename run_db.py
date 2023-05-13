from backend import create_app

from sqlalchemy.orm import sessionmaker

from backend.model import User, Image, Caption, Tag, engine, Favourite

# create_app just one time
app = create_app()

Session = sessionmaker(bind=engine)
session = Session()

# Thêm một user mới
new_user = User(name='John Doe', email='johndoe@example.com')
session.add(new_user)
session.commit()

# Thêm một image mới
new_image = Image(image_url='https://example.com/image.jpg', user=new_user)
session.add(new_image)
session.commit()

# Thêm một caption mới cho ảnh
new_caption = Caption(caption_text='This is a caption', image=new_image, user=new_user)
session.add(new_caption)
session.commit()

# Thêm một tag mới cho caption
new_tag = Tag(tag_text='tag1')
new_caption.tags.append(new_tag)
session.commit()

# Lấy tất cả các captions
captions = session.query(Caption).all()
for caption in captions:
    print(caption.caption_text, caption.image.image_url)

# Đánh dấu một caption là yêu thích của một user
new_favourite = Favourite(caption=new_caption, user=new_user)
session.add(new_favourite)
session.commit()

# Lấy các caption đã được đánh dấu yêu thích của một user
favourites = session.query(Favourite).filter_by(user_id=new_user.id).all()
for favourite in favourites:
    print(favourite.caption.caption_text)

# Xóa một user
session.delete(new_user)
session.commit()

# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False, host="0.0.0.0", port="5000")
