from __future__ import annotations

import heapq


class Twitter:
    def __init__(self) -> None:
        self.time = 0
        self.tweets: dict[int, list[tuple[int, int]]] = {}
        self.following: dict[int, set[int]] = {}

    def postTweet(self, userId: int, tweetId: int) -> None:
        if userId not in self.tweets:
            self.tweets[userId] = []

        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> list[int]:
        visible_users = set(self.following.get(userId, set()))
        visible_users.add(userId)

        max_heap: list[tuple[int, int, int, int]] = []

        for visible_user in visible_users:
            user_tweets = self.tweets.get(visible_user, [])

            if user_tweets:
                index = len(user_tweets) - 1
                timestamp, tweet_id = user_tweets[index]
                heapq.heappush(
                    max_heap,
                    (-timestamp, tweet_id, visible_user, index),
                )

        news_feed: list[int] = []

        while max_heap and len(news_feed) < 10:
            _, tweet_id, author_id, index = heapq.heappop(max_heap)
            news_feed.append(tweet_id)

            previous_index = index - 1

            if previous_index >= 0:
                timestamp, previous_tweet_id = self.tweets[author_id][previous_index]
                heapq.heappush(
                    max_heap,
                    (
                        -timestamp,
                        previous_tweet_id,
                        author_id,
                        previous_index,
                    ),
                )

        return news_feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId == followeeId:
            return

        if followerId not in self.following:
            self.following[followerId] = set()

        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followerId in self.following:
            self.following[followerId].discard(followeeId)


if __name__ == "__main__":
    twitter = Twitter()
    twitter.postTweet(1, 5)
    assert twitter.getNewsFeed(1) == [5]

    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    assert twitter.getNewsFeed(1) == [6, 5]

    twitter.unfollow(1, 2)
    assert twitter.getNewsFeed(1) == [5]

    merged_feed = Twitter()
    merged_feed.postTweet(1, 101)
    merged_feed.postTweet(2, 201)
    merged_feed.follow(1, 2)
    merged_feed.postTweet(2, 202)
    assert merged_feed.getNewsFeed(1) == [202, 201, 101]

    latest_ten = Twitter()
    for tweet_id in range(1, 13):
        latest_ten.postTweet(3, tweet_id)
    assert latest_ten.getNewsFeed(3) == list(range(12, 2, -1))

    latest_ten.follow(3, 4)
    latest_ten.follow(3, 4)
    latest_ten.unfollow(3, 99)
    latest_ten.unfollow(3, 3)
    assert latest_ten.getNewsFeed(3) == list(range(12, 2, -1))

    print("All examples passed.")
