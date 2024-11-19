# README ✿✿✿

#### **Overview**

What I’ve created is a simple webpage that generates a small selection of art from the Art Institute of Chicago API and pairs it with a music album I recommend for your listening pleasure.

![Flask demo](C:\Users\Soe-Myat\OneDrive - Hogarth Worldwide\Pictures\Flask demo.png)

------

#### **Going Back One Step - My Fight with Spotify API (ง •̀_•́)ง**

As you may remember, ever since I started working with the Spotify API using Spotipy, I’ve struggled with my code freezing and hitting a wall when trying to access Spotify’s genre-based recommendations and create playlists. At first, I thought it was just the **"sp.recommendation_genre_seeds"** function causing the issue. The last time this happened, I was advised to add a cap to the number of retries for the API until it hits an error. However, even this didn’t work this time. I tested different parts of my coded in separate python files to find the culprit and I am sure it's the Spotify API giving me the same issue: **endless loading**.

In an attempt to meet the deadline, I pivoted and decided to **hardcode a set of albums** I thought would pair well with the art and use those albums to generate playlists instead of relying on the genre-based approach. Unfortunately, even after hardcoding the **URIs of the albums** straight from Spotify, I was still getting errors.

I also thought the issue might be due to the fact that I was using a **free Spotify account**, which could have been limited. So, I upgraded to a **free premium trial** account, but still, no luck.

Ultimately, my final solution was to **hardcode the selected albums**, paired with artwork categories, and just show them directly, bypassing the need for dynamically generated playlists. It wasn’t the ideal solution, but I ended up liking the results. It allowed me to showcase music I already liked without the frustration of struggling with the Spotify API.
