import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from insta_app.models import (
    UserProfile, Follow, Hashtag, Post, Content,
    PostLike, Comment, CommentLike, SavePost, SavePostItem, Stories
)


def clear_data():
    """Очистка всех данных"""
    print("Очистка базы данных...")
    Stories.objects.all().delete()
    SavePostItem.objects.all().delete()
    SavePost.objects.all().delete()
    CommentLike.objects.all().delete()
    Comment.objects.all().delete()
    PostLike.objects.all().delete()
    Content.objects.all().delete()
    Post.objects.all().delete()
    Hashtag.objects.all().delete()
    Follow.objects.all().delete()
    UserProfile.objects.all().delete()
    print("База данных очищена")


def populate_users():
    """Создание пользователей"""
    print("Создание пользователей...")

    users_data = [
        {
            'username': 'alex_music',
            'email': 'alex@example.com',
            'first_name': 'Alex',
            'last_name': 'Martinez',
            'bio': 'Music producer and DJ 🎵 | Electronic beats | Follow for daily inspiration',
            'network': 'https://soundcloud.com/alexmusic'
        },
        {
            'username': 'sarah_photo',
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'bio': 'Professional photographer 📸 | Travel enthusiast | Capturing moments around the world',
            'network': 'https://instagram.com/sarahphoto'
        },
        {
            'username': 'mike_beats',
            'email': 'mike@example.com',
            'first_name': 'Mike',
            'last_name': 'Chen',
            'bio': 'DJ and music producer 🎧 | Techno & House | Booking: mike@beats.com',
            'network': 'https://spotify.com/mikebeats'
        },
        {
            'username': 'emma_design',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Williams',
            'bio': 'Graphic designer & artist 🎨 | Creative soul | Available for freelance work',
            'network': 'https://behance.net/emmadesign'
        },
        {
            'username': 'david_fitness',
            'email': 'david@example.com',
            'first_name': 'David',
            'last_name': 'Brown',
            'bio': 'Personal trainer 💪 | Fitness coach | Transform your body and mind',
            'network': 'https://youtube.com/davidfitness'
        },
        {
            'username': 'lisa_food',
            'email': 'lisa@example.com',
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'bio': 'Food blogger & chef 🍳 | Sharing recipes daily | Cookbook author',
            'network': 'https://pinterest.com/lisafood'
        },
        {
            'username': 'john_travel',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'bio': 'Travel blogger ✈️ | 47 countries visited | Living my best life',
            'network': 'https://blog.johntravel.com'
        },
        {
            'username': 'kate_fashion',
            'email': 'kate@example.com',
            'first_name': 'Kate',
            'last_name': 'Davis',
            'bio': 'Fashion influencer 👗 | Style tips & trends | Collaborate: kate@fashion.com',
            'network': 'https://tiktok.com/@katefashion'
        },
        {
            'username': 'tom_tech',
            'email': 'tom@example.com',
            'first_name': 'Tom',
            'last_name': 'Wilson',
            'bio': 'Software developer 💻 | Tech reviews | Coding tutorials',
            'network': 'https://github.com/tomtech'
        },
        {
            'username': 'maria_yoga',
            'email': 'maria@example.com',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'bio': 'Yoga instructor 🧘‍♀️ | Mindfulness coach | Online classes available',
            'network': 'https://mariayoga.com'
        }
    ]

    users = []
    for i, user_data in enumerate(users_data, 1):
        user = UserProfile.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            password=make_password('password123'),
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            bio=user_data['bio'],
            user_network=user_data['network'],
            user_image=f'profile_images/user_{i}.png'
        )
        users.append(user)

    print(f"Создано {len(users)} пользователей")
    return users


def populate_follows(users):
    """Создание подписок"""
    print("Создание подписок...")

    follows = []
    # Каждый пользователь подписывается на 3-6 случайных пользователей
    for user in users:
        # Получаем список других пользователей
        other_users = [u for u in users if u != user]
        # Выбираем случайное количество пользователей для подписки
        follow_count = random.randint(3, 6)
        users_to_follow = random.sample(other_users, min(follow_count, len(other_users)))

        for followed_user in users_to_follow:
            # Проверяем, не существует ли уже такая подписка
            if not Follow.objects.filter(follower=user, following=followed_user).exists():
                follow = Follow.objects.create(
                    follower=user,
                    following=followed_user
                )
                follows.append(follow)

    print(f"Создано {len(follows)} подписок")
    return follows


def populate_hashtags():
    """Создание хештегов"""
    print("Создание хештегов...")

    hashtags_data = [
        'music', 'photography', 'travel', 'food', 'fitness',
        'fashion', 'art', 'design', 'nature', 'motivation',
        'lifestyle', 'tech', 'coding', 'beauty', 'health',
        'inspiration', 'love', 'instagood', 'photooftheday', 'happy',
        'dj', 'producer', 'electronic', 'techno', 'house',
        'workout', 'gym', 'yoga', 'meditation', 'wellness',
        'foodie', 'cooking', 'recipe', 'delicious', 'yummy',
        'style', 'ootd', 'fashionista', 'streetstyle', 'trending'
    ]

    hashtags = []
    for tag_name in hashtags_data:
        hashtag = Hashtag.objects.create(hashtag_name=tag_name)
        hashtags.append(hashtag)

    print(f"Создано {len(hashtags)} хештегов")
    return hashtags


def populate_posts(users, hashtags):
    """Создание постов"""
    print("Создание постов...")

    posts_data = [
        {
            'desc': 'Just dropped my new track! 🔥 Let me know what you think! #music #producer #electronic',
            'tags': ['music', 'producer', 'electronic', 'newmusic']
        },
        {
            'desc': 'Sunset vibes in Bishkek 🌅 The sky was absolutely breathtaking today! #photography #sunset #nature',
            'tags': ['photography', 'sunset', 'nature', 'bishkek']
        },
        {
            'desc': 'Live set from last night was incredible! Thanks to everyone who came out 🎉 #dj #livemusic #party',
            'tags': ['dj', 'livemusic', 'party', 'techno']
        },
        {
            'desc': 'New design project finished! So proud of how this turned out ✨ #design #art #creative',
            'tags': ['design', 'art', 'creative', 'graphicdesign']
        },
        {
            'desc': 'Morning workout complete! 💪 Remember, consistency is key! #fitness #motivation #workout',
            'tags': ['fitness', 'motivation', 'workout', 'gym']
        },
        {
            'desc': 'Trying out this amazing new recipe today 🍝 Who wants the recipe? #food #cooking #delicious',
            'tags': ['food', 'cooking', 'delicious', 'recipe']
        },
        {
            'desc': 'Exploring the beautiful mountains of Kyrgyzstan ⛰️ Nature therapy at its finest! #travel #nature #adventure',
            'tags': ['travel', 'nature', 'adventure', 'mountains']
        },
        {
            'desc': 'Today\'s outfit inspiration 👗 Simple but stylish! #fashion #ootd #style',
            'tags': ['fashion', 'ootd', 'style', 'fashionista']
        },
        {
            'desc': 'Working on an exciting new project! Stay tuned 💻 #tech #coding #developer',
            'tags': ['tech', 'coding', 'developer', 'programming']
        },
        {
            'desc': 'Sunday yoga session complete 🧘‍♀️ Feeling centered and peaceful #yoga #wellness #meditation',
            'tags': ['yoga', 'wellness', 'meditation', 'mindfulness']
        },
        {
            'desc': 'Behind the scenes of today\'s photoshoot 📸 #photography #bts #creative',
            'tags': ['photography', 'bts', 'creative', 'photooftheday']
        },
        {
            'desc': 'Late night studio session 🎧 The best ideas come after midnight! #music #studio #producer',
            'tags': ['music', 'studio', 'producer', 'beats']
        },
        {
            'desc': 'Healthy breakfast to start the day right! 🥑 #health #breakfast #healthyfood',
            'tags': ['health', 'breakfast', 'healthyfood', 'nutrition']
        },
        {
            'desc': 'New collection preview! What do you think? 👀 #fashion #style #collection',
            'tags': ['fashion', 'style', 'collection', 'trending']
        },
        {
            'desc': 'Just finished an amazing hike! The views were worth every step 🏔️ #travel #hiking #adventure',
            'tags': ['travel', 'hiking', 'adventure', 'nature']
        }
    ]

    posts = []
    for i, post_data in enumerate(posts_data):
        user = random.choice(users)

        # Случайная дата создания (последние 30 дней)
        random_date = datetime.now() - timedelta(days=random.randint(0, 30))

        post = Post.objects.create(
            user=user,
            description=post_data['desc'],
            created_date=random_date,
            music=f'music/track_{i + 1}.mp3' if random.random() > 0.7 else None
        )

        # Добавляем хештеги
        post_hashtags = [h for h in hashtags if h.hashtag_name in post_data['tags']]
        post.hashtag.set(post_hashtags)

        # Отмечаем 0-2 случайных людей
        tagged_count = random.randint(0, 2)
        if tagged_count > 0:
            tagged_users = random.sample([u for u in users if u != user],
                                        min(tagged_count, len(users) - 1))
            post.people.set(tagged_users)

        posts.append(post)

        # Создаем контент для поста (1-4 файла)
        content_count = random.randint(1, 4)
        for j in range(content_count):
            Content.objects.create(
                post=post,
                file=f'post_contents/post_{post.id}_content_{j + 1}.jpg'
            )

    print(f"Создано {len(posts)} постов и {sum(random.randint(1, 4) for _ in posts)} файлов контента")
    return posts


def populate_likes(users, posts):
    """Создание лайков для постов"""
    print("Создание лайков...")

    likes = []
    for post in posts:
        # Каждый пост лайкают 2-8 случайных пользователей
        like_count = random.randint(2, 8)
        users_who_like = random.sample(users, min(like_count, len(users)))

        for user in users_who_like:
            like = PostLike.objects.create(
                user=user,
                post=post,
                like=True
            )
            likes.append(like)

    print(f"Создано {len(likes)} лайков")
    return likes


def populate_comments(users, posts):
    """Создание комментариев"""
    print("Создание комментариев...")

    comments_data = [
        "Amazing! Love this! 🔥",
        "This is so cool! Great work! 👏",
        "Absolutely beautiful! ❤️",
        "Can't wait to see more! 🙌",
        "This made my day! 😊",
        "Incredible content! Keep it up! 💪",
        "So inspiring! Thank you for sharing! ✨",
        "Love your style! 👌",
        "This is awesome! 🎉",
        "Great shot! The lighting is perfect! 📸",
        "Your creativity is amazing! 🎨",
        "This is fire! 🔥🔥🔥",
        "Beautiful work! 💯",
        "Wow, just wow! 😍",
        "You're so talented! 🌟",
        "This is exactly what I needed to see today! 💕",
        "Fantastic! More please! 🙏",
        "Love the vibes! ✌️",
        "This is perfection! 👑",
        "So good! Keep doing what you do! 💫"
    ]

    comments = []
    for post in posts:
        # Каждый пост получает 1-5 комментариев
        comment_count = random.randint(1, 5)

        for _ in range(comment_count):
            user = random.choice([u for u in users if u != post.user])
            comment_text = random.choice(comments_data)

            # Случайная дата (после создания поста)
            days_after = random.randint(0, 5)
            comment_date = post.created_date + timedelta(days=days_after,
                                                        hours=random.randint(0, 23))

            comment = Comment.objects.create(
                user=user,
                post=post,
                text=comment_text,
                created_date=comment_date
            )
            comments.append(comment)

    print(f"Создано {len(comments)} комментариев")
    return comments


def populate_comment_likes(users, comments):
    """Создание лайков для комментариев"""
    print("Создание лайков для комментариев...")

    comment_likes = []
    for comment in comments:
        # Каждый комментарий лайкают 0-4 пользователей
        like_count = random.randint(0, 4)
        if like_count > 0:
            users_who_like = random.sample(users, min(like_count, len(users)))

            for user in users_who_like:
                comment_like = CommentLike.objects.create(
                    user=user,
                    comment=comment,
                    like=True
                )
                comment_likes.append(comment_like)

    print(f"Создано {len(comment_likes)} лайков для комментариев")
    return comment_likes


def populate_saved_posts(users, posts):
    """Создание сохраненных постов"""
    print("Создание сохраненных постов...")

    saved_items = []
    # Для половины пользователей создаем SavePost
    for user in random.sample(users, len(users) // 2):
        save_post = SavePost.objects.create(user=user)

        # Сохраняем 2-5 случайных постов
        posts_to_save = random.sample(posts, random.randint(2, 5))

        for post in posts_to_save:
            item = SavePostItem.objects.create(
                save_post=save_post,
                post=post
            )
            saved_items.append(item)

    print(f"Создано {len(saved_items)} сохраненных постов")
    return saved_items


def populate_stories(users):
    """Создание историй"""
    print("Создание историй...")

    stories = []
    # Половина пользователей создают истории
    for user in random.sample(users, len(users) // 2):
        # Каждый пользователь создает 1-3 истории
        story_count = random.randint(1, 3)

        for i in range(story_count):
            # Истории за последние 24 часа
            hours_ago = random.randint(0, 24)
            story_date = datetime.now() - timedelta(hours=hours_ago)

            story = Stories.objects.create(
                user=user,
                file=f'stories/story_{user.id}_{i + 1}.jpg',
                created_date=story_date
            )
            stories.append(story)

    print(f"Создано {len(stories)} историй")
    return stories


def main():
    """Главная функция"""
    print("=" * 80)
    print("НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ СОЦИАЛЬНОЙ СЕТИ")
    print("=" * 80)

    # Очищаем базу данных
    clear_data()

    # Заполняем данные в правильном порядке
    users = populate_users()
    follows = populate_follows(users)
    hashtags = populate_hashtags()
    posts = populate_posts(users, hashtags)
    likes = populate_likes(users, posts)
    comments = populate_comments(users, posts)
    comment_likes = populate_comment_likes(users, comments)
    saved_items = populate_saved_posts(users, posts)
    stories = populate_stories(users)

    print("=" * 80)
    print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 80)
    print(f"Всего создано:")
    print(f"  - Пользователей: {len(users)}")
    print(f"  - Подписок: {len(follows)}")
    print(f"  - Хештегов: {len(hashtags)}")
    print(f"  - Постов: {len(posts)}")
    print(f"  - Лайков постов: {len(likes)}")
    print(f"  - Комментариев: {len(comments)}")
    print(f"  - Лайков комментариев: {len(comment_likes)}")
    print(f"  - Сохраненных постов: {len(saved_items)}")
    print(f"  - Историй: {len(stories)}")
    print("=" * 80)


if __name__ == '__main__':
    main()