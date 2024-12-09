
from django.urls import path
from post.views import home,NewPost,PostDetails,tags,like,favorite,homeLikes,savePost,update_post,deletePost,like_post,unlike_post,search_users,post_save,post_unsave


urlpatterns = [
   	path('', home, name='home'),
   	path('upload/', NewPost, name='upload'),
   	path('<uuid:post_id>/update', update_post, name='update_post'),
   	path('<uuid:post_id>/delete', deletePost, name='deletePost'),
   	path('homeLikes/', homeLikes, name='homelikes'),
   	path('<uuid:post_id>', PostDetails, name='postdetails'),
   	path('<uuid:post_id>/like', like, name='postlike'),
   	path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
   	path('<uuid:post_id>/savePost', savePost, name='savePost'),
   	path('tag/<slug:tag_slug>', tags, name='tags'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('unlike/<int:post_id>/', unlike_post, name='unlike_post'),
    path('search/', search_users, name='search_users'),
    path('post/<uuid:post_id>/save/', post_save, name='post_save'),
    path('post/<uuid:post_id>/unsave/', post_unsave, name='post_unsave'),
    ]