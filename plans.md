# TP > Plans

## General idea

* A database for Twiner, a very popular website
* There's users that interact by: 
  * Signing up, and receiving a unique id
  * Uploading and removing posts
  * Seeing posts and:
    * Liking them
    * Commenting on them
    * Liking comments
    * Re-twining them 

* An ordered map for currently logged in users
* When an user signs up they get a unique ID
* And when they log in they get a temporary session ID
* For every interaction they send an API request with their user ID and their session ID
  * We look for their user in an ordered map and check the current and provided session IDs match

* A list of posts sorted by date 
* We keep track of each user's position in it
  * If their current post is removed, we look from the start for what would be the next post
* They can choose to interact with the post and:
  * Like it
  * Re-twine it
* They can also get embarrassed and delete a post of theirs
