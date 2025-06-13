from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='subscribers',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follow'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'


class Group(models.Model):
    slug = models.SlugField(unique=True)
    description = models.TextField()
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='published_posts'
    )
    text = models.TextField()
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='group_posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
