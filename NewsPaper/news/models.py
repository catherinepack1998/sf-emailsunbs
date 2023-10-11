from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    rating = models.SmallIntegerField(default=0)
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return self.authorUser.first_name

class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)
    subscribes = models.ManyToManyField(User, through='CategorySubscription')
    def __str__(self):
        return self.categoryName

class CategorySubscription(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscriber} | {self.category}"

class Post(models.Model):
    article = 'AT'
    news = 'NW'

    ARTICLE_OR_NEWS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2,
                                choices=ARTICLE_OR_NEWS,
                                default=article)
    createData = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length = 128)
    articleText = models.TextField()
    rating = models.SmallIntegerField(default=0)
    description = models.TextField()

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return self.articleText[:123] + '...'

    def get_absolute_url(self):
        return f'/posts/{self.id}'
    
    def __str__(self):
        return f'{self.title} | {self.author}'

class PostCategory(models.Model):
    postTr = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTr = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryTr.categoryName} | {self.postTr.title}'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentCreateData = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()